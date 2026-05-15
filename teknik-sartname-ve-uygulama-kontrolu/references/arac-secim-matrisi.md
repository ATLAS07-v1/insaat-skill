# Araç Seçim Matrisi

## Dosya ve Kaynak Tipi

| Kaynak | Birincil araç | Yedek araç | Kontrol |
|---|---|---|---|
| Metin tabanlı PDF | pdfplumber | pypdf / PyMuPDF | Sayfa izi, tablo varlığı, düşük güvenli satırlar. |
| Taranmış PDF | OCR dış araç | Manuel doğrulama | OCR sonucu sayfa görüntüsüyle eşleştirilmeli. |
| DOCX şartname | python-docx | pandoc | Başlık, paragraf, tablo ve revizyon izi. |
| CSV/XLSX tablo | pandas / openpyxl | stdlib csv | Kolon eşleme, boş alan, tekrar, tip kontrolü. |
| IFC + IDS | IfcTester | IfcOpenShell validation | Property, classification, entity ve quantity şartları. |
| IFC davranış testi | BIMTester | Gherkin parser | İnsan-okunur test senaryosu ve model sonucu. |
| Uygunsuzluk konusu | BCF API | OpenProject BCF API | Topic, viewpoint, kanıt dosyası, sorumlu kişi. |
| JSON çıktı | jsonschema | stdlib kontrol | Şema, zorunlu alan, tip ve enum kontrolü. |
| Veri kalite raporu | Great Expectations | pandas kontrolleri | Tablo kaynaklarında expectation suite yaklaşımı. |

## Seçim Kuralları

- Şartname kaynağı PDF/DOCX ise önce metin çıkarım kalitesini ölç; metin güvenilir değilse sonuçları düşük güven bayrağıyla ver.
- Kaynakta tablo yoğunluğu varsa pdfplumber/Camelot ve pandas hattını ayrı çalıştır.
- BIM bilgi gereksinimi açıkça model property veya classification ile ilgiliyse IDS/IfcTester rotası hazırla.
- Uygulama kontrolü saha kanıtına bağlıysa kanıt dosyası, tarih, mahal, imalat kalemi ve sorumlu alanlarını zorunlu kabul et.
- Sözleşme, standart veya yönetmelik yorumu gerekiyorsa kullanıcıdan geçerli doküman ve öncelik sırası istenir.
- Büyük projelerde JSON çıktı şeması ve BCF topic taslağı aynı madde id sistemini kullanmalıdır.

## Minimum Bağımlılık Modu

Hiç harici paket yoksa skill yine çalışır:

- TXT/MD/CSV/JSON kaynakları stdlib ile okur.
- Madde adaylarını regex ve anahtar kelime ile çıkarır.
- Kanıt eşleştirmeyi JSON/CSV kayıtları üzerinde yapar.
- PDF, DOCX, IFC, IDS ve BCF entegrasyonlarını eksik araç olarak bayraklar.
