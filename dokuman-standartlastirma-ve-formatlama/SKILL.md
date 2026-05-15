---
name: dokuman-standartlastirma-ve-formatlama
description: İnşaat proje dokümanları için DOCX, PDF, Markdown, XLSX, ODT, teknik rapor, şartname, method statement, toplantı tutanağı, RFI/submittal/transmittal, kapak, revizyon, stil, numaralandırma, dosya adlandırma, dönüşüm ve QA format kontrolü hazırlamak için kullanılır.
---

# Doküman Standartlaştırma ve Formatlama

## Ne Zaman Kullanılır

- Kullanıcı inşaat dokümanını standart kurumsal formata, başlık/numaralandırma düzenine, revizyon tablosuna veya teslim paketine çevirmek istediğinde.
- DOCX, PDF, Markdown, XLSX, ODT, HTML veya metin tabanlı belgelerde stil, başlık hiyerarşisi, kapak, içindekiler, ekler, tablo formatı ve çıktı QA kontrolü yapılacağında.
- Teknik şartname, method statement, ITP, RFI, submittal, transmittal, toplantı tutanağı, saha raporu, hakediş eki veya kalite/İSG raporu tek standarda çekileceğinde.
- Pandoc, LibreOffice, python-docx, Open XML SDK, Apache POI, Vale, LanguageTool, remark-lint, markdownlint veya Prettier gibi açık araçlar için rota seçileceğinde.
- Belge dönüşümü sonrası PDF sayfa düzeni, başlık sırası, revizyon, dosya adı, eksik bölüm, placeholder ve son kontrol bayrakları üretileceğinde.

Bu skill belge içeriğini hukuki, teknik veya sözleşmesel olarak onaylamaz. Formatlama ve standartlaştırma, yetkili teknik/hukuki/onay sahibinin nihai kontrolü yerine geçmez.

## Girdi

- Kaynak doküman: DOCX, Markdown, PDF, XLSX, ODT, HTML, TXT veya klasör içi doküman paketi.
- Doküman türü: teknik rapor, şartname, method statement, ITP, RFI, submittal, transmittal, toplantı tutanağı, kalite/İSG raporu, hakediş eki.
- Kurumsal standart: kapak, logo, proje kodu, başlıklar, sayfa üst/alt bilgi, revizyon tablosu, numaralandırma, dosya adı, dil ve terminoloji.
- Teslim hedefi: DOCX, PDF, Markdown, HTML, XLSX ek listesi, paket manifest veya QA raporu.
- Kontrol hedefi: eksik başlık, bozuk hiyerarşi, placeholder, gereksiz boşluk, revizyon eksikliği, link/dosya referansı, PDF dönüşüm kalite riski.

## Araç Stratejisi

| Durum | İlk tercih | İkinci tercih | Not |
|---|---|---|---|
| Markdown tabanlı kaynak | Pandoc | Prettier / remark-lint | Markdown'dan DOCX/PDF/HTML üretimi için güçlü rota. |
| DOCX oluşturma/düzenleme | python-docx | Open XML SDK / docx4j | Stil ve yapı düzeni için; karmaşık mevcut DOCX'te şablonla çalış. |
| DOCX/PPTX/XLSX yapısal işleme | Open XML SDK | Apache POI / docx4j | OOXML paket, stil, relation ve yapısal kontrol için. |
| PDF/Office dönüşümü | LibreOffice headless | Pandoc + PDF engine | Görsel QA gerekir; dönüşüm başarı durumu tek başına yeterli değildir. |
| Markdown kalite kontrol | `validate_markdown_document.py` | markdownlint / remark-lint | Başlık hiyerarşisi, placeholder, uzun satır ve zorunlu bölüm kontrolü. |
| Doküman paketi denetimi | `inspect_document_package.py` | Frictionless / manifest | Dosya adı, revizyon, duplicate ve desteklenmeyen format kontrolü. |
| Dil/stil kontrolü | Vale | LanguageTool | Kurumsal dil, yazım ve terminoloji tutarlılığı için. |
| XLSX ek/manifest | openpyxl / pandas | LibreOffice Calc | Doküman register, ek listesi ve transmittal tablosu için. |

## İş Akışı

1. Doküman türünü ve teslim hedefini belirle: rapor, şartname, method statement, RFI, submittal, transmittal, tutanak veya paket manifest.
2. Kaynakları ayır: düzenlenecek ana belge, referans dosyalar, ekler, görseller, çizim/model linkleri ve revizyon bilgisi.
3. Standart şablonu seç: kapak, başlık hiyerarşisi, revizyon tablosu, doküman kodu, sayfa düzeni, footer/header ve ek yapısı.
4. İçerik yapısını normalize et: başlıklar, numaralandırma, tablo başlıkları, görsel altyazıları, ekler, referanslar ve terminoloji.
5. Dönüşüm rotasını seç: Markdown/Pandoc, DOCX/python-docx, LibreOffice headless, OOXML SDK veya manuel QA.
6. QA kontrolü yap: eksik zorunlu bölüm, placeholder, bozuk başlık, duplicate dosya, revizyon eksikliği, bozuk link, PDF dönüşüm riski.
7. Çıktı paketini üret: ana belge, PDF, ek listesi, revizyon notu, QA raporu ve gönderim/transmittal özeti.
8. Onay sınırını yaz: format doğru olsa bile teknik, hukuki, sözleşmesel ve ticari içerik yetkili onay gerektirir.

## Çıktı Formatı

```markdown
## Doküman Standardizasyon Özeti

## Kaynak ve Hedef Formatlar

## Uygulanan Format / Stil Kuralları

## Revizyon ve Dosya Adlandırma Kontrolü

## Dönüşüm / PDF QA Sonuçları

## Eksik Bölüm ve Placeholder Bulguları

## Teslim Paketi Manifesti

## Onay Sınırı
```

Makine çıktısı için `references/cikti-semalari.md` içindeki JSON şemalarını kullan.

## Kalite Kapısı

- Doküman türü, proje kodu, doküman kodu, revizyon, tarih ve sorumlu bilgisi açık olmalıdır.
- Başlık hiyerarşisi atlamalı olmamalıdır; H2'den H4'e doğrudan geçilmez.
- Placeholder, `TODO`, `TBD`, boş köşeli parantez veya örnek metin teslim dokümanında kalmamalıdır.
- PDF dönüşümü sonrası sayfa, tablo, görsel, header/footer ve kesilmiş metin görsel olarak kontrol edilmelidir.
- Revizyon tablosu ile dosya adı revizyonu çelişmemelidir.
- DOCX/PDF dönüşümü içeriğin teknik doğruluğunu kanıtlamaz; sadece format çıktısıdır.
- Sözleşmesel, hukuki, finansal ve teknik karar içeren metinler yetkili onay gerektirir.

## Referanslar

- Açık kaynak araştırması: `references/acik-kaynak-arastirma.md`
- Araç seçim matrisi: `references/arac-secim-matrisi.md`
- Doküman standardizasyon iş akışı: `references/dokuman-standartlastirma-is-akisi.md`
- Stil ve format kuralları: `references/stil-ve-format-kurallari.md`
- Revizyon ve dosya adlandırma kuralları: `references/revizyon-ve-dosya-adlandirma-kurallari.md`
- Dönüşüm ve PDF QA kuralları: `references/donusum-ve-pdf-qa-kurallari.md`
- Çıktı şemaları: `references/cikti-semalari.md`

## Yardımcı Scriptler

- `scripts/check_document_format_tools.py`: doküman, PDF, Markdown, stil ve dönüşüm araçlarının durumunu raporlar.
- `scripts/plan_document_standardization_route.py`: doküman tipine göre rota, araç, QA kapısı ve çıktı seti üretir.
- `scripts/inspect_document_package.py`: klasör içi doküman paketini dosya adı, revizyon, format ve duplicate açısından denetler.
- `scripts/validate_markdown_document.py`: Markdown dokümanlarda başlık hiyerarşisi, placeholder, uzun satır ve zorunlu bölüm kontrolü yapar.
