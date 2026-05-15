---
name: saha-fotograf-ve-kanit-analizi
description: İnşaat saha fotoğrafları, video kareleri ve görsel kanıtlar için EXIF/metadata, hash, OCR, mahal/konum, ilerleme, kalite, İSG, uygunsuzluk, önce-sonra karşılaştırma, drone görselleri ve kanıt register analizi hazırlamak için kullanılır.
---

# Saha Fotoğraf ve Kanıt Analizi

## Ne Zaman Kullanılır

- Kullanıcı saha fotoğrafları, drone görselleri, ekran görüntüleri, video kareleri veya görsel kanıtları sınıflandırmak, kayıt altına almak veya raporlamak istediğinde.
- Fotoğraflardan proje, mahal, tarih, EXIF, GPS, dosya hash'i, OCR metni, kalite/İSG/ilerleme bulgusu veya kanıt eksikliği çıkarılacağında.
- Önce-sonra, planlanan-gerçekleşen, imalat ilerleme, hasar/uygunsuzluk, teslim/kapatma kanıtı veya taşeron performansı görsel olarak değerlendirileceğinde.
- Kanıt paketinin bütünlük, tekrar/duplicate, metadata eksikliği, zincirleme kayıt, gizlilik ve onay riskleri kontrol edileceğinde.
- CVAT, Label Studio, FiftyOne, OpenCV, ExifTool, Tesseract, ImageHash, OpenDroneMap veya QGIS gibi açık araçlar için rota seçileceğinde.

Bu skill fotoğraftan kesin kusur, kesin uygunluk, hukuki delil geçerliliği veya kişi kimliği tespiti üretmez. Görsel analiz bulguları saha yetkilisi, teknik ekip, İSG uzmanı veya hukuki yetkili tarafından doğrulanmalıdır.

## Girdi

- Görseller: JPG, JPEG, PNG, TIFF, HEIC/HEIF, WebP, drone fotoğrafları, video kareleri, ekran görüntüleri.
- Bağlam: proje, tarih, mahal, kat, blok, disiplin, iş kalemi, taşeron, çekim amacı, ilgili RFI/NCR/submittal/iş emri.
- Kanıt bilgisi: çeken kişi/ekip, kaynak cihaz, teslim alan, saklama yolu, dosya hash'i, revizyon, ilişkilendirilen gereksinim veya aksiyon.
- Analiz hedefi: ilerleme takibi, kalite kontrol, İSG kanıtı, uygunsuzluk, hasar, teslim/kapanış, drone haritalama, OCR, duplicate kontrol.
- Teslim formatı: JSON/CSV kanıt register, Markdown rapor, aksiyon listesi, fotoğraf indeks tablosu, QA bayrakları veya iletişim eki.

## Araç Stratejisi

| Durum | İlk tercih | İkinci tercih | Not |
|---|---|---|---|
| Kanıt register üretimi | `build_photo_evidence_register.py` | ExifTool | SHA256, dosya boyutu, EXIF, boyut ve temel metadata çıkarır. |
| Kanıt paketi doğrulama | `validate_photo_evidence_register.py` | Frictionless / Great Expectations | Eksik hash, tarih, mahal, proje, tekrar ve hassas veri bayrakları. |
| EXIF/metadata | ExifTool | Pillow / exifread | Orijinal dosyada metadata korunur; kopyada metadata kaybolabilir. |
| OCR | Tesseract | PaddleOCR / manuel okuma | Levha, form, pano, tarih veya çizim numarası okumak için. |
| Görsel işleme | OpenCV | scikit-image / Pillow | Keskinlik, boyut, benzerlik, crop, anotasyon ve kalite ön kontrolü. |
| Duplicate / near-duplicate | ImageHash | SHA256 + dosya adı | Aynı dosya ile benzer görüntü ayrı değerlendirilir. |
| Etiketleme / anotasyon | CVAT / Label Studio | FiftyOne | İnsan doğrulamalı kusur, risk, mahal ve nesne etiketleme. |
| Dataset QA | FiftyOne | CSV/JSON register | Büyük görsel setlerde filtreleme, data quality ve model/etiket inceleme. |
| Drone / haritalama | OpenDroneMap / WebODM | QGIS | Ortomozaik, nokta bulutu, 3D model, georeferans ve saha haritası için. |
| GIS / konum | QGIS | GeoJSON/CSV | GPS'li fotoğraf ve mahal koordinatlarını harita katmanına bağlamak için. |

## İş Akışı

1. Kapsamı belirle: ilerleme, kalite, İSG, uygunsuzluk, teslim kanıtı, drone haritalama, OCR veya claim/support paketi.
2. Orijinal dosyaları koru: dosya kopyası üzerinde çalış; orijinal dosya adı, yol, boyut, SHA256 ve alınma tarihini kaydet.
3. Metadata çıkar: EXIF tarih, cihaz, GPS, yön, boyut, renk modu ve varsa açıklama alanlarını kayda al.
4. Bağlamla eşleştir: proje, mahal, iş kalemi, taşeron, ilgili RFI/NCR/submittal/iş emri ve aksiyon id'si.
5. Görsel bulgu çıkar: fotoğrafta görülen imalat, risk, hasar, eksik, uygunsuzluk veya ilerleme gözlemini kanıt seviyesiyle yaz.
6. OCR ve anotasyon yap: levha/form/tarih/etiket/çizim numarası okunuyorsa OCR; kusur/risk alanları için insan doğrulamalı anotasyon öner.
7. Kanıt kalitesini değerlendir: bulanıklık, düşük çözünürlük, metadata eksikliği, duplicate, bağlam eksikliği, gizlilik ve zincirleme kayıt risklerini bayrakla.
8. Raporla ve sınırla: "fotoğrafta görülen bulgu" dili kullan; kesin uygunluk, kusur, kimlik veya hukuki delil geçerliliği iddiası kurma.

## Çıktı Formatı

```markdown
## Fotoğraf / Kanıt Analiz Özeti

## Kanıt Register

## Metadata ve Bütünlük Kontrolü

## Görsel Bulgular

## OCR / Okunan Metinler

## Kalite, İSG, İlerleme veya Uygunsuzluk Bulguları

## Eksik Kanıt ve Risk Bayrakları

## Aksiyon ve Takip Önerisi

## Onay Sınırı
```

Makine çıktısı için `references/cikti-semalari.md` içindeki JSON şemalarını kullan.

## Kalite Kapısı

- Orijinal dosyaya müdahale edilmeden SHA256 hash ve dosya yolu kayıtlanmalıdır.
- EXIF/GPS yoksa fotoğraf geçersiz sayılmaz; ancak tarih/konum kanıt seviyesi düşürülür.
- Fotoğraftaki kişi, yüz, plaka, özel alan, GPS veya hassas veri varsa gizlilik kontrolü gerekir.
- Bir fotoğrafla kesin kusur/uygunluk hükmü verilmez; bağlam, şartname, saha teyidi ve yetkili onay gerekir.
- Duplicate ve near-duplicate fotoğraflar ilerleme/kanıt sayısını şişirmemelidir.
- OCR sonucu ham metin olarak işaretlenir; kritik bilgi manuel doğrulanmalıdır.
- Drone/harita çıktıları koordinat sistemi, uçuş tarihi ve işleme ayarları olmadan teknik kanıt sayılmaz.

## Referanslar

- Açık kaynak araştırması: `references/acik-kaynak-arastirma.md`
- Araç seçim matrisi: `references/arac-secim-matrisi.md`
- Fotoğraf kanıt iş akışı: `references/fotograf-kanit-is-akisi.md`
- Metadata ve bütünlük kuralları: `references/metadata-ve-butunluk-kurallari.md`
- Görsel analiz ve anotasyon kuralları: `references/gorsel-analiz-ve-anotasyon-kurallari.md`
- Gizlilik ve kanıt sınırları: `references/gizlilik-ve-kanit-sinirlari.md`
- Çıktı şemaları: `references/cikti-semalari.md`

## Yardımcı Scriptler

- `scripts/check_photo_evidence_tools.py`: görsel işleme, metadata, OCR, anotasyon ve GIS araçlarının durumunu raporlar.
- `scripts/plan_photo_evidence_route.py`: iş tipine göre araç rotası, QA kapıları ve çıktı seti üretir.
- `scripts/build_photo_evidence_register.py`: klasördeki görsellerden hash/metadata tabanlı kanıt register üretir.
- `scripts/validate_photo_evidence_register.py`: kanıt register'ında eksik alan, duplicate, dosya yokluğu ve gizlilik risklerini denetler.
