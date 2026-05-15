# BOQ ve Maliyet Kuralları

## Kalem Yapısı

| Alan | Açıklama |
|---|---|
| `code` | WBS/BOQ/poz kodu. Duplicate olmamalı. |
| `description` | İş kalemi açıklaması. Kapsam ve kalite belirsizse bayraklanır. |
| `category` | Kaba yapı, ince işler, mekanik, elektrik, genel gider vb. |
| `quantity` | Metraj miktarı. Kaynağı yazılmalıdır. |
| `unit` | m, m2, m3, kg, ton, adet, gün, saat vb. |
| `unit_price` | Birim fiyat. Tarih ve kaynak gerekir. |
| `waste_percent` | Fire/zayiat. İş türüne göre makul aralık kontrol edilir. |
| `source` | Metraj/fiyat kaynağı. |

## Toplam Mantığı

- Kalem düzeyinde `adjusted_quantity = quantity + fire`.
- Fire satır içine dahil ediliyorsa ayrı kolonla gösterilir.
- Genel gider, kar ve risk payı satır fiyatına gömülüyse ayrıca iki kez eklenmez.
- KDV dahil/hariç durumu açıkça işaretlenir.
- Dövizli kalemlerde kur tarihi ve kur kaynağı yazılır.

## Kapsam Dışı İşler

Teklif raporunda şu başlıklar ayrı belirtilmelidir:

- Ruhsat, harç, resmi ödeme.
- Zemin iyileştirme, beklenmeyen kazı, taşıma.
- Tasarım/proje hizmeti.
- Elektrik/su bağlantı bedelleri.
- Gece çalışma, hızlandırma, şantiye mobilizasyonu.
- Test, devreye alma, bakım ve garanti kapsamı.

## Onay Notu

Fiyatlar ve vergiler zamanla değişir. Kullanıcı canlı fiyat araştırması istemediyse veya fiyat listesi vermediyse sonuç bağlayıcı teklif değil, hesap modeli ve taslak teklif tablosudur.
