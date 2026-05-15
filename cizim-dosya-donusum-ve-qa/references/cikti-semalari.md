# Çıktı Şemaları

## Dönüşüm Planı

```json
{
  "job_type": "dwg_to_dxf",
  "inputs": [],
  "target_format": "dxf",
  "recommended_route": [],
  "commands_to_review": [],
  "preflight_flags": [],
  "post_conversion_qa": []
}
```

## Dosya Manifesti

```json
{
  "files": [
    {
      "path": "input.dxf",
      "extension": ".dxf",
      "size_bytes": 1000,
      "sha256": "...",
      "detected_kind": "cad_dxf",
      "magic": "text",
      "qa_flags": []
    }
  ],
  "summary": {
    "file_count": 1,
    "risk_count": 0,
    "kinds": {"cad_dxf": 1}
  }
}
```

## Dönüşüm QA Raporu

```json
{
  "source": "input.ifc",
  "output": "output.glb",
  "checks": {
    "output_exists": true,
    "output_nonzero": true,
    "scale_checked": false,
    "geometry_checked": false,
    "validator_checked": false
  },
  "qa_flags": ["scale_not_verified"]
}
```
