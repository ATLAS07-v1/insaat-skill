# Araç Seçim Matrisi

| İhtiyaç | İlk tercih | İkinci tercih | QA odağı |
|---|---|---|---|
| IFC mahal listesi | IfcOpenShell | xBIM / web-ifc | `IfcSpace`, storey, BaseQuantities |
| IFC schedule export | IfcCSV | pandas | kolon, GlobalId, quantity adları |
| IFC 5D/metraj | Ifc5D | QuantityTakeoff-Python | cost item ve quantity eşleşmesi |
| CSV/XLSX karşılaştırma | pandas/openpyxl | stdlib CSV | kolon eşleştirme, toplamlar |
| PDF mahal tablosu | pdfplumber | Camelot | text-based PDF, extraction accuracy |
| Mahal adı fuzzy eşleşme | RapidFuzz | difflib | düşük güvenli eşleşme bayrağı |
| CAD alan listesi | CAD skill'i | DXF parser | layer, closed polyline, scale |
| Hesap doğrulama | insaat-hesaplamalar | spreadsheet skill | formül, birim, fire, boşluk |

## Varsayılan Rota

1. Kaynakları manifestle.
2. Kolonları ve birimleri normalize et.
3. Tek kaynak QA çalıştır.
4. Kaynaklar arası eşleştirme ve sapma çıkar.
5. Kritik farkları raporla ve sonraki skill'i öner.
