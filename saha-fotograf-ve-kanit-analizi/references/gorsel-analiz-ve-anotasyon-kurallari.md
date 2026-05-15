# Görsel Analiz ve Anotasyon Kuralları

## Analiz Dili

- "Fotoğrafta ... görülüyor" yaz.
- "Fotoğrafa göre ... olabilir" yaz.
- "Şu kanıtlarla birlikte doğrulanmalıdır" yaz.
- "Kesin kusurludur", "mevzuata aykırıdır", "tamamlanmıştır" gibi bağlayıcı dil kullanma.

## Etiket Sözlüğü

Önerilen etiketler:

- `progress_completed`
- `progress_partial`
- `quality_defect`
- `safety_risk`
- `missing_protection`
- `material_delivery`
- `installation_ready`
- `rework_needed`
- `blocked_area`
- `unknown_context`
- `privacy_sensitive`

## Anotasyon Alanları

CVAT/Label Studio gibi araçlarda her işaretleme için:

- sınıf,
- bounding box veya polygon,
- açıklama,
- güven seviyesi,
- doğrulayan kişi,
- tarih,
- ilgili aksiyon id'si

tutulmalıdır.

## Önce-Sonra Kontrol

- Aynı mahal, aynı açı ve yakın tarihli karşılaştırma tercih edilir.
- Perspektif farkı ve aydınlatma farkı bulgu güvenini düşürür.
- Sadece görsel benzerlik ilerleme yüzdesi için yeterli değildir; metraj/hakediş verisiyle bağlanmalıdır.

## OCR Kontrolü

- OCR sonucu ham veri olarak saklanır.
- Kritik tarih, tutar, belge no, imza, izin no ve revizyon manuel doğrulanır.
- Düşük ışık, eğik çekim, bulanıklık ve el yazısı OCR güvenini düşürür.
