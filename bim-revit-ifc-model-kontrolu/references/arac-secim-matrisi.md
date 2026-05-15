# Araç Seçim Matrisi

| İhtiyaç | Araç | Gerekçe | Çıktı |
|---|---|---|---|
| IFC hızlı veri özeti | IfcOpenShell Python | Python, güçlü IFC API, geniş schema desteği | JSON/Markdown model özeti |
| IFC geometry/export | IfcConvert | IfcOpenShell ekosisteminde CLI dönüşüm | OBJ/DAE/geometry çıktı |
| IFC görsel kontrol | Bonsai | Blender içinde native IFC modelleme/görüntüleme | Görsel QA notu |
| IFC alternatif .NET kontrol | xBIM | .NET enterprise ve WPF viewer örnekleri | .NET model raporu |
| Web viewer | web-ifc, xeokit | JavaScript/WASM/WebGL | Browser model kontrolü |
| Revit'ten IFC export | Autodesk revit-ifc | Revit'in açık kaynak IFC exporter kodu | Standart IFC export |
| Revit otomasyon | pyRevit | Revit API ile hızlı script/add-in üretimi | Export/parametre otomasyonu |
| Revit script shell | RevitPythonShell | IronPython shell | İnteraktif Revit API kontrolü |
| Model server | BIMserver | IFC versioning/model checking | Proje ölçeği BIM yönetimi |

## Karar Ağacı

1. Dosya `.ifc` veya `.ifczip` mi?
   - Evet: IfcOpenShell ile analiz et.
   - Hayır: 2. adıma geç.
2. Dosya `.rvt` mi?
   - Evet: Revit/Autodesk revit-ifc ile IFC export planı hazırla.
   - Hayır: `insaat-arac-kullanimlari` skill'ine geri dön.
3. Görsel doğrulama gerekiyor mu?
   - Evet: Bonsai/FreeCAD/xeokit rotası öner.
4. Teslim gereksinimi veya IDS var mı?
   - Evet: IfcTester/IDS doğrulaması planla.
