# Çıktı Şemaları

## Hesap Planı

```json
{
  "calculation_type": "quantity_takeoff",
  "inputs": [],
  "route": [],
  "required_assumptions": [],
  "tools": [],
  "qa_gates": []
}
```

## Temel Metraj Sonucu

```json
{
  "project": "ornek",
  "items": [
    {
      "name": "Döşeme betonu",
      "category": "concrete",
      "formula": "length * width * thickness",
      "quantity": 12.5,
      "unit": "m3",
      "assumptions": [],
      "qa_flags": []
    }
  ],
  "totals": {
    "concrete_m3": 12.5,
    "formwork_m2": 0,
    "rebar_kg": 0
  },
  "qa_flags": []
}
```

## Hesap QA Raporu

```json
{
  "checks": {
    "units_present": true,
    "positive_dimensions": true,
    "assumptions_recorded": true,
    "structural_approval_required": false
  },
  "warnings": []
}
```
