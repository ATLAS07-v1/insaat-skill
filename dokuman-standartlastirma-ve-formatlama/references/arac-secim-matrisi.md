# Araç Seçim Matrisi

## İş Tipine Göre Rota

| İş tipi | Veri | Ana araç | Destek araç | Çıktı |
|---|---|---|---|---|
| Markdown -> DOCX/PDF | `.md`, şablon | Pandoc | `validate_markdown_document.py` | DOCX/PDF/HTML, QA raporu |
| DOCX standardizasyon | `.docx`, kurumsal şablon | python-docx | Open XML SDK | DOCX, revizyonlu format raporu |
| Office -> PDF dönüşümü | DOCX/XLSX/PPTX/ODT | LibreOffice headless | qpdf / pypdf | PDF, dönüşüm QA notu |
| Teknik rapor formatı | Markdown/DOCX | Pandoc veya python-docx | Vale / LanguageTool | rapor, stil kontrol listesi |
| Şartname/method statement | DOCX/Markdown | python-docx / Pandoc | `validate_markdown_document.py` | standart doküman, eksik bölüm listesi |
| Toplantı tutanağı | Markdown/DOCX | şablon + Pandoc | OpenProject Meetings | tutanak, aksiyon tablosu |
| RFI/submittal/transmittal | Markdown/DOCX/XLSX | şablon + manifest | iletişim skill'i | gönderim notu, ek listesi |
| Doküman paket denetimi | klasör | `inspect_document_package.py` | Frictionless | manifest, revizyon/format hataları |
| Dil/stil QA | Markdown/HTML/Text | Vale | LanguageTool | stil/dil QA raporu |

## Seçim Kuralları

- Dönüşümden önce kaynak doküman yapısı temizlenir; bozuk başlık ve placeholder dönüşümden sonra düzeltilmez.
- DOCX şablonu varsa stiller elle taklit edilmez; mümkünse şablon üzerinde çalışılır.
- PDF tesliminde sayfa kırılması, tablo taşması ve görsel bozulması manuel/render QA gerektirir.
- Markdown kaynaklı işlerde başlık hiyerarşisi ve zorunlu bölüm kontrolü otomatik yapılmalıdır.
- Revizyon ve dosya adı kontrolü teslim paketi seviyesinde yapılır; tek dosya yeterli değildir.
