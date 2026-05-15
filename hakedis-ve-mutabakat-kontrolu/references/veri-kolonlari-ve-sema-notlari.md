# Veri Kolonları ve Şema Notları

## Hakediş Kalemi

| Kolon | Zorunlu | Açıklama |
|---|---|---|
| `code` | Evet | Poz/BOQ/sözleşme kalemi kodu. |
| `description` | Evet | İş kalemi açıklaması. |
| `unit` | Evet | m, m2, m3, kg, adet vb. |
| `contract_quantity` | Önerilir | Sözleşme miktarı. |
| `unit_price` | Evet | Sözleşme birim fiyatı. |
| `previous_quantity` | Evet | Önceki onaylı kümülatif miktar. |
| `current_quantity` | Evet | Bu dönem bildirilen miktar. |
| `approved_current_quantity` | Önerilir | Bu dönem onaylanan miktar. |
| `cumulative_quantity` | Opsiyonel | Verilmişse script hesaplanan değerle karşılaştırır. |
| `source` | Önerilir | Metraj, fatura veya ölçüm kaynağı. |

## Fatura / Ödeme Kaydı

| Kolon | Açıklama |
|---|---|
| `document_no` | Fatura veya ödeme belge no. |
| `date` | Belge/ödeme tarihi. |
| `party` | Cari hesap / taşeron / tedarikçi. |
| `code` | İlgili poz veya paket kodu. |
| `amount` | Tutar. |
| `tax_amount` | Vergi tutarı. |
| `currency` | Para birimi. |
| `payment_ref` | Dekont veya banka referansı. |

## Normalize Etme Kuralları

- Ondalık ayracı nokta olmalıdır.
- Boş tutar `0` kabul edilmeden önce QA bayrağı alır.
- Kodlar trim edilir ve büyük/küçük harf farkı normalleştirilir.
- Aynı kod birden çok satırda ise toplamlanmadan önce duplicate olarak raporlanır.
