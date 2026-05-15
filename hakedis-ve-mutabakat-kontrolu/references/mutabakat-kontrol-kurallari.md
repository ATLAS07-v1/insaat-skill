# Mutabakat Kontrol Kuralları

## Eşleştirme Alanları

- Poz kodu / BOQ code.
- Fatura no.
- Ödeme referansı / dekont no.
- Cari hesap / taşeron adı.
- Dönem / hakediş no.
- Para birimi.
- Tutar ve vergi ayrımı.

## Fark Sınıfları

| Fark | Anlam |
|---|---|
| `missing_in_source_b` | Hakedişte var, karşı kaynakta yok. |
| `missing_in_source_a` | Karşı kaynakta var, hakedişte yok. |
| `quantity_mismatch` | Miktar tolerans üstü farklı. |
| `amount_mismatch` | Tutar tolerans üstü farklı. |
| `unit_price_mismatch` | Birim fiyat sözleşme/BOQ ile farklı. |
| `currency_mismatch` | Para birimi farklı. |
| `duplicate_code` | Aynı kod birden fazla satırda. |
| `over_contract_quantity` | Kümülatif miktar sözleşme miktarını aşıyor. |
| `overpayment` | Ödeme kaydı tahakkuk/fatura tutarını aşıyor. |

## Toleranslar

- Miktar farkı varsayılan: `0.0001`.
- Tutar farkı varsayılan: `0.01`.
- Para birimi farklıysa otomatik mutabık kabul edilmez; kur tarihi gerekir.
- Yuvarlama farkı ayrıca gösterilir, ana farktan saklanmaz.

## Kanıt

Her fark için şu alanlar istenir:

- Kaynak A dosya/satır.
- Kaynak B dosya/satır.
- Hesaplanan fark.
- Olası sebep.
- Gerekli aksiyon.
