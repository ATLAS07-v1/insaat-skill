# Metadata ve Bütünlük Kuralları

## Zorunlu Minimum

- Dosya yolu veya kaynak referansı
- SHA256 hash
- Dosya boyutu
- Dosya adı
- Kayıt oluşturma zamanı
- Proje veya bağlam id'si
- Kanıt amacı

## EXIF Alanları

Öncelikli EXIF alanları:

- çekim tarihi,
- cihaz/telefon/kamera,
- GPS koordinatı,
- yön/orientation,
- genişlik/yükseklik,
- lens ve odak bilgisi,
- açıklama/yorum alanı.

## Bütünlük Bayrakları

- `missing_sha256`: hash yok.
- `file_missing`: register dosya yolunu gösteriyor ama dosya yok.
- `duplicate_sha256`: aynı dosya birden fazla kayıtlı.
- `missing_capture_date`: çekim tarihi yok.
- `missing_context`: proje/mahal/konu eksik.
- `gps_present`: paylaşım öncesi gizlilik kontrolü gerekir.
- `metadata_absent`: EXIF yok veya okunamadı.
- `low_resolution`: düşük çözünürlük.
- `screenshot_or_export`: ekran görüntüsü veya export olma ihtimali.

## Orijinal Dosya İlkesi

- Orijinal dosya üzerinde resize, crop, renk düzeltme veya metadata temizleme yapılmaz.
- İşleme yapılacaksa kopya dosya kullanılır ve kopyanın hash'i ayrıca alınır.
- Orijinal ve işlenmiş dosya ilişkisi register'da tutulur.
