# Açık Kaynak Araştırması

Bu skill, saha fotoğraflarını tek tek yorumlamak yerine kanıt yönetimi zinciri olarak ele alır: dosya bütünlüğü, metadata, OCR, görsel bulgu, anotasyon, konum, drone haritalama ve raporlanabilir register.

## Referans Alınan Araçlar

| Kaynak | Kullanım | Neden alındı |
|---|---|---|
| OpenCV | Görsel kalite, crop, fark, eşikleme, nesne/alan ön işleme | Büyük ve yaygın açık kaynak bilgisayarlı görü kütüphanesi. |
| ExifTool | EXIF/IPTC/XMP ve geniş dosya metadata okuma | Fotoğraf kanıtlarında tarih, cihaz, GPS ve metadata çıkarımı için en güçlü açık araçlardan biri. |
| Tesseract OCR | Fotoğraf içindeki pano, levha, form ve çizim numarası okuma | Açık kaynak OCR motoru; saha formları ve etiketler için uygun başlangıç. |
| CVAT | Görsel/video/3D anotasyon, QA ve ekip çalışması | Fotoğraftaki kusur, risk, imalat ve bölge etiketlerini insan doğrulamalı toplamak için. |
| Label Studio | Çok tipli veri etiketleme ve standart çıktı | Esnek etiketleme, human-in-the-loop kontrol ve görüntü sınıflandırma için. |
| FiftyOne | Görsel dataset curation, filtreleme ve kalite inceleme | Büyük fotoğraf setlerinde duplicate, düşük kalite ve etiket QA iş akışı için. |
| ImageHash | Perceptual hash ve near-duplicate kontrol | Aynı/benzer fotoğrafların kanıt sayısını şişirmesini önlemek için. |
| OpenDroneMap / WebODM | Drone fotoğraflarından harita, nokta bulutu, 3D model ve DEM | Şantiye ilerleme ve alan kanıtlarında drone tabanlı açık fotogrametri için. |
| QGIS | Geotag, mahal, harita katmanı ve konum analizi | Fotoğrafları konum ve proje haritasına bağlamak için. |

## Hibrit Çalışma Kararı

1. Dosya bütünlüğü ve register üretimi yerel scriptlerle yapılır.
2. Metadata için ExifTool en güçlü rota; Python scriptleri temel fallback sağlar.
3. OCR için Tesseract/PaddleOCR kullanılabilir; kritik yazılar manuel doğrulanır.
4. İnsani doğrulama gereken kusur/risk etiketleri CVAT veya Label Studio ile yapılır.
5. Büyük fotoğraf setleri FiftyOne ile filtrelenebilir ve QA edilebilir.
6. Drone görselleri OpenDroneMap/WebODM ve QGIS ile harita/konum çıktısına çevrilir.
7. Hiçbir görsel analiz tek başına kesin hukuki/teknik karar değildir; kanıt seviyesi ve onay sınırı raporda yazılır.

## Kaynak Linkleri

- OpenCV: https://opencv.org/
- ExifTool: https://exiftool.org/
- Tesseract OCR: https://github.com/tesseract-ocr/tesseract
- CVAT: https://docs.cvat.ai/docs/getting_started/overview/
- Label Studio: https://github.com/HumanSignal/label-studio
- FiftyOne: https://github.com/voxel51/fiftyone
- ImageHash: https://github.com/JohannesBuchner/imagehash
- OpenDroneMap ODM: https://github.com/OpenDroneMap/ODM
- QGIS: https://github.com/qgis/QGIS
