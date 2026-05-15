# Çıktı Şemaları

## BIM Özet JSON

```json
{
  "source_file": "C:/project/model.ifc",
  "schema": "IFC4",
  "tool_route": ["ifcopenshell"],
  "project": {"name": "Proje", "global_id": "abc"},
  "sites": [{"name": "Site", "global_id": "def"}],
  "buildings": [{"name": "Building", "global_id": "ghi"}],
  "storeys": [{"name": "Level 01", "global_id": "jkl", "elevation": 0.0}],
  "spaces": [{"name": "Salon", "global_id": "mno", "storey": "Level 01"}],
  "entity_counts": {"IfcWall": 120, "IfcDoor": 44},
  "property_summary": {"with_psets": 300, "without_psets": 25},
  "quantity_summary": {"with_quantities": 210, "without_quantities": 115},
  "quality_flags": ["missing_classification", "geometry_not_checked"],
  "next_skill": "metraj-ve-mahal-kontrolu"
}
```

## Eksik Parametre Tablosu

```markdown
| GlobalId | Sınıf | Ad | Eksik Alan | Risk | Aksiyon |
|---|---|---|---|---|---|
| 1Abc | IfcWall | W-101 | Qto_WallBaseQuantities.NetVolume | Hakediş/metraj riski | Quantity export veya geometri hesabı kontrol edilmeli |
```
