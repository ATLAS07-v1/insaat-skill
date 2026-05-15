# Bağımlılık Matrisi

Bu repo iki seviyede çalışır:

- `core`: Manifest üretme/doğrulama, temel PDF/tablo/görsel okuma ve çoğu rota/check scripti.
- Opsiyonel gruplar: CAD, BIM, doküman, görsel/OCR ve veri kalite gibi domain işleri.

## Hızlı Kurulum

```bash
python -m venv .venv
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Tüm opsiyonel Python bağımlılıklarını kurmak için:

```bash
pip install -e ".[cad,bim,pdf-doc,spreadsheet,image-ocr,data-quality,communication]"
```

## Python Grupları

| Grup | Paketler | Kullanım |
|---|---|---|
| `core` | `PyYAML`, `Pillow`, `pypdf`, `pandas`, `XlsxWriter`, `requests`, `beautifulsoup4`, `jsonschema` | Manifest, JSON Schema doğrulama, temel doküman/tablo/görsel ve API yardımcıları. |
| `cad` | `ezdxf[draw]` | DXF okuma, layer/entity/block kontrolü. |
| `bim` | `ifcopenshell` | IFC model, space, eleman ve property/quantity okuma. |
| `pdf-doc` | `python-docx`, `pdfplumber`, `PyMuPDF`, `markdown`, `odfpy`, `lxml` | DOCX/PDF/Markdown/ODF okuma, dönüştürme ve QA. |
| `spreadsheet` | `openpyxl`, `numpy` | XLSX okuma/yazma ve sayısal analiz. |
| `image-ocr` | `opencv-python`, `imagehash`, `pytesseract`, `scikit-image`, `exifread`, `piexif`, `rawpy`, `geopandas` | Fotoğraf kalite, OCR, metadata, duplicate ve GIS akışları. |
| `data-quality` | `jsonschema`, `frictionless`, `great-expectations`, `rapidfuzz` | Şema, veri kalite ve metin/ürün eşleştirme. |
| `communication` | `Jinja2`, `email-validator` | Mesaj şablonlama ve e-posta adres doğrulama. |
| `dev` | `pytest`, `jsonschema` | Test ve CI hazırlığı. |

## Skill Bazlı Bağımlılık Grupları

| Skill | Python grupları | Sistem araçları |
|---|---|---|
| `insaat-arac-kullanimlari` | `core`, `pdf-doc`, `spreadsheet` | Pandoc, LibreOffice |
| `cad-autocad-dwg-dxf-isleme` | `core`, `cad`, `pdf-doc` | ODA File Converter, LibreDWG, QCAD/LibreCAD |
| `bim-revit-ifc-model-kontrolu` | `core`, `bim`, `data-quality` | IfcConvert, IfcTester CLI, BlenderBIM |
| `blender-3d-modelleme-ve-render` | `core` | Blender |
| `sketchup-konsept-ve-kutle-modelleme` | `core` | SketchUp |
| `cizim-dosya-donusum-ve-qa` | `core`, `cad`, `bim`, `pdf-doc`, `data-quality` | Pandoc, LibreOffice, qpdf, IfcConvert, ODA File Converter |
| `insaat-hesaplamalar` | `core`, `spreadsheet` | Yok |
| `metraj-ve-mahal-kontrolu` | `core`, `bim`, `spreadsheet`, `data-quality` | IfcConvert |
| `teknik-sartname-ve-uygulama-kontrolu` | `core`, `pdf-doc`, `bim`, `data-quality` | Pandoc, LibreOffice, IfcTester CLI |
| `insaat-tasarim-ve-konsept` | `core`, `spreadsheet` | Yok |
| `teklif-ve-maliyet-tablolama` | `core`, `spreadsheet`, `data-quality` | LibreOffice |
| `hakedis-ve-mutabakat-kontrolu` | `core`, `spreadsheet`, `data-quality`, `bim` | LibreOffice |
| `tedarik-ve-malzeme-karsilastirma` | `core`, `spreadsheet`, `data-quality`, `communication` | OpenRefine, LibreOffice |
| `risk-guvenlik-ve-uygunluk-denetimi` | `core`, `spreadsheet`, `data-quality`, `pdf-doc`, `bim`, `communication` | IfcTester CLI, OpenSCAP, LibreOffice |
| `musteri-ve-taseron-iletisim-hazirlayici` | `core`, `communication`, `pdf-doc`, `spreadsheet` | Pandoc, LibreOffice |
| `saha-fotograf-ve-kanit-analizi` | `core`, `image-ocr`, `spreadsheet` | ExifTool, Tesseract OCR, ImageMagick, FFmpeg, QGIS, Docker |
| `dokuman-standartlastirma-ve-formatlama` | `core`, `pdf-doc`, `spreadsheet`, `communication` | Pandoc, LibreOffice, qpdf, Java, Node.js |

## Sistem Araçları

Bu araçlar Python paketi değildir; işletim sistemine ayrıca kurulmalıdır:

- Pandoc: Markdown/DOCX/PDF/HTML dönüşümü.
- LibreOffice: Office dosyalarını PDF veya farklı formatlara dönüştürme.
- qpdf: PDF doğrulama, onarım ve paketleme.
- ExifTool: EXIF/IPTC/XMP metadata çıkarımı.
- Tesseract OCR: Görselden metin okuma.
- ImageMagick: Görsel dönüştürme ve ön işleme.
- FFmpeg: Video kare çıkarımı.
- Blender: 3D modelleme/render scriptleri.
- SketchUp: SketchUp Ruby çıktılarını çalıştırma.
- IfcConvert / IfcTester CLI: IFC/IDS/BIM kalite kontrol.
- ODA File Converter / LibreDWG / QCAD / LibreCAD: CAD dönüşüm ve görüntüleme.
- QGIS: GIS/geotag çalışma.
- Docker: CVAT, Label Studio, WebODM gibi servisleri çalıştırma.
- Java / Node.js: LanguageTool, markdownlint, Prettier, remark-lint gibi QA araçları.

Kurulu ortamı JSON veya Markdown olarak denetlemek için:

```bash
python scripts/check_system_tools.py --format markdown
python scripts/check_system_tools.py --skill cad-autocad-dwg-dxf-isleme --format json
```

Çıktı durumları:

- `available`: araç veya Python modülü bulundu.
- `missing_required`: temel çalışma için gerekli Python modülü eksik.
- `missing_optional`: domain'e özel opsiyonel paket veya açık kaynak CLI eksik.
- `manual_install_required`: ticari/harici uygulama manuel lisans ve kurulum gerektirir.

## Notlar

- Birçok script opsiyonel paket yoksa anlaşılır hata mesajı veya araç durumu üretir.
- Finansal, İSG, teknik uygunluk ve üçüncü taraf iletişimi içeren çıktılar insan onayı gerektirir.
- Test ve CI hattı, temel manifest ve smoke akışlarını `dev` bağımlılıklarıyla doğrular; domain'e özel ağır bağımlılıklar ayrı ortamda kurulmalıdır.
