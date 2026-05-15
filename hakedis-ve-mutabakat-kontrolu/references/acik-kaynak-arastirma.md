# Açık Kaynak Araştırması

Bu skill için referanslar, hakedişi yalnız bir ödeme tablosu olarak değil; sözleşme, metraj, fatura, ödeme, kesinti ve denetlenebilir mutabakat kanıtı olarak ele almak için seçildi.

## Çekirdek Referanslar

| Referans | Kullanım | Hibrit yaklaşımdaki rol |
|---|---|---|
| OpenConstructionERP | BOQ, 4D/5D, cost item, CAD/BIM takeoff ve validation | Hakedişin sözleşme/BOQ ve proje maliyet katmanı. |
| IfcOpenShell Ifc5D | IFC cost item, quantity ve 5D cost report | BIM quantity ile hakediş/metraj ilişkisini kurar. |
| OpenProject | Time/cost report, unit cost, budget ve Excel export | Gerçekleşen işçilik/birim maliyet ve bütçe kontrolü. |
| ERPNext | Invoice, payment, accounting, project ve supplier/customer kayıtları | Fatura/ödeme/ERP mutabakatı için ana açık ERP referansı. |
| Mint for ERPNext | ERPNext bank reconciliation eklentisi | Banka/kredi kartı hareketlerini ERP kayıtlarıyla eşleştirme referansı. |
| Settler | Açık kaynak reconciliation engine | Kural tabanlı, tekrarlanabilir ve kanıt üreten mutabakat mimarisi. |
| Beancount / Ledger | Metin tabanlı çift kayıt muhasebe | Ödeme ve kesinti kayıt disiplinini açıklamak için. |
| Frictionless | CSV/table schema validation | Hakediş ve mutabakat tablolarında şema/veri kalite kontrolü. |
| Great Expectations | Veri kalite expectation yaklaşımı | Büyük hakediş/ödeme tablolarında QA beklentileri. |
| pandas / XlsxWriter / openpyxl | Tablo normalizasyonu ve raporlama | JSON/CSV/XLSX çıktı ve tekrar hesap kontrolü. |

## Hibrit Çalışma

1. Sözleşme BOQ, önceki hakediş, cari ölçüm, fatura ve ödeme kayıtları standart kolonlara normalize edilir.
2. Hakediş hesabı deterministik script ile üretilir: önceki, cari, kümülatif, kesinti, vergi ve net ödeme.
3. Mutabakat katmanı kaynaklar arası fark çıkarır: hakediş-fatura, fatura-ödeme, ERP-banka, metraj-hakediş.
4. Tablo QA katmanı eksik alan, duplicate poz, sözleşme üstü miktar, negatif tutar, ters yönde kümülatif ve ödeme fazlası bayraklar.
5. BIM/5D kaynak varsa Ifc5D ve BIM skill hattına yönlendirilir.
6. ERP/muhasebe kaynak varsa ERPNext/Mint/Beancount/Ledger mantığına göre kayıt izi istenir.
7. Sonuç teknik/ticari kontrol bulgusudur; resmi ödeme onayı veya vergi yorumu değildir.

## Kaynak Linkleri

- OpenConstructionERP: https://github.com/datadrivenconstruction/OpenConstructionERP
- IfcOpenShell Ifc5D: https://docs.ifcopenshell.org/ifc5d.html
- OpenProject time and cost reporting: https://www.openproject.org/docs/user-guide/time-and-costs/reporting/
- OpenProject GitHub: https://github.com/opf/openproject
- ERPNext: https://github.com/frappe/erpnext
- Mint for ERPNext reconciliation: https://github.com/The-Commit-Company/mint
- Settler reconciliation engine: https://www.settler.dev/
- Beancount: https://github.com/beancount/beancount/
- Ledger CLI: https://github.com/ledger/ledger
- Frictionless validation: https://framework.frictionlessdata.io/docs/guides/validating-data.html
- Great Expectations: https://github.com/great-expectations/great_expectations
- XlsxWriter: https://xlsxwriter.com/
