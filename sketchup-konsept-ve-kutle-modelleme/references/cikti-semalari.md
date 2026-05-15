# Çıktı Şemaları

## SketchUp İş Planı

```json
{
  "job_type": "site_massing",
  "inputs": [],
  "assumptions": [],
  "route": ["brief", "ruby_api_script", "manual_review"],
  "model_organization": {
    "tags": [],
    "materials": [],
    "groups": []
  },
  "scenes": [],
  "exports": [],
  "qa_flags": []
}
```

## Kütle Spec

```json
{
  "units": "m",
  "site": {"width": 30, "depth": 40},
  "building": {"width": 14, "depth": 18, "floors": 4, "floor_height": 3.2},
  "setbacks": {"front": 5, "rear": 4, "left": 3, "right": 3},
  "materials": {"site": "matte gray", "building": "warm concrete", "glass": "blue glass"},
  "scenes": ["site", "perspective", "front_elevation"]
}
```
