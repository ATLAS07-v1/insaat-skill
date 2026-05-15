# Araç Seçim Matrisi

| İhtiyaç | Araç | Gerekçe | Çıktı |
|---|---|---|---|
| Ölçülü oda/kütle modeli | Blender Python `bpy` | Deterministik, tekrar üretilebilir | `.blend`, PNG, GLB |
| Çoklu render pipeline | BlenderProc | Kamera/ışık/materyal ve veri çıktıları için | RGB/depth/normal/segmentation |
| IFC model görselleştirme | Bonsai / IfcOpenShell | Native IFC ve BIM property bağlantısı | BIM görsel QA |
| DXF planı 3D anlatıma çevirme | CAD skill + Blender import/script | DXF önce temizlenmeli | 3D kütle/model |
| Parametrik tasarım | Sverchok | Node tabanlı mimari geometri | Parametrik model |
| Hızlı bina kütlesi | Building Tools | Floor/roof/stair gibi hazır yapı parçaları | Konsept bina modeli |
| Arazi ve kent bağlamı | BlenderGIS | OSM/DEM/georeference | Arazi/kentsel sahne |
| Asset ve materyal | BlenderKit / yerel kütüphane | Hızlı sunum kalitesi | Mobilya, materyal, HDRI |

## Karar Ağacı

1. Ölçülü ve tekrar üretilebilir çıktı mı?
   - Evet: `bpy` script üret.
2. Render otomasyonu ve çoklu veri çıktısı mı?
   - Evet: BlenderProc planla.
3. BIM/IFC kaynak mı?
   - Evet: Bonsai/IfcOpenShell kullan; önce BIM skill raporunu iste.
4. CAD/DXF kaynak mı?
   - Evet: önce CAD skill ile temiz DXF/ölçü çıkar.
5. Arazi/kent bağlamı mı?
   - Evet: BlenderGIS rotası kur.
6. Sadece konsept render mı?
   - Temsili model + materyal + ışık + kamera QA yeterlidir.
