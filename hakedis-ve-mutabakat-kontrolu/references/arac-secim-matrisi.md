# Araç Seçim Matrisi

| İş | İlk tercih | Yedek | Not |
|---|---|---|---|
| Hakediş hesabı | `calculate_progress_payment.py` | spreadsheet skill | Önceki/cari/kümülatif ve kesinti hesabı için. |
| Kaynak mutabakatı | `compare_progress_sources.py` | pandas / RapidFuzz | Kod bazlı miktar/tutar farkı çıkarır. |
| BOQ ve 5D maliyet | OpenConstructionERP | teklif-ve-maliyet-tablolama | Sözleşme kalemi ve maliyet ilişkisi. |
| BIM quantity | IfcOpenShell Ifc5D | BIM/metraj skill'leri | Model quantity önce QA'dan geçmelidir. |
| Fatura/ödeme | ERPNext | Mint / Settler | ERP ve banka/ödeme eşleştirme. |
| Proje gerçekleşen maliyet | OpenProject | ERPNext | Time, unit cost, budget ve export. |
| Muhasebe izi | Beancount / Ledger / GnuCash | CSV ledger | Çift kayıt prensibi ve denetlenebilir kayıt. |
| Tablo şema kontrolü | Frictionless | Great Expectations | Büyük CSV/XLSX kaynaklarda. |
| XLSX/ODS çıktı | XlsxWriter / openpyxl / LibreOffice | CSV/JSON | Formül sonucu ayrıca tekrar hesaplanır. |

## Seçim Kuralları

- Hakediş hesabı için önce sözleşme kalemi ve önceki hakediş zemini doğrulanır.
- Fatura-ödeme mutabakatı için belge numarası, tarih, cari hesap ve para birimi eşleştirilir.
- BIM/metraj kaynağı varsa model quantity ile hakediş quantity aynı ölçüm kuralına göre normalize edilmelidir.
- Vergi ve kesinti kurgusu ülkeden/sözleşmeden etkilenir; varsayım olarak değil kullanıcı verisi olarak alınır.
- Ödeme farkı varsa "fark" ve "olası sebep" yazılır; ödeme talimatı verilmez.
