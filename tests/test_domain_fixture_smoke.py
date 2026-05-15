from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FIXTURES = Path(__file__).resolve().parent / "fixtures"


def run_json(*args: str) -> dict:
    result = subprocess.run([sys.executable, *args], cwd=ROOT, text=True, capture_output=True, check=False)
    assert result.returncode == 0, result.stderr or result.stdout
    return json.loads(result.stdout)


def test_cad_dwg_route_smoke_uses_safe_plan_without_mutation(tmp_path: Path) -> None:
    source = tmp_path / "sample.dwg"
    source.write_bytes(b"placeholder dwg fixture")

    payload = run_json("cad-autocad-dwg-dxf-isleme/scripts/plan_dwg_conversion.py", str(source))

    assert payload["target_dxf"].endswith("sample.dxf")
    assert payload["recommended_route"] in {"dwg2dxf_then_ezdxf_qa", "install_libredwg_or_use_freecad_librecad"}
    assert "qa_after_conversion" in payload


def test_bim_revit_ifc_route_smoke_records_export_settings(tmp_path: Path) -> None:
    source = tmp_path / "model.rvt"
    source.write_text("placeholder revit fixture", encoding="utf-8")

    payload = run_json(
        "bim-revit-ifc-model-kontrolu/scripts/plan_revit_ifc_export.py",
        str(source),
        "--schema",
        "IFC4 Reference View",
        "--discipline",
        "architecture",
    )

    assert payload["requested_schema"] == "IFC4 Reference View"
    assert "rooms/spaces export" in payload["export_settings_to_record"]
    assert any("IFC" in item or "ifc" in item for item in payload["recommended_route"])


def test_blender_job_plan_smoke_does_not_run_blender(tmp_path: Path) -> None:
    payload = run_json(
        "blender-3d-modelleme-ve-render/scripts/plan_blender_job.py",
        "--job-type",
        "fixture_scene",
        "--output-dir",
        str(tmp_path / "blender-output"),
    )

    assert payload["job_type"] == "fixture_scene"
    assert "render_file_nonzero" in payload["quality_gates"]
    assert payload["command_to_review"] is None or "--background" in payload["command_to_review"]


def test_sketchup_ruby_generation_smoke(tmp_path: Path) -> None:
    output = tmp_path / "massing.rb"
    payload = run_json(
        "sketchup-konsept-ve-kutle-modelleme/scripts/generate_sketchup_massing_ruby.py",
        "--spec",
        str(FIXTURES / "concept_massing_spec.json"),
        "--output",
        str(output),
    )

    ruby = output.read_text(encoding="utf-8")
    assert payload["ruby_script"] == str(output)
    assert "Sketchup.active_model" in ruby
    assert "model.save" in ruby
    assert "construction_ai" in ruby


def test_photo_evidence_fixture_flags_privacy_and_missing_data() -> None:
    payload = run_json(
        "saha-fotograf-ve-kanit-analizi/scripts/validate_photo_evidence_register.py",
        str(FIXTURES / "photo_evidence_register.json"),
        "--no-file-check",
        "--format",
        "json",
    )

    flags = {item["flag"] for item in payload["issues"] if item["evidence_id"] == "PH-002"}
    assert payload["summary"]["photo_count"] == 2
    assert payload["summary"]["needs_review_count"] == 1
    assert {"missing_sha256", "missing_capture_date", "privacy_review", "low_resolution"} <= flags
