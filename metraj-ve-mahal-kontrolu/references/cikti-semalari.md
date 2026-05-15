# Çıktı Şemaları

## Mahal Kontrol Planı

```json
{
  "source_type": "ifc_vs_excel",
  "sources": [],
  "columns": {
    "code": "mahal_no",
    "name": "mahal_adi",
    "level": "kat",
    "area": "net_alan_m2"
  },
  "tolerances": {
    "area_m2_abs": 0.1,
    "area_percent": 1.0
  },
  "qa_gates": []
}
```

## Karşılaştırma Raporu

```json
{
  "summary": {
    "source_a_count": 10,
    "source_b_count": 10,
    "matched_count": 9,
    "issue_count": 1
  },
  "matches": [],
  "issues": [
    {
      "type": "area_delta_over_tolerance",
      "key": "Z01|101",
      "source_a_area_m2": 12.5,
      "source_b_area_m2": 13.0,
      "delta_m2": 0.5,
      "delta_percent": 4.0
    }
  ],
  "qa_flags": []
}
```

## IFC Space Kaydı

```json
{
  "global_id": "...",
  "code": "101",
  "name": "Salon",
  "long_name": "Yaşam Alanı",
  "level": "Zemin",
  "quantities": {
    "NetFloorArea": 24.5,
    "GrossVolume": 70.0
  },
  "qa_flags": []
}
```
