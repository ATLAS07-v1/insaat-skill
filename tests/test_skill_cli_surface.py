from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HELP_SCRIPTS_BY_SKILL = {
    "insaat-arac-kullanimlari": "scripts/inspect_construction_inputs.py",
    "cad-autocad-dwg-dxf-isleme": "scripts/plan_dwg_conversion.py",
    "bim-revit-ifc-model-kontrolu": "scripts/plan_revit_ifc_export.py",
    "blender-3d-modelleme-ve-render": "scripts/plan_blender_job.py",
    "sketchup-konsept-ve-kutle-modelleme": "scripts/plan_sketchup_job.py",
    "cizim-dosya-donusum-ve-qa": "scripts/plan_file_conversion.py",
    "insaat-hesaplamalar": "scripts/basic_quantity_calculator.py",
    "metraj-ve-mahal-kontrolu": "scripts/plan_metraj_mahal_route.py",
    "teknik-sartname-ve-uygulama-kontrolu": "scripts/plan_spec_review_route.py",
    "insaat-tasarim-ve-konsept": "scripts/plan_design_concept_route.py",
    "teklif-ve-maliyet-tablolama": "scripts/plan_bid_cost_route.py",
    "hakedis-ve-mutabakat-kontrolu": "scripts/plan_progress_payment_route.py",
    "tedarik-ve-malzeme-karsilastirma": "scripts/plan_procurement_route.py",
    "risk-guvenlik-ve-uygunluk-denetimi": "scripts/plan_risk_compliance_route.py",
    "musteri-ve-taseron-iletisim-hazirlayici": "scripts/plan_communication_route.py",
    "saha-fotograf-ve-kanit-analizi": "scripts/plan_photo_evidence_route.py",
    "dokuman-standartlastirma-ve-formatlama": "scripts/plan_document_standardization_route.py",
}


def run_script(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run([sys.executable, *args], cwd=ROOT, text=True, capture_output=True, check=False)


def test_each_skill_exposes_at_least_one_helping_cli_surface() -> None:
    assert len(HELP_SCRIPTS_BY_SKILL) == 17
    for skill_name, script in HELP_SCRIPTS_BY_SKILL.items():
        path = ROOT / skill_name / script
        result = run_script(str(path), "--help")
        assert result.returncode == 0, result.stderr or result.stdout
        assert "usage" in result.stdout.lower()


def test_optional_cad_bim_tools_fail_gracefully_without_traceback(tmp_path: Path) -> None:
    samples = [
        ("cad-autocad-dwg-dxf-isleme/scripts/inspect_dxf_ezdxf.py", tmp_path / "missing.dxf"),
        ("bim-revit-ifc-model-kontrolu/scripts/inspect_ifc_ifcopenshell.py", tmp_path / "missing.ifc"),
        ("metraj-ve-mahal-kontrolu/scripts/extract_ifc_spaces_ifcopenshell.py", tmp_path / "missing.ifc"),
    ]
    for script, missing_file in samples:
        result = run_script(script, str(missing_file))
        combined = result.stdout + result.stderr
        assert combined.strip()
        assert result.returncode in {0, 1, 2}
        assert "Traceback" not in combined
        assert any(
            token in combined.lower()
            for token in ["error", "hint", "install", "missing", "not installed", "not found", "no such file"]
        )
