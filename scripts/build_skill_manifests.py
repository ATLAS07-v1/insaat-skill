#!/usr/bin/env python3
"""Build canonical skill manifests and the root skill index."""

from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[1]
VERSION = "0.1.0"
SCHEMA_VERSION = "1.0.0"
LANGUAGE = "tr"
REPOSITORY = "https://github.com/ATLAS07-v1/insaat-skill"


ORDER = [
    "insaat-arac-kullanimlari",
    "cad-autocad-dwg-dxf-isleme",
    "bim-revit-ifc-model-kontrolu",
    "blender-3d-modelleme-ve-render",
    "sketchup-konsept-ve-kutle-modelleme",
    "cizim-dosya-donusum-ve-qa",
    "insaat-hesaplamalar",
    "metraj-ve-mahal-kontrolu",
    "teknik-sartname-ve-uygulama-kontrolu",
    "insaat-tasarim-ve-konsept",
    "teklif-ve-maliyet-tablolama",
    "hakedis-ve-mutabakat-kontrolu",
    "tedarik-ve-malzeme-karsilastirma",
    "risk-guvenlik-ve-uygunluk-denetimi",
    "musteri-ve-taseron-iletisim-hazirlayici",
    "saha-fotograf-ve-kanit-analizi",
    "dokuman-standartlastirma-ve-formatlama",
]

DISPLAY_NAMES = {
    "insaat-arac-kullanimlari": "İnşaat Araç Kullanımları",
    "cad-autocad-dwg-dxf-isleme": "CAD AutoCAD DWG/DXF İşleme",
    "bim-revit-ifc-model-kontrolu": "BIM Revit IFC Model Kontrolü",
    "blender-3d-modelleme-ve-render": "Blender 3D Modelleme ve Render",
    "sketchup-konsept-ve-kutle-modelleme": "SketchUp Konsept ve Kütle Modelleme",
    "cizim-dosya-donusum-ve-qa": "Çizim Dosya Dönüşüm ve QA",
    "insaat-hesaplamalar": "İnşaat Hesaplamalar",
    "metraj-ve-mahal-kontrolu": "Metraj ve Mahal Kontrolü",
    "teknik-sartname-ve-uygulama-kontrolu": "Teknik Şartname ve Uygulama Kontrolü",
    "insaat-tasarim-ve-konsept": "İnşaat Tasarım ve Konsept",
    "teklif-ve-maliyet-tablolama": "Teklif ve Maliyet Tablolama",
    "hakedis-ve-mutabakat-kontrolu": "Hakediş ve Mutabakat Kontrolü",
    "tedarik-ve-malzeme-karsilastirma": "Tedarik ve Malzeme Karşılaştırma",
    "risk-guvenlik-ve-uygunluk-denetimi": "Risk Güvenlik ve Uygunluk Denetimi",
    "musteri-ve-taseron-iletisim-hazirlayici": "Müşteri ve Taşeron İletişim Hazırlayıcı",
    "saha-fotograf-ve-kanit-analizi": "Saha Fotoğraf ve Kanıt Analizi",
    "dokuman-standartlastirma-ve-formatlama": "Doküman Standartlaştırma ve Formatlama",
}


META: dict[str, dict[str, Any]] = {
    "insaat-arac-kullanimlari": {
        "tags": ["insaat", "arac-secimi", "dosya-inceleme", "dokuman", "tablo", "rota-planlama"],
        "triggers": ["inşaat girdilerini incele", "hangi araçla açılır", "dosya envanteri", "araç kullanım rotası"],
        "inputs": ["construction_files", "pdf", "docx", "xlsx", "csv", "images", "project_context"],
        "outputs": ["input_inventory", "tool_route", "document_skeleton", "table_skeleton", "qa_notes"],
        "risk_level": "medium",
        "requires_human_approval": False,
        "related_skills": ["cizim-dosya-donusum-ve-qa", "dokuman-standartlastirma-ve-formatlama"],
    },
    "cad-autocad-dwg-dxf-isleme": {
        "tags": ["cad", "autocad", "dwg", "dxf", "layer", "block", "markup"],
        "triggers": ["DWG incele", "DXF analiz et", "CAD layer kontrolü", "AutoCAD dönüşüm planı"],
        "inputs": ["dwg_file", "dxf_file", "pdf_markup", "cad_standards", "layer_list"],
        "outputs": ["cad_qa_report", "dxf_entity_report", "conversion_plan", "markup_summary"],
        "risk_level": "medium",
        "requires_human_approval": True,
        "related_skills": ["cizim-dosya-donusum-ve-qa", "metraj-ve-mahal-kontrolu"],
    },
    "bim-revit-ifc-model-kontrolu": {
        "tags": ["bim", "revit", "ifc", "ids", "bcf", "model-qa"],
        "triggers": ["IFC model kontrolü", "Revit export", "BIM QA", "IDS uygunluk", "BCF issue"],
        "inputs": ["ifc_model", "rvt_context", "ids_file", "bcf_issue", "bim_requirements"],
        "outputs": ["bim_qa_report", "ifc_element_summary", "ids_check_plan", "bcf_issue_summary"],
        "risk_level": "high",
        "requires_human_approval": True,
        "related_skills": ["metraj-ve-mahal-kontrolu", "teknik-sartname-ve-uygulama-kontrolu"],
    },
    "blender-3d-modelleme-ve-render": {
        "tags": ["blender", "3d", "render", "python", "modelleme", "gorsellestirme"],
        "triggers": ["Blender sahnesi oluştur", "3D render", "kütle model", "malzeme ışık kamera"],
        "inputs": ["scene_brief", "model_reference", "materials", "camera_views", "export_format"],
        "outputs": ["blender_script", "scene_plan", "render_plan", "export_notes"],
        "risk_level": "low",
        "requires_human_approval": False,
        "related_skills": ["insaat-tasarim-ve-konsept", "sketchup-konsept-ve-kutle-modelleme"],
    },
    "sketchup-konsept-ve-kutle-modelleme": {
        "tags": ["sketchup", "konsept", "kutle-model", "ruby", "sahne", "yerlesim"],
        "triggers": ["SketchUp brief", "kütle model", "konsept sahne", "yerleşim modeli"],
        "inputs": ["concept_brief", "site_constraints", "massing_program", "view_list"],
        "outputs": ["sketchup_ruby_script", "massing_plan", "scene_list", "export_notes"],
        "risk_level": "low",
        "requires_human_approval": False,
        "related_skills": ["insaat-tasarim-ve-konsept", "blender-3d-modelleme-ve-render"],
    },
    "cizim-dosya-donusum-ve-qa": {
        "tags": ["dosya-donusum", "pdf", "dwg", "dxf", "ifc", "qa", "format"],
        "triggers": ["dosya dönüşümü", "PDF QA", "DWG DXF IFC dönüştür", "çizim paketini kontrol et"],
        "inputs": ["source_files", "target_format", "conversion_requirements", "drawing_package"],
        "outputs": ["conversion_route", "file_package_report", "qa_flags", "format_risk_notes"],
        "risk_level": "medium",
        "requires_human_approval": True,
        "related_skills": ["cad-autocad-dwg-dxf-isleme", "bim-revit-ifc-model-kontrolu"],
    },
    "insaat-hesaplamalar": {
        "tags": ["hesaplama", "metraj", "malzeme", "birim", "varsayim", "formul"],
        "triggers": ["inşaat hesabı", "malzeme hesabı", "alan hacim ağırlık", "beton donatı kalıp hesapla"],
        "inputs": ["calculation_request", "dimensions", "units", "assumptions", "material_specs"],
        "outputs": ["calculation_result", "assumption_log", "unit_check", "risk_notes"],
        "risk_level": "high",
        "requires_human_approval": True,
        "related_skills": ["metraj-ve-mahal-kontrolu", "teklif-ve-maliyet-tablolama"],
    },
    "metraj-ve-mahal-kontrolu": {
        "tags": ["metraj", "mahal", "quantity", "room-schedule", "ifc", "qa"],
        "triggers": ["metraj kontrolü", "mahal listesi", "room schedule karşılaştır", "IFC space çıkar"],
        "inputs": ["quantity_table", "room_schedule", "ifc_model", "boq", "measurement_rules"],
        "outputs": ["quantity_comparison", "space_schedule_report", "metraj_qa_flags"],
        "risk_level": "high",
        "requires_human_approval": True,
        "related_skills": ["bim-revit-ifc-model-kontrolu", "teklif-ve-maliyet-tablolama"],
    },
    "teknik-sartname-ve-uygulama-kontrolu": {
        "tags": ["teknik-sartname", "uygulama-kontrol", "evidence", "ids", "bcf", "qa"],
        "triggers": ["şartname kontrolü", "uygulama kanıtı", "madde çıkar", "checklist oluştur"],
        "inputs": ["specification", "evidence_files", "checklist", "ids_file", "site_records"],
        "outputs": ["clause_register", "evidence_comparison", "application_checklist", "nonconformance_notes"],
        "risk_level": "high",
        "requires_human_approval": True,
        "related_skills": ["risk-guvenlik-ve-uygunluk-denetimi", "dokuman-standartlastirma-ve-formatlama"],
    },
    "insaat-tasarim-ve-konsept": {
        "tags": ["tasarim", "konsept", "yerlesim", "kutle", "surdurulebilirlik", "performans"],
        "triggers": ["konsept tasarım", "yerleşim alternatifi", "kütle opsiyonu", "tasarım skoru"],
        "inputs": ["design_brief", "site_data", "program", "constraints", "performance_goals"],
        "outputs": ["concept_options", "design_scorecard", "layout_notes", "risk_tradeoffs"],
        "risk_level": "medium",
        "requires_human_approval": True,
        "related_skills": ["blender-3d-modelleme-ve-render", "sketchup-konsept-ve-kutle-modelleme"],
    },
    "teklif-ve-maliyet-tablolama": {
        "tags": ["teklif", "maliyet", "boq", "fiyat", "excel", "risk"],
        "triggers": ["teklif hazırla", "maliyet tablosu", "BOQ", "birim fiyat", "keşif özeti"],
        "inputs": ["boq_items", "unit_prices", "tax_rules", "risk_allowances", "supplier_quotes"],
        "outputs": ["cost_table", "bid_summary", "risk_allowance_report", "xlsx_export"],
        "risk_level": "high",
        "requires_human_approval": True,
        "related_skills": ["tedarik-ve-malzeme-karsilastirma", "hakedis-ve-mutabakat-kontrolu"],
    },
    "hakedis-ve-mutabakat-kontrolu": {
        "tags": ["hakedis", "mutabakat", "fatura", "odeme", "kesinti", "hakediş"],
        "triggers": ["hakediş hesapla", "mutabakat kontrolü", "fatura ödeme karşılaştır", "kesinti avans teminat"],
        "inputs": ["progress_items", "contract_quantities", "invoices", "payments", "deductions"],
        "outputs": ["progress_payment_report", "reconciliation_report", "mismatch_flags", "payment_summary"],
        "risk_level": "high",
        "requires_human_approval": True,
        "related_skills": ["teklif-ve-maliyet-tablolama", "metraj-ve-mahal-kontrolu"],
    },
    "tedarik-ve-malzeme-karsilastirma": {
        "tags": ["tedarik", "malzeme", "rfq", "supplier", "datasheet", "sertifika"],
        "triggers": ["tedarikçi karşılaştır", "malzeme teknik uygunluk", "RFQ", "datasheet sertifika kontrolü"],
        "inputs": ["supplier_quotes", "material_specs", "datasheets", "certificates", "delivery_terms"],
        "outputs": ["supplier_comparison", "material_compliance_matrix", "procurement_risk_report"],
        "risk_level": "high",
        "requires_human_approval": True,
        "related_skills": ["teklif-ve-maliyet-tablolama", "teknik-sartname-ve-uygulama-kontrolu"],
    },
    "risk-guvenlik-ve-uygunluk-denetimi": {
        "tags": ["risk", "isg", "uygunluk", "kanit", "denetim", "bcf"],
        "triggers": ["risk değerlendirmesi", "İSG denetimi", "uygunluk kontrolü", "kanıt matrisi"],
        "inputs": ["risk_register", "compliance_checklist", "evidence_register", "method_statement", "permit_to_work"],
        "outputs": ["risk_score_report", "compliance_audit", "nonconformance_action_plan", "evidence_gap_matrix"],
        "risk_level": "high",
        "requires_human_approval": True,
        "related_skills": ["saha-fotograf-ve-kanit-analizi", "teknik-sartname-ve-uygulama-kontrolu"],
    },
    "musteri-ve-taseron-iletisim-hazirlayici": {
        "tags": ["iletisim", "musteri", "taseron", "rfi", "submittal", "toplanti"],
        "triggers": ["müşteri e-postası", "taşeron mesajı", "RFI taslağı", "toplantı tutanağı", "aksiyon takibi"],
        "inputs": ["project_context", "recipient", "communication_type", "facts", "references", "attachments"],
        "outputs": ["message_draft", "meeting_minutes", "action_list", "communication_risk_check"],
        "risk_level": "high",
        "requires_human_approval": True,
        "related_skills": ["dokuman-standartlastirma-ve-formatlama", "risk-guvenlik-ve-uygunluk-denetimi"],
    },
    "saha-fotograf-ve-kanit-analizi": {
        "tags": ["saha-fotografi", "kanit", "exif", "ocr", "privacy", "drone"],
        "triggers": ["saha fotoğrafı", "kanıt analizi", "EXIF metadata", "fotoğraf register", "duplicate foto"],
        "inputs": ["photo_folder", "image_files", "project_context", "evidence_register", "annotations"],
        "outputs": ["photo_evidence_register", "metadata_integrity_report", "visual_findings", "privacy_flags"],
        "risk_level": "high",
        "requires_human_approval": True,
        "related_skills": ["risk-guvenlik-ve-uygunluk-denetimi", "musteri-ve-taseron-iletisim-hazirlayici"],
    },
    "dokuman-standartlastirma-ve-formatlama": {
        "tags": ["dokuman", "formatlama", "docx", "pdf", "markdown", "revizyon", "qa"],
        "triggers": ["doküman standardı", "DOCX PDF formatla", "Markdown QA", "revizyon kontrolü"],
        "inputs": ["source_documents", "document_type", "template_requirements", "revision_data", "output_format"],
        "outputs": ["standardized_document", "pdf_export", "document_manifest", "formatting_qa_report"],
        "risk_level": "medium",
        "requires_human_approval": True,
        "related_skills": ["musteri-ve-taseron-iletisim-hazirlayici", "teknik-sartname-ve-uygulama-kontrolu"],
    },
}


APPROVAL_CONTEXTS = {
    "high": [
        "teknik, mali, hukuki, İSG veya sözleşmesel nihai karar",
        "üçüncü taraf gönderimi veya şirket adına taahhüt",
        "resmi onay, ödeme, satın alma, hakediş, teslim veya uygunluk beyanı",
    ],
    "medium": [
        "teknik karar, teslim çıktısı veya üçüncü tarafla paylaşım",
        "kaynak verisi eksik veya varsayım kullanılan çıktı",
    ],
    "low": ["nihai teslim veya üçüncü taraf paylaşımı"],
}


def read_frontmatter(skill_dir: Path) -> dict[str, str]:
    text = (skill_dir / "SKILL.md").read_text(encoding="utf-8-sig")
    if not text.startswith("---"):
        raise SystemExit(f"Frontmatter yok: {skill_dir / 'SKILL.md'}")
    match = re.match(r"^---\s*\n(.*?)\n---\s*\n", text, re.DOTALL)
    if not match:
        raise SystemExit(f"Frontmatter okunamadı: {skill_dir / 'SKILL.md'}")
    data: dict[str, str] = {}
    for line in match.group(1).splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        data[key.strip()] = value.strip()
    return data


def display_name(name: str) -> str:
    if name in DISPLAY_NAMES:
        return DISPLAY_NAMES[name]
    words = name.replace("-", " ").split()
    return " ".join(word.capitalize() for word in words)


def list_tools(skill_dir: Path) -> list[dict[str, str]]:
    scripts_dir = skill_dir / "scripts"
    if not scripts_dir.exists():
        return []
    tools = []
    for script in sorted(scripts_dir.glob("*.py")):
        tools.append(
            {
                "name": script.stem,
                "type": "cli",
                "path": f"scripts/{script.name}",
                "command": f"python scripts/{script.name}",
            }
        )
    return tools


def guardrails(name: str, risk_level: str, approval_required: bool) -> list[str]:
    items = [
        "Kaynak, varsayım, eksik veri ve çıktı sınırları açık yazılmalıdır.",
        "Bu skill karar destek ve çıktı hazırlama amacı taşır; yetkili onay yerine geçmez.",
    ]
    if approval_required:
        items.append("Hukuki, finansal, İSG, teknik veya üçüncü taraf taahhüdü doğuran kararlar insan onayı gerektirir.")
    if "iletisim" in name:
        items.append("Bu skill üçüncü taraflara mesaj göndermez; yalnızca taslak ve kontrol çıktısı üretir.")
    if "risk" in name or "guvenlik" in name:
        items.append("Resmi İSG, hukuk veya yapı denetim uygunluğu kesin ifade edilmez.")
    if "foto" in name or "kanit" in name:
        items.append("Kişisel veri, GPS, yüz, plaka ve hassas saha bilgileri paylaşım öncesi kontrol edilmelidir.")
    if "teklif" in name or "hakedis" in name or "tedarik" in name:
        items.append("Fiyat, ödeme, satın alma ve hakediş çıktıları yetkili finans/ticari onay gerektirir.")
    if risk_level == "high":
        items.append("Yüksek riskli çıktılarda nihai karar kullanıcı veya yetkili uzman tarafından doğrulanmalıdır.")
    return items


def build_skill_manifest(name: str) -> dict[str, Any]:
    skill_dir = ROOT / name
    frontmatter = read_frontmatter(skill_dir)
    meta = META[name]
    risk_level = meta["risk_level"]
    approval_required = bool(meta["requires_human_approval"])
    return {
        "schema_version": SCHEMA_VERSION,
        "name": name,
        "version": VERSION,
        "language": LANGUAGE,
        "display_name": display_name(name),
        "description": frontmatter["description"],
        "entrypoint": "SKILL.md",
        "default_prompt": f"{display_name(name)} skillini kullanarak kullanıcının inşaat operasyonu talebini analiz et, uygun araç rotasını seç, çıktı sınırlarını ve gerekli insan onaylarını belirt.",
        "tags": meta["tags"],
        "triggers": meta["triggers"],
        "inputs": meta["inputs"],
        "outputs": meta["outputs"],
        "guardrails": guardrails(name, risk_level, approval_required),
        "risk_level": risk_level,
        "requires_human_approval": approval_required,
        "human_approval_contexts": APPROVAL_CONTEXTS[risk_level],
        "tools": list_tools(skill_dir),
        "related_skills": meta["related_skills"],
    }


def write_skill_manifest(name: str, manifest: dict[str, Any]) -> None:
    path = ROOT / name / "agents" / "openai.yaml"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(manifest, sort_keys=False, allow_unicode=True, width=120), encoding="utf-8")


def build_index(manifests: list[dict[str, Any]]) -> dict[str, Any]:
    existing_index = ROOT / "skill-index.json"
    generated_at = datetime.now(tz=timezone.utc).isoformat().replace("+00:00", "Z")
    if existing_index.exists():
        try:
            generated_at = json.loads(existing_index.read_text(encoding="utf-8-sig")).get("generated_at") or generated_at
        except json.JSONDecodeError:
            pass
    skills = []
    for manifest in manifests:
        skills.append(
            {
                "name": manifest["name"],
                "version": manifest["version"],
                "path": manifest["name"],
                "manifest": f"{manifest['name']}/agents/openai.yaml",
                "entrypoint": f"{manifest['name']}/SKILL.md",
                "display_name": manifest["display_name"],
                "description": manifest["description"],
                "tags": manifest["tags"],
                "triggers": manifest["triggers"],
                "inputs": manifest["inputs"],
                "outputs": manifest["outputs"],
                "tools": manifest["tools"],
                "related_skills": manifest["related_skills"],
                "risk_level": manifest["risk_level"],
                "requires_human_approval": manifest["requires_human_approval"],
            }
        )
    return {
        "schema_version": SCHEMA_VERSION,
        "name": "insaat-skill-seti",
        "version": VERSION,
        "language": LANGUAGE,
        "description": "Hermes/Codex benzeri agent'ler için inşaat operasyonlarına özel tekrar kullanılabilir yetenek skill seti.",
        "repository": REPOSITORY,
        "generated_at": generated_at,
        "skill_count": len(skills),
        "skills": skills,
    }


def main() -> int:
    manifests = [build_skill_manifest(name) for name in ORDER]
    for manifest in manifests:
        write_skill_manifest(manifest["name"], manifest)
    index = build_index(manifests)
    (ROOT / "skill-index.json").write_text(json.dumps(index, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {len(manifests)} skill manifests and skill-index.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
