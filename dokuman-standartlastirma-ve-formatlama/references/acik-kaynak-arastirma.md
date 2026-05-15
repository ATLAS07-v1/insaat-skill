# Açık Kaynak Araştırması

Bu skill, inşaat dokümanlarını sadece biçimsel olarak düzeltmek yerine dönüştürülebilir, izlenebilir ve QA edilebilir doküman paketlerine çevirmek için açık araçları birlikte kullanır.

## Referans Alınan Açık Kaynak Araçlar

| Kaynak | Kullanım | Neden alındı |
|---|---|---|
| Pandoc | Markdown, HTML, DOCX, ODT, PDF ve diğer formatlar arasında dönüşüm | Metin tabanlı kaynak dokümandan çok formatlı teslim üretimi için ana rota. |
| LibreOffice | Office dosyalarını headless dönüştürme, PDF export ve ODT/DOCX uyumluluk | Gerçek ofis formatlarında batch dönüşüm ve görsel çıktı üretimi için. |
| python-docx | Python ile DOCX oluşturma ve düzenleme | Kapak, başlık, paragraf, tablo ve temel Word çıktıları için pratik. |
| Open XML SDK | OOXML paketlerini yapısal olarak işleme | DOCX/XLSX/PPTX yapısını, XML parçalarını ve farkları denetleme referansı. |
| Apache POI | Java ile OOXML/OLE2 dosyaları okuma/yazma | Kurumsal Java akışlarında DOCX/XLSX/PPTX işleme için. |
| Vale | Markdown/AsciiDoc/HTML/XML gibi formatlarda prose/style lint | Kurumsal dil, stil ve terminoloji kuralı yazmak için. |
| LanguageTool | Çok dilli yazım, dilbilgisi ve stil kontrolü | Türkçe dahil çok dilli dokümanlarda dil QA katmanı için. |
| remark-lint / markdownlint | Markdown başlık, liste, link ve biçim kuralları | Markdown kaynak doküman standardı ve CI kontrolü için. |
| Prettier | Markdown/YAML/JSON ve benzeri metin formatlarında tutarlı biçim | Otomatik formatlama, satır ve tablo düzeni için. |

## Hibrit Çalışma Kararı

1. Markdown kaynak varsa önce metin standardı ve Pandoc rotası tercih edilir.
2. DOCX manipülasyonu gerekiyorsa python-docx hızlı rota; karmaşık OOXML yapısı için Open XML SDK/docx4j/Apache POI referans alınır.
3. PDF, görsel teslim formatıdır; conversion success tek başına yeterli değildir, render/görsel QA gerekir.
4. Stil ve dil kontrolü ayrı katmandır: Vale kurumsal stil, LanguageTool dilbilgisi için kullanılır.
5. Dosya paketi tesliminde manifest, revizyon, format ve placeholder kontrolü zorunlu kabul edilir.

## Kaynak Linkleri

- Pandoc: https://pandoc.org/
- Pandoc GitHub: https://github.com/jgm/pandoc
- LibreOffice Core: https://github.com/LibreOffice/core
- python-docx: https://github.com/python-openxml/python-docx
- Open XML SDK: https://github.com/dotnet/Open-XML-SDK
- Apache POI: https://github.com/apache/poi
- Vale: https://github.com/vale-cli/vale
- LanguageTool: https://github.com/languagetool-org/languagetool
- remark-lint: https://github.com/remarkjs/remark-lint
