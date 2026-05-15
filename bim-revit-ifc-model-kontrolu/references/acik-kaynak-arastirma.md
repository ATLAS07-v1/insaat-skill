# Açık Kaynak Araştırması

Bu skill Revit/IFC/BIM modellerinde açık kaynak araçların en güçlü kullanımını hibrit şekilde toplar.

## Ana Araçlar

| Araç | Kaynak | Kullanım | Not |
|---|---|---|---|
| IfcOpenShell | https://github.com/IfcOpenShell/IfcOpenShell | IFC parse, C++/Python API, geometry, IfcConvert, BCF, IDS, Bonsai ekosistemi | Python IFC veri çıkarımı için ana omurga. |
| Bonsai | https://github.com/IfcOpenShell/IfcOpenShell/tree/v0.8.0/src/bonsai | Blender içinde native IFC authoring/görsel kontrol | Görsel QA ve model keşfi için iyi. |
| Autodesk revit-ifc | https://github.com/Autodesk/revit-ifc | Revit IFC export/link UI ve açık kaynak IFC export kodu | Revit'ten IFC almak için en doğru referans. Revit gerekir. |
| pyRevit | https://github.com/pyrevitlabs/pyRevit | Revit içinde Python/C#/VB.NET ile otomasyon ve eklenti geliştirme | Revit kuruluysa export/parametre kontrol otomasyonu için. |
| RevitPythonShell | https://github.com/architecture-building-systems/revitpythonshell | Revit içinde IronPython scripting | Daha düşük seviye Revit script alternatifi. |
| xBIM Toolkit | https://github.com/xBimTeam/XbimEssentials | .NET IFC veri modeli, geometry, viewer örnekleri | .NET hattı veya Windows enterprise entegrasyonu için güçlü. |
| web-ifc | https://github.com/ThatOpen/engine_web-ifc | JavaScript/WASM ile hızlı IFC okuma-yazma | Web uygulaması ve viewer entegrasyonu için. |
| xeokit | https://github.com/xeokit/xeokit-sdk | WebGL BIM/AEC viewer SDK | IFC modellerini webde yüksek performanslı göstermek için. |
| FreeCAD | https://github.com/FreeCAD/FreeCAD | IFC import/export, Python API, görsel model kontrolü | Açık kaynak CAD/BIM doğrulama ve dönüşüm destek aracı. |
| BIMserver | https://github.com/opensourceBIM/BIMserver | IFC model server, model checking, versioning | Proje ölçeğinde model yönetimi için ikinci faz. |
| Speckle | https://github.com/specklesystems | AEC object graph, Revit/Blender/AutoCAD connector ekosistemi | File-only akıştan veri platformuna geçilecekse değerlendirilir. |

## En İyi Hibrit Kullanım

1. Revit kaynak model varsa önce IFC export ayarları standardize edilir.
2. IFC dosyası IfcOpenShell ile hızlı veri envanterine alınır.
3. Property/quantity eksikleri raporlanır.
4. Geometry veya görsel kontrol gerekiyorsa Bonsai/FreeCAD/xeokit kullanılır.
5. Teslim gereksinimi varsa IfcTester/IDS doğrulaması eklenir.
6. Revit ortamı varsa pyRevit/RevitPythonShell yalnızca kontrollü otomasyon için devreye alınır.

## Kritik Gerçek

- `.rvt` kapalı/proprietary bir formattır; açık kaynakla doğrudan güvenilir şekilde okunacak ana format değildir.
- Açık BIM hattında gerçek taşınabilir kaynak IFC'dir.
- Revit IFC export kalitesi modelleme disiplini, export ayarları, property mapping ve classification durumuna bağlıdır.
