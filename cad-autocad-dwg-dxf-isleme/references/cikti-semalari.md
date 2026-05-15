# Çıktı Şemaları

## CAD Özet JSON

```json
{
  "source_file": "C:/project/plan.dxf",
  "working_file": "C:/project/output/plan.normalized.dxf",
  "file_type": "dxf",
  "tool_route": ["ezdxf"],
  "dxf_version": "AC1032",
  "insunits": 4,
  "layouts": ["Model", "Layout1"],
  "layers": [
    {"name": "A-WALL", "entity_count": 125, "flags": []}
  ],
  "blocks": [
    {"name": "DOOR-90", "insert_count": 12}
  ],
  "entities": {
    "LINE": 240,
    "LWPOLYLINE": 58,
    "TEXT": 33,
    "MTEXT": 14,
    "DIMENSION": 22
  },
  "texts": [
    {"text": "Salon", "layer": "A-ROOM", "layout": "Model", "insert": [10.0, 15.0, 0.0]}
  ],
  "quality_flags": ["missing_units"],
  "next_skill": "metraj-ve-mahal-kontrolu"
}
```

## Markup Tablosu

```markdown
| No | Kaynak | Layer | Konu | Risk | Aksiyon |
|---|---|---|---|---|---|
| 1 | plan.dxf / Model | A-WALL | Birim okunamadı | Metraj riski | Proje birimi teyit edilmeli |
```
