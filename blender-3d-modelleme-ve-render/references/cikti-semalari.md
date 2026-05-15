# Çıktı Şemaları

## Blender İş Planı JSON

```json
{
  "job_type": "interior_concept_render",
  "unit": "meters",
  "inputs": ["brief.md", "reference.png"],
  "tool_route": ["bpy"],
  "outputs": {
    "blend": "output/scene.blend",
    "render": "output/render.png",
    "report": "output/render_report.json"
  },
  "assumptions": ["room dimensions assumed"],
  "quality_flags": ["representational_model_only"]
}
```

## Render QA JSON

```json
{
  "scene_file": "scene.blend",
  "render_file": "render.png",
  "resolution": [1600, 1000],
  "camera": "Camera_Main",
  "materials": ["Mat_Wall_Paint", "Mat_Glass_Clear"],
  "lights": ["Sun_Main", "Area_Key"],
  "quality_flags": []
}
```
