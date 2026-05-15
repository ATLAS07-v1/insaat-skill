# Açık Kaynak Araştırması

Bu skill için açık kaynak referansları, inşaat malzemesi satın alma kararını sadece fiyat tablosu değil; teknik uygunluk, tedarik riski, stok, termin, sertifika ve veri kalitesi üzerinden yönetmek için seçildi.

## Çekirdek Referanslar

| Referans | Kullanım | Hibrit yaklaşımdaki rol |
|---|---|---|
| ERPNext Procurement | Material Request, RFQ, Supplier Quotation, Purchase Order, Receipt ve Payment | Tedarik sürecinin uçtan uca açık ERP referansı. |
| OpenBoxes | Stok, lot, expiry, depo, sevkiyat ve supply chain izleme | Malzeme teslim/lot/stok riskleri için. |
| Dolibarr | Tedarikçi, sipariş, fatura, stok ve KOBİ ERP akışı | Daha hafif ERP alternatifi. |
| Odoo Community | Purchase, Inventory ve ürün/tedarikçi akışları | Açık kaynak ERP alternatifi; Community/Enterprise ayrımı kontrol edilir. |
| Akeneo PIM Community | Ürün attribute, datasheet ve ürün bilgi tek kaynağı | Malzeme teknik verisinin normalize edilmesi. |
| OpenPIM | Açık kaynak ürün bilgi yönetimi | Akeneo alternatifi PIM rotası. |
| OpenRefine | Veri temizleme, reconciliation, entity matching | Ürün adı, marka/model ve tedarikçi eşleştirme. |
| Frictionless | CSV/table schema validation | Tedarikçi teklif tabloları ve ürün attribute şeması kontrolü. |
| OCDS / OpenProcurement | Tender, award, contract ve supplier veri yapısı | Kamu/ihale veri modeli ve şeffaf tedarik referansı. |
| pandas / XlsxWriter / openpyxl | Tablo işleme, raporlama ve teklif matrisi | Deterministik karşılaştırma ve çıktı. |

## Hibrit Çalışma

1. İhtiyaç listesi ve şartname kriterleri JSON/CSV çekirdeğine normalize edilir.
2. Tedarikçi teklifleri aynı birim, para birimi, fiyat geçerlilik tarihi ve teslim koşulu üzerinden hizalanır.
3. Malzeme datasheet/sertifika bilgisi teknik kriterlerle eşleştirilir; eksikler kritik bayraklanır.
4. Fiyat, termin, stok, garanti, ödeme ve teknik uygunluk skorları ayrı hesaplanır.
5. En ucuz, en hızlı, teknik olarak en uyumlu ve dengeli seçenek ayrı raporlanır.
6. ERP/PIM/stock sistemi varsa ERPNext/OpenBoxes/Akeneo/OpenPIM rotasına aktarım alanları önerilir.
7. Satın alma, teknik onay ve sözleşme kararı kullanıcı/şirket yetkilisi onayına bırakılır.

## Kaynak Linkleri

- ERPNext GitHub: https://github.com/frappe/erpnext
- ERPNext Procurement: https://frappe.io/erpnext/open-source-procurement
- OpenBoxes GitHub: https://github.com/openboxes/openboxes
- OpenBoxes: https://openboxes.com/
- Dolibarr GitHub: https://github.com/Dolibarr/dolibarr
- Odoo GitHub: https://github.com/odoo/odoo
- Akeneo PIM Community Edition: https://www.akeneo.com/akeneo-pim-community-edition/
- OpenPIM: https://www.openpim.org/index.html
- OpenRefine reconciliation: https://openrefine.org/docs/manual/reconciling
- Frictionless validation: https://framework.frictionlessdata.io/docs/guides/validating-data.html
- OpenProcurement OCDS: https://openprocurement.io/en/ocds
- Open Contracting GitHub: https://github.com/open-contracting
