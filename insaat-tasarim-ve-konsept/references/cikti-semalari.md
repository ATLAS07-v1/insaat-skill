# Çıktı Şemaları

## Tasarım Brief JSON

```json
{
  "project_type": "mixed_use",
  "site": {
    "area_m2": 5000,
    "width_m": 80,
    "depth_m": 62.5,
    "north": "street side",
    "setbacks_m": {"front": 5, "side": 3, "rear": 5}
  },
  "program": {
    "target_gfa_m2": 7500,
    "floors": 5,
    "uses": ["retail", "office"]
  },
  "goals": ["daylight", "cost_efficiency", "clear_public_entry"],
  "constraints": ["concept_only", "zoning_not_verified"]
}
```

## Alternatif JSON

```json
{
  "options": [
    {
      "id": "OPT-01",
      "name": "Compact Block",
      "concept": "Kompakt, ekonomik ve hızlı uygulanabilir kütle.",
      "metrics": {
        "footprint_area_m2": 1500,
        "gross_floor_area_m2": 7500,
        "coverage_ratio": 0.3,
        "floor_area_ratio": 1.5,
        "open_space_ratio": 0.7
      },
      "strengths": ["ekonomik taşıyıcı düzen", "basit sirkülasyon"],
      "risks": ["tekdüze cephe", "gün ışığı derin planlarda zayıflayabilir"],
      "next_skill": "blender-3d-modelleme-ve-render"
    }
  ]
}
```

## Karar Matrisi JSON

```json
{
  "weights": {
    "program_fit": 0.3,
    "site_response": 0.2,
    "daylight_potential": 0.2,
    "cost_simplicity": 0.2,
    "flexibility": 0.1
  },
  "ranking": [
    {
      "id": "OPT-01",
      "score": 7.8,
      "decision_note": "İlk modelleme için güçlü aday."
    }
  ]
}
```
