# Açık Kaynak Araştırması

Bu skill Blender tabanlı inşaat/mimari 3D üretim ve render için açık kaynak araçların en iyi hibrit kullanımını özetler.

## Ana Araçlar

| Araç | Kaynak | Kullanım | Not |
|---|---|---|---|
| Blender | https://github.com/blender/blender | 3D modelleme, render, animasyon, Python API, import/export | Ana motor. GitHub resmi mirror; asıl repo projects.blender.org tarafında. |
| Blender built-in add-ons | https://github.com/blender/blender-addons | DXF, SVG, FBX, glTF, STL, material ve ölçüm araçları | Resmi add-on mirror arşivlenmiş olabilir; yine de referans değeri yüksek. |
| BlenderProc | https://github.com/DLR-RM/BlenderProc | Procedural render pipeline, kamera/ışık/materyal otomasyonu, RGB/depth/normal/segmentation | Render otomasyonu ve sentetik görüntü üretimi için güçlü. |
| IfcOpenShell / Bonsai | https://github.com/IfcOpenShell/IfcOpenShell | IFC/BIM modelini Blender içinde açma, native IFC authoring/görsel kontrol | BIM bağlantısı için ana açık kaynak hat. |
| BlenderGIS | https://github.com/domlysz/BlenderGIS | OSM, DEM, shapefile, georeferencing, arazi ve kentsel model | Arsa, topografya ve kent bağlamı için. |
| Sverchok | https://github.com/nortikin/sverchok | Parametrik node tabanlı geometri, mimari/şekil üretimi | Visual programming ve parametrik tasarım için. |
| Building Tools | https://github.com/ranjian0/building_tools | Floorplan, floor, door, window, roof, stair, balcony üretimi | Hızlı bina kütlesi ve konsept model için. |
| BlenderKit | https://github.com/BlenderKit/blenderkit | Asset, materyal, HDRI ve sahne kütüphanesi | Lisans ve müşteri teslim hakları ayrıca kontrol edilmeli. |

## En İyi Hibrit Kullanım

1. Üretim script tabanlıysa `bpy` kullan.
2. Render pipeline çoklu kamera/ışık/veri çıktısı istiyorsa BlenderProc değerlendir.
3. BIM/IFC varsa Bonsai/IfcOpenShell ile aç veya IFC'yi önce `bim-revit-ifc-model-kontrolu` skill'inden geçir.
4. DXF/CAD varsa önce `cad-autocad-dwg-dxf-isleme` skill'iyle temizlenmiş DXF/ölçü verisi al.
5. Arsa/topografya/kent bağlamı varsa BlenderGIS kullan.
6. Parametrik tasarım arayüzü gerekiyorsa Sverchok; hızlı bina parçaları gerekiyorsa Building Tools.
7. Sunum kalitesi için kamera, ışık, materyal ve render QA kapıları zorunlu.

## Kritik Gerçekler

- Blender renderı görsel anlatım üretir; teknik uygulama projesi yerine geçmez.
- `bpy` genellikle Blender'ın kendi Python ortamında çalışır; normal Python interpreter'da `import bpy` her zaman çalışmaz.
- Asset ve materyal kaynaklarının lisansı müşteri tesliminden önce kontrol edilmelidir.
- IFC/DXF import'ta geometri ve materyal kaybı olabilir; kaynak skill'lerin QA raporu aranmalıdır.
