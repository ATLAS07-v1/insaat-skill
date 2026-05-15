# Açık Kaynak Araştırması

Bu skill için açık kaynak referansları, inşaat maliyetini sadece "miktar x fiyat" olarak değil; kaynak, revizyon, bölge, para birimi, markup, risk ve QA kapılarıyla izlenebilir bir teklif modeline çevirmek için seçildi.

## Çekirdek Referanslar

| Referans | Kullanım | Hibrit yaklaşımdaki rol |
|---|---|---|
| OpenConstructionERP | BOQ, CAD/BIM/PDF takeoff, maliyet veri tabanı, 4D/5D, teklif ve validation | İnşaat özelinde uçtan uca açık kaynak maliyet platformu referansı. |
| DDC CWICR | Açık inşaat iş kalemi, kaynak ve bölgesel fiyat veri tabanı | Birim fiyat eşleştirme ve cost item katalog yapısı için referans. |
| IfcOpenShell Ifc5D | IFC cost item, quantity ve cost report işlemleri | BIM metrajını 5D maliyet akışına bağlar. |
| ERPNext | Quotation, item, project, inventory, accounting ve purchasing iş akışları | Teklifin ERP/satın alma/muhasebe tarafına taşınması için. |
| OpenProject | Budget, time/cost report ve proje maliyet takibi | Teklif sonrası bütçe ve gerçekleşen maliyet takibi. |
| GnuCash | Çift taraflı muhasebe ve küçük işletme kayıtları | Teklif değil, muhasebe kayıt disiplini referansı. |
| pandas | CSV/XLSX tablo normalize etme, gruplama, toplam ve QA | Deterministik tablo çekirdeği. |
| XlsxWriter | Formatlı XLSX rapor, formül, grafik ve çıktı | Profesyonel teklif eki üretimi için. |
| openpyxl | XLSX okuma/yazma ve template doldurma | Var olan Excel teklif şablonlarıyla çalışma. |
| LibreOffice Calc / ODF / odfdo | ODS açık format ve ofis uyumluluğu | Açık doküman formatında tablo üretimi ve dönüşüm. |

## Hibrit Çalışma

1. Metraj ve kalem listesi JSON/CSV çekirdeğine normalize edilir.
2. Fiyat kaynağı açıkça etiketlenir: kullanıcı fiyatı, taşeron teklifi, açık kaynak katalog, önceki proje veya canlı araştırma.
3. Hesap motoru direkt maliyet, fire, genel gider, kar, beklenmeyen gider, iskonto ve KDV toplamını deterministik üretir.
4. QA motoru eksik birim, sıfır fiyat, duplicate kod, yüksek fire, toplam farkı ve kaynak belirsizliğini bayraklar.
5. BIM/IFC kaynağı varsa Ifc5D ve `bim-revit-ifc-model-kontrolu` skill'i ile quantity-cost bağlantısı kurulabilir.
6. Çıktı CSV/JSON/Markdown olarak güvenli çekirdekte üretilir; XLSX/ODS için pandas/XlsxWriter/openpyxl/LibreOffice rotası seçilir.
7. Bağlayıcı teklif, vergi ve güncel piyasa fiyatı kullanıcı/teknik-ticari sorumlu onayı gerektirir.

## Kaynak Linkleri

- OpenConstructionERP: https://github.com/datadrivenconstruction/OpenConstructionERP
- DDC CWICR cost database: https://github.com/datadrivenconstruction/OpenConstructionEstimate-DDC-CWICR
- IfcOpenShell Ifc5D: https://docs.ifcopenshell.org/ifc5d.html
- IfcOpenShell cost API: https://docs.ifcopenshell.org/autoapi/ifcopenshell/api/cost/index.html
- ERPNext: https://github.com/frappe/erpnext
- OpenProject: https://github.com/opf/openproject
- OpenProject time/cost/budget: https://www.openproject.org/collaboration-software-features/time-tracking/
- GnuCash: https://github.com/Gnucash/gnucash
- XlsxWriter: https://xlsxwriter.com/
- openpyxl: https://openpyxl.readthedocs.io/
- pandas: https://pandas.pydata.org/
- odfdo: https://github.com/jdum/odfdo
- Apache OpenOffice Calc: https://www.openoffice.org/product/calc.html
