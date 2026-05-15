# Hibrit İş Akışı

## 1. Envanter

Her işlem önce dosya envanteriyle başlar:

- dosya adı
- uzantı
- boyut
- SHA256
- kategori
- önerilen araç
- risk bayrağı

`scripts/inspect_construction_inputs.py` bu aşama için kullanılabilir.

## 2. Araç Seçim Kararı

| Durum | Seçim |
|---|---|
| Hızlı LLM bağlamı isteniyor | MarkItDown |
| PDF layout karmaşık | Docling |
| PDF sayfası görsele çevrilecek | PyMuPDF |
| PDF tablo hassas çıkarılacak | pdfplumber |
| CSV/XLSX normalize edilecek | pandas |
| XLSX formül/sheet yapısı korunacak | openpyxl |
| DXF okunacak | ezdxf |
| DWG okunacak | LibreDWG veya FreeCAD ile DXF'e dönüştür, sonra QA |
| IFC okunacak | IfcOpenShell |
| Taranmış görsel/PDF iyileştirilecek | OpenCV + OCR |

## 3. Kanıt Haritası

Her çıkarılan veri şu kanıt alanlarından en az birini taşımalı:

- `source_file`
- `page`
- `sheet`
- `row`
- `column`
- `layer`
- `block`
- `entity_type`
- `image_region`
- `confidence`

## 4. Normalizasyon

Çıktıları şu ortak kolonlara çevirmeye çalış:

| Kolon | Açıklama |
|---|---|
| `source_id` | Dosya veya belge kimliği |
| `discipline` | Mimari, mekanik, elektrik, statik, genel |
| `space` | Mahal |
| `work_item` | İş kalemi |
| `description` | Açıklama |
| `quantity` | Miktar |
| `unit` | Birim |
| `evidence` | Sayfa/sheet/layer/region kanıtı |
| `quality_flag` | Belirsizlik veya hata bayrağı |

## 5. Sonraki Skill Yönlendirmesi

| Çıkarılan veri | Sonraki skill |
|---|---|
| mahal/metraj | `metraj-ve-mahal-kontrolu` |
| teknik madde | `teknik-sartname-ve-uygulama-kontrolu` |
| maliyet/teklif tablosu | `teklif-ve-maliyet-tablolama` |
| hakediş | `hakedis-ve-mutabakat-kontrolu` |
| malzeme listesi | `tedarik-ve-malzeme-karsilastirma` |
| risk/uygunsuzluk | `risk-guvenlik-ve-uygunluk-denetimi` |
| müşteri/taşeron mesajı | `musteri-ve-taseron-iletisim-hazirlayici` |
