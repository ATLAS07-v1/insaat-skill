# Araç Seçim Matrisi

| İş | İlk tercih | Yedek | Not |
|---|---|---|---|
| RFQ / tedarik akışı | ERPNext Procurement | Dolibarr / Odoo Community | Material Request, RFQ, Supplier Quotation ve PO için. |
| Teklif karşılaştırma | `compare_supplier_quotes.py` | teklif-ve-maliyet-tablolama | Fiyat, termin, teknik uygunluk ve risk skorlaması. |
| Malzeme teknik uygunluk | `compare_material_specs.py` | teknik-sartname-ve-uygulama-kontrolu | Datasheet/sertifika/şartname karşılaştırması. |
| Stok ve lot izleme | OpenBoxes | ERPNext Stock | Expiry, lot, depo, sevkiyat ve stok riski. |
| Ürün bilgi yönetimi | Akeneo / OpenPIM | CSV attribute catalog | Marka/model, teknik attribute ve doküman merkezi. |
| Veri temizleme | OpenRefine | RapidFuzz / difflib | Ürün adı ve tedarikçi eşleştirme için. |
| Tablo doğrulama | Frictionless / Great Expectations | stdlib validator | Kolon, tip, zorunlu alan ve aralık kontrolleri. |
| Kamu ihale veri modeli | OCDS | OpenProcurement API | Tender/award/contract/supplier veri yapısı. |

## Seçim Kuralları

- Teknik kriter kritikse önce malzeme uygunluğu, sonra fiyat karşılaştırması yapılır.
- Tedarikçi teklifleri aynı teslim yeri, KDV, nakliye, ödeme ve fiyat geçerlilik koşuluna normalize edilir.
- Stok/termin kritikse OpenBoxes/ERP stok rotası seçilir.
- Ürün bilgisi çok sayıda marka/model ve datasheet içeriyorsa PIM rotası açılır.
- Veri kirliyse OpenRefine/RapidFuzz ile ad/model eşleştirme yapılmadan karar matrisi üretilmez.
