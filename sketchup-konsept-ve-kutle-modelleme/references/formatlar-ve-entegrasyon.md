# Formatlar ve Entegrasyon

| Format | Kullanım | Not |
|---|---|---|
| `.skp` | Ana SketchUp model dosyası | SketchUp/SDK lisansı gerekir. |
| `.rb` | Ruby API otomasyon script'i | SketchUp içinde çalışır. |
| `.dwg/.dxf` | CAD tabanlı import/export | Ölçek/layer temizliği için CAD skill'i kullan. |
| `.ifc` | BIM alışverişi | IFC karmaşıksa BIM skill'i kullan. |
| `.obj/.fbx` | Genel 3D aktarım | Malzeme/ölçek kaybı kontrol edilir. |
| `.glb/.gltf` | Web/3D paylaşım | Ruby glTF exporter veya Blender hattı. |
| `.png/.pdf` | Sunum ve müşteri iletişimi | Sahne/kamera listesi gerekir. |

## Entegrasyon Rotaları

- CAD -> SketchUp: DWG/DXF temizle, katmanları sadeleştir, SketchUp içinde import et.
- BIM -> SketchUp: IFC'den sade geometri çıkar veya Blender/BIM skill'i ile ara format üret.
- SketchUp -> Blender: SKP'den OBJ/FBX/DAE/GLB export, Blender'da render QA.
- SketchUp -> Müşteri: sahne isimleri, açıklama notları, temsili/varsayım uyarıları.
