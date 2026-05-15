# IFC Model Kontrol Listesi

## Header ve Şema

- IFC schema: IFC2x3, IFC4, IFC4x3.
- Authoring tool ve export zamanı.
- Unit assignment.
- Georeferencing / coordinate reference.

## Proje Hiyerarşisi

- IfcProject
- IfcSite
- IfcBuilding
- IfcBuildingStorey
- IfcSpace

## Eleman Grupları

| Grup | IFC sınıfları | Kontrol |
|---|---|---|
| Mimari | IfcWall, IfcSlab, IfcRoof, IfcDoor, IfcWindow, IfcStair | Kat/mahal ilişkisi, type, material, quantity |
| Statik | IfcBeam, IfcColumn, IfcFooting, IfcPile, IfcMember | Type, load-bearing, material, storey |
| MEP | IfcFlowSegment, IfcFlowTerminal, IfcDistributionElement | Sistem, bağlantı, type, discipline |
| Mahal | IfcSpace, IfcZone | Name, number, area, storey |
| Tip | IfcTypeObject ve alt tipler | Occurrence-type ilişkisi |

## Property / Quantity

- Pset_* varlığı.
- Qto_* varlığı.
- Net/Gross area/volume/length değerleri.
- Material ilişkisi.
- Classification / Omniclass / Uniclass vb.
- FireRating, IsExternal, LoadBearing gibi kritik property'ler.

## Kalite Bayrakları

- `missing_units`
- `missing_storeys`
- `missing_spaces`
- `elements_without_container`
- `elements_without_type`
- `elements_without_material`
- `missing_quantities`
- `missing_classification`
- `georeferencing_missing`
- `revit_export_settings_unknown`
- `geometry_not_checked`
