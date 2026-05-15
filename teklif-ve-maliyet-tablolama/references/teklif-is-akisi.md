# Teklif İş Akışı

## 1. Kapsam

- Proje adı, disiplin, imalat paketi, mahal/kat ve revizyon.
- Teklif tipi: yaklaşık maliyet, bütçe, detaylı teklif, taşeron karşılaştırma, variation order, ihale eki.
- Fiyat geçerlilik süresi, para birimi, vergi ve kur varsayımı.

## 2. Kalem Normalizasyonu

Zorunlu alanlar:

- `code`
- `description`
- `quantity`
- `unit`
- `unit_price`
- `currency`
- `source`

Önerilen alanlar:

- `category`
- `waste_percent`
- `labor_rate`
- `material_rate`
- `equipment_rate`
- `supplier`
- `revision`
- `exclusions`
- `notes`

## 3. Hesap

1. Fireli miktar: `quantity * (1 + waste_percent / 100)`.
2. Direkt satır toplamı: `adjusted_quantity * unit_price`.
3. Direkt toplam: satır toplamları.
4. Genel gider, kar ve beklenmeyen gider direkt toplam üzerinden hesaplanır.
5. İskonto subtotal'dan düşülür.
6. KDV veya vergi son subtotal üzerinden hesaplanır.

## 4. QA

- Eksik veya sıfır miktar.
- Eksik birim.
- Sıfır veya negatif birim fiyat.
- Duplicate kod.
- Fiyat kaynağı yok.
- Yüksek fire.
- Toplam hesap farkı.
- Birden fazla para birimi.
- Güncel olmayan fiyat tarihi.

## 5. Rapor

- Toplam teklif bedeli.
- Direkt maliyet ve markup kırılımı.
- Kategori toplamları.
- En büyük maliyet kalemleri.
- Risk ve kapsam dışı işler.
- Onay sınırı.
