#!/usr/bin/env python3
"""Create a tool route for construction design and concept tasks."""

from __future__ import annotations

import argparse
import json
from typing import Any


ROUTES: dict[str, dict[str, Any]] = {
    "site_concept": {
        "goal": "Arsa, çevre, giriş, servis ve kütle yerleşimi için konsept üretmek.",
        "tools": ["QGIS/OSMnx/GeoPandas", "Shapely", "generate_concept_options.py"],
        "next_skills": ["cad-autocad-dwg-dxf-isleme", "blender-3d-modelleme-ve-render"],
    },
    "massing_options": {
        "goal": "Alan hedeflerine göre kütle alternatifleri ve karar matrisi üretmek.",
        "tools": ["generate_concept_options.py", "FreeCAD/BIM Workbench", "Blender/Bonsai"],
        "next_skills": ["sketchup-konsept-ve-kutle-modelleme", "blender-3d-modelleme-ve-render"],
    },
    "space_program": {
        "goal": "Mahal programını bloklara, adjacency notlarına ve kütle parametrelerine çevirmek.",
        "tools": ["JSON/CSV program", "TopologicPy/NetworkX", "metraj-ve-mahal-kontrolu"],
        "next_skills": ["metraj-ve-mahal-kontrolu", "bim-revit-ifc-model-kontrolu"],
    },
    "facade_concept": {
        "goal": "Cephe dili, açıklık/gölgeleme fikri, malzeme paleti ve görsel brief üretmek.",
        "tools": ["Blender", "Ladybug/Honeybee", "material board brief"],
        "next_skills": ["blender-3d-modelleme-ve-render", "teknik-sartname-ve-uygulama-kontrolu"],
    },
    "sustainability_concept": {
        "goal": "Güneş, gün ışığı, enerji, doğal havalandırma ve açık alan stratejilerini ön değerlendirmek.",
        "tools": ["Ladybug/Honeybee", "OpenStudio/EnergyPlus", "QGIS climate/site context"],
        "next_skills": ["insaat-hesaplamalar", "teknik-sartname-ve-uygulama-kontrolu"],
    },
    "client_presentation_concept": {
        "goal": "Müşteri sunumu için sade konsept hikayesi, alternatif karşılaştırması ve görsel üretim brief'i hazırlamak.",
        "tools": ["Markdown report", "Blender render brief", "SketchUp scene list"],
        "next_skills": ["musteri-ve-taseron-iletisim-hazirlayici", "blender-3d-modelleme-ve-render"],
    },
}


def build_plan(args: argparse.Namespace) -> dict[str, Any]:
    route = ROUTES[args.job_type]
    phases = [
        {
            "phase": "brief_derleme",
            "actions": [
                "Proje tipi, hedef kullanıcı, arsa, program, kısıt ve çıktı formatı toplanır.",
                "Eksik ölçü, kuzey, imar, çekme mesafesi ve hedef alan bayraklanır.",
            ],
        },
        {
            "phase": "alternatif_uretimi",
            "actions": [
                "En az iki gerçek konsept alternatifi üretilir.",
                "Her alternatif için alan, kaplama, açık alan, artı/eksi ve risk yazılır.",
            ],
        },
        {
            "phase": "karar_matrisi",
            "actions": [
                "Program uyumu, site response, gün ışığı, maliyet basitliği ve esneklik ağırlıklandırılır.",
                "Sonuç konsept önerisi olarak yazılır; resmi uygunluk iddiası kurulmaz.",
            ],
        },
    ]
    if args.has_gis:
        phases.append(
            {
                "phase": "gis_baglam",
                "actions": [
                    "QGIS/OSMnx/GeoPandas ile yol, bina, POI, erişim ve bağlam analizi rotası açılır.",
                    "OSM veri kalitesi ve lisans atfı rapora eklenir.",
                ],
            }
        )
    if args.has_performance_goal:
        phases.append(
            {
                "phase": "performans_on_degerlendirme",
                "actions": [
                    "Ladybug/Honeybee/OpenStudio/EnergyPlus hattı için gerekli geometri ve iklim verisi listelenir.",
                    "Simülasyon yoksa sonuç tasarım hipotezi olarak işaretlenir.",
                ],
            }
        )
    return {
        "job_type": args.job_type,
        "project_type": args.project_type,
        "goal": route["goal"],
        "recommended_tools": route["tools"],
        "next_skills": route["next_skills"],
        "phases": phases,
        "quality_gates": [
            "Ölçü, birim ve kuzey bilgisi doğrulanmalı.",
            "İmar ve çekme mesafesi kesin değilse alternatifler konsept olarak işaretlenmeli.",
            "Alan türleri net/brüt/emsal/toplam inşaat alanı olarak ayrılmalı.",
            "Her alternatif artı, eksi, risk ve sonraki araç rotası içermeli.",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--job-type", choices=sorted(ROUTES), default="massing_options")
    parser.add_argument("--project-type", default="mixed_use")
    parser.add_argument("--has-gis", action="store_true")
    parser.add_argument("--has-performance-goal", action="store_true")
    args = parser.parse_args()
    print(json.dumps(build_plan(args), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
