# Araç Seçim Matrisi

| İş | İlk tercih | Yedek | Not |
|---|---|---|---|
| Hızlı teklif tablosu | `build_cost_table.py` | spreadsheet skill | JSON/CSV çekirdeği her ortamda çalışır. |
| Detaylı BOQ | OpenConstructionERP | pandas + XlsxWriter | BOQ standardı ve validation gerekiyorsa. |
| Açık maliyet katalogu | DDC CWICR | kullanıcı fiyat listesi | Bölge, tarih ve lisans uygunluğu kontrol edilir. |
| BIM 5D | IfcOpenShell Ifc5D | BIM skill'i | IFC quantity-cost ilişkisi ayrıca doğrulanır. |
| XLSX teklif eki | XlsxWriter | openpyxl | XlsxWriter yazma/formatlama, openpyxl template düzenleme için. |
| ODS açık format | LibreOffice Calc / odfdo | CSV | Kamu/açık format ihtiyacında. |
| Tekliften ERP'ye geçiş | ERPNext | CSV import | Quotation, item, supplier, purchase ve project costing. |
| Gerçekleşen bütçe takibi | OpenProject | ERPNext | Budget, cost report, time ve unit cost. |
| Muhasebe | GnuCash | ERP muhasebe | Teklif değil muhasebe kayıt katmanıdır. |
| PDF teklif/metraj çıkarımı | pypdf/pdfplumber | OCR + manuel QA | Tarama PDF düşük güvenlidir. |

## Seçim Kuralları

- Kullanıcı sadece kalem ve fiyat verdiyse stdlib JSON/CSV hesap motoru yeterlidir.
- Profesyonel teslim eki isteniyorsa XLSX/ODS rotası açılır; formül çıktılarına ayrıca tekrar hesap QA uygulanır.
- Güncel piyasa fiyatı isteniyorsa canlı araştırma ve tarih/kaynak etiketi zorunludur.
- Taşeron teklifleri kapsam eşitlemesi yapılmadan sıralanmaz.
- BIM metrajı varsa quantity doğruluğu önce `metraj-ve-mahal-kontrolu` veya `bim-revit-ifc-model-kontrolu` ile kontrol edilir.
