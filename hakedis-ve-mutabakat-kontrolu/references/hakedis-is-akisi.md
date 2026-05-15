# Hakediş İş Akışı

## 1. Kapsamı Belirle

- Hakediş tipi: ana sözleşme, taşeron, kesin hesap, variation, fiyat farkı veya avans kapama.
- Dönem: hakediş no, dönem başlangıç/bitiş, önceki hakediş no.
- Para birimi, KDV/vergi durumu, sözleşme revizyonu ve fiyat farkı yöntemi.

## 2. Kalemleri Normalize Et

Zorunlu kolonlar:

- `code`
- `description`
- `unit`
- `contract_quantity`
- `unit_price`
- `previous_quantity`
- `current_quantity`

Önerilen kolonlar:

- `approved_current_quantity`
- `cumulative_quantity`
- `previous_amount`
- `invoice_no`
- `payment_ref`
- `variation_ref`
- `measurement_source`
- `notes`

## 3. Hesap Mantığı

- Cari onaylı miktar yoksa cari miktar kullanılır ve `approval_missing` bayrağı verilir.
- Kümülatif miktar: önceki onaylı miktar + cari onaylı miktar.
- Cari brüt tutar: cari onaylı miktar x birim fiyat.
- Kümülatif tutar: kümülatif miktar x birim fiyat.
- Sözleşme üstü miktar varsa variation/onay bayrağı verilir.
- Kesintiler cari brüt veya kullanıcı tarafından verilen vergi matrahı üzerinden hesaplanır.

## 4. Mutabakat

- Hakediş neti ile fatura neti/tutarı karşılaştırılır.
- Fatura ile ödeme kayıtları karşılaştırılır.
- Önceki hakediş tutarı ile cari kümülatif tutar tutarlı mı kontrol edilir.
- Ödenen toplam, tahakkuk eden toplamı aşıyorsa fazla ödeme bayrağı verilir.

## 5. Rapor

- Hakediş özeti.
- Kalem bazlı cari/kümülatif tablo.
- Kesinti ve vergi tablosu.
- Fatura/ödeme mutabakatı.
- Fark listesi ve olası aksiyonlar.
- Onay sınırı.
