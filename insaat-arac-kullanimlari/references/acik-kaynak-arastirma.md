# Açık Kaynak Araştırması

Bu referans `insaat-arac-kullanimlari` skill'i için GitHub'da doğrulanan açık kaynak örneklerinden hibrit araç seçimini özetler.

## Belge ve PDF

| Araç | GitHub | Ne için kullanılır | Not |
|---|---|---|---|
| MarkItDown | https://github.com/microsoft/markitdown | PDF, Office, görsel, HTML, CSV/JSON/XML ve arşivleri Markdown'a çevirmek | Hızlı LLM ön işleme için iyi; yüksek sadakatli insan dokümanı üretimi için tek başına yeterli sayılmamalı. |
| Docling | https://github.com/docling-project/docling | PDF/DOCX/PPTX/XLSX/HTML/görsel parse, layout, okuma sırası, tablo yapısı, OCR | Karmaşık sayfa düzeni, OCR ve tablo yapısı için güçlü ana seçenek. |
| PyMuPDF | https://github.com/pymupdf/PyMuPDF | PDF metni, sayfa render, görüntü çıkarımı, layout detayları | Hızlı sayfa render ve düşük seviye PDF kontrolü için kullan. Lisans etkisini ayrıca kontrol et. |
| pdfplumber | https://github.com/jsvine/pdfplumber | Makine üretimi PDF'lerde karakter, çizgi, dikdörtgen ve tablo çıkarımı | Metraj/teklif tablolarında crop ve görsel debugging ile iyi çalışır; OCR için ana araç değildir. |

## Tablo ve Excel

| Araç | GitHub | Ne için kullanılır | Not |
|---|---|---|---|
| pandas | https://github.com/pandas-dev/pandas | CSV/Excel okuma, temizleme, birleştirme, normalizasyon | Tablo standardizasyonunun ana motoru. |
| xlwings | https://github.com/xlwings/xlwings | Excel ile Python arasında canlı bağlantı | Kullanıcı gerçek Excel uygulamasıyla çalışmak isterse faydalı; rutin batch işte pandas daha sade. |
| openpyxl | https://foss.heptapod.net/openpyxl/openpyxl | XLSX/XLSM okuma-yazma, sheet/hücre/formül ayrımı | GitHub aynaları var; resmi geliştirme deposu Heptapod tarafındadır. |

## CAD / DWG / DXF

| Araç | GitHub | Ne için kullanılır | Not |
|---|---|---|---|
| ezdxf | https://github.com/mozman/ezdxf | DXF dosyası okuma, yazma, layer/entity/block analizi | DXF için ilk tercih. DWG değil, DXF merkezli düşün. |
| LibreDWG | https://github.com/LibreDWG/libredwg | DWG okuma/yazma ve DWG araçları | DWG proprietary olduğu için dönüşüm sonrası QA şart. Lisans GPL-3.0. |
| FreeCAD | https://github.com/FreeCAD/FreeCAD | Parametrik CAD, 2D/3D, mimari/engineering kullanım, Python API | CAD/BIM/STEP/IFC gibi daha geniş dönüşüm ve görsel kontrol için değerli. |

## BIM / IFC

| Araç | GitHub | Ne için kullanılır | Not |
|---|---|---|---|
| IfcOpenShell | https://github.com/IfcOpenShell/IfcOpenShell | IFC parse, geometry, model elemanı ve BIM veri çıkarımı | IFC için ana açık kaynak omurga. Bonsai Blender eklentisiyle birlikte değerlendirilebilir. |

## Görsel

| Araç | GitHub | Ne için kullanılır | Not |
|---|---|---|---|
| OpenCV | https://github.com/opencv/opencv | Görsel ön işleme, kırpma, kontrast, kenar/çizgi, kalite kontrol | Saha fotoğrafı veya taranmış doküman OCR öncesi iyileştirme için. |

## Hibrit Sonuç

Tek araç seçmek yerine şu yaklaşım en sağlamıdır:

1. Envanter ve güvenlik kontrolü standart Python ile yapılır.
2. Belge Markdown ön okuması için MarkItDown kullanılır.
3. Karmaşık PDF, tablo ve OCR için Docling devreye alınır.
4. Hassas PDF sayfası ve render için PyMuPDF kullanılır.
5. Tablo doğrulama ve görsel PDF debugging için pdfplumber kullanılır.
6. Tablo normalizasyonu pandas ile yapılır.
7. DXF için ezdxf, DWG için LibreDWG/FreeCAD dönüşüm hattı kullanılır.
8. IFC/BIM için IfcOpenShell kullanılır.
9. Görsel kalitesi ve ön işleme için OpenCV kullanılır.

## Dikkat

- DWG dosyasında açık kaynak işleme hiçbir zaman AutoCAD ile birebir davranış garantisi vermez.
- OCR ve tablo çıkarımı kritik sayılarda ikinci kaynakla doğrulanmalıdır.
- Lisanslar müşteri paketine gömülmeden önce ayrı kontrol edilmelidir.
