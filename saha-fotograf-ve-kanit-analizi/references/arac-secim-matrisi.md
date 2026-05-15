# Araç Seçim Matrisi

## İş Tipine Göre Rota

| İş tipi | Veri | Ana araç | Destek araç | Çıktı |
|---|---|---|---|---|
| Fotoğraf kanıt register | klasör, görseller | `build_photo_evidence_register.py` | ExifTool | JSON/CSV register, SHA256, metadata |
| Kanıt paketi doğrulama | register | `validate_photo_evidence_register.py` | Frictionless / GX | eksik alan, duplicate, gizlilik bayrağı |
| İlerleme fotoğrafı | önce/sonra, tarih, mahal | register + manuel analiz | OpenCV / ImageHash | ilerleme bulgusu, eksik kanıt |
| Kalite/uygunsuzluk | hasar/kusur fotoğrafı | CVAT / Label Studio | OpenCV | anotasyon, NCR eki, aksiyon |
| İSG kanıtı | risk, bariyer, izin, KKD | risk skill'i + foto register | OCR / CVAT | İSG kanıt matrisi |
| OCR | pano, form, levha, etiket | Tesseract | OpenCV preprocessing | okunan metin, güven notu |
| Duplicate kontrol | çok fotoğraf | ImageHash + SHA256 | FiftyOne | aynı/benzer foto listesi |
| Drone haritalama | drone foto seti | OpenDroneMap / WebODM | QGIS | ortomozaik, nokta bulutu, 3D model |
| Konum analizi | GPS/mahal | QGIS | GeoJSON/CSV | harita katmanı, lokasyon raporu |
| Büyük dataset QA | yüzlerce/binlerce görsel | FiftyOne | CVAT | filtreleme, kalite, etiket QA |

## Seçim Kuralları

- Orijinal dosya değiştirilmeyecekse önce SHA256 ve dosya bilgisi alınır.
- EXIF kritikse ExifTool tercih edilir; Python fallback sadece temel metadata içindir.
- OCR sonucu karar için yeterli değilse ham okuma olarak kalır ve manuel teyit istenir.
- Kusur/risk alanı koordinatlı gösterilecekse CVAT/Label Studio anotasyonu önerilir.
- Drone görselleri tek tek fotoğraf olarak değil, uçuş/işleme paketi olarak değerlendirilir.
- GPS bilgisi hassas olabileceği için paylaşım öncesi gizlilik kontrolü yapılır.
