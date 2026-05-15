# Açık Kaynak Araştırması

Bu skill, metraj ve mahal kontrolünü tek bir "doğru kaynak" varsayımıyla yapmaz. IFC, tablo, PDF, CAD ve manuel metraj kaynakları farklı ölçüm kuralları ve eksik alanlar taşıyabilir. Bu yüzden süreç önce kaynak QA, sonra kaynaklar arası karşılaştırma olarak kurulur.

## Ana Referanslar

| Kaynak | Rol | Skill'e Alınan İlke |
|---|---|---|
| https://github.com/IfcOpenShell/IfcOpenShell | IFC okuma, `IfcSpace`, quantity, IfcCSV, Ifc5D, IfcTester ekosistemi | IFC mahal ve quantity kontrolünde ana açık kaynak Python hattı. |
| https://docs.ifcopenshell.org/autoapi/ifccsv/index.html | IFC schedule CSV/XLSX export/import | Model property ve mahal listelerini tabloya çıkarma. |
| https://docs.ifcopenshell.org/ifc5d.html | Cost/quantity veri işleme | BOQ, QTO ve 5D quantity rotası. |
| https://github.com/datadrivenconstruction/QuantityTakeoff-Python | Revit/IFC kaynaklı quantity takeoff örneği | Filtreli metraj gruplama ve volume toplama yaklaşımı. |
| https://github.com/datadrivenconstruction/OpenConstructionERP | BOQ/CAD/BIM takeoff ve cost platformu | Metrajın BOQ ve maliyet kalemleriyle ilişkisi. |
| https://github.com/xBimTeam/XbimEssentials | .NET IFC veri kütüphanesi | `IfcSpace` raporları ve IFC schedule çıkarımı için alternatif. |
| https://docs.xbim.net/examples/excel-space-report-from-ifc.html | IFC'den Excel space report örneği | Mahal/space quantity raporlamada pratik model. |
| https://github.com/ThatOpen/engine_web-ifc | JS/WASM IFC parser | Web tabanlı IFC data extraction alternatif hattı. |
| https://github.com/pandas-dev/pandas | Tablo analizi | CSV/XLSX metraj karşılaştırma ve grup/toplam işlemleri. |
| https://github.com/jsvine/pdfplumber | PDF metin/tablo çıkarımı | Machine-generated PDF mahal listesi çıkarımı. |
| https://github.com/camelot-dev/camelot | PDF tablo extraction | Text-based PDF tablolarda accuracy/whitespace metrikleriyle QA. |
| https://github.com/rapidfuzz/RapidFuzz | Fuzzy string matching | Mahal adı/kodu farklılıklarında aday eşleşme üretimi. |

## Hibrit Sonuç

1. IFC varsa önce `IfcSpace`, storey, quantity ve property setleri kontrol edilir.
2. CSV/XLSX/PDF kaynakları normalize edilip kolon eşleştirilir.
3. Karşılaştırma önce kod, sonra ad+kat, sonra fuzzy aday eşleşme şeklinde yapılır.
4. Tolerans ve ölçüm kuralı raporlanmadan sapma yorumu yapılmaz.
5. Hakediş/ihale/teslim için sonuç uzman ve sözleşme kontrolüne gider.
