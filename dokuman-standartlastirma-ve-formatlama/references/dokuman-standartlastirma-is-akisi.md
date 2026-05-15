# Doküman Standardizasyon İş Akışı

## 1. Sınıflandırma

- Doküman türü
- Proje kodu
- Doküman kodu
- Revizyon
- Teslim hedefi
- Onay sahibi
- Kaynak format
- Hedef format

## 2. Şablon Seçimi

Şablon şu öğeleri tanımlamalıdır:

- kapak,
- doküman bilgi tablosu,
- revizyon tablosu,
- başlık stilleri,
- sayfa üst/alt bilgi,
- tablo/görsel altyazısı,
- içindekiler,
- ekler,
- onay sayfası.

## 3. İçerik Normalizasyonu

- Başlık hiyerarşisi düzenlenir.
- Tekrarlı başlıklar temizlenir.
- Placeholder ve örnek metin kaldırılır.
- Tablo başlıkları standartlaştırılır.
- Şekil/görsel altyazıları eklenir.
- Ek ve referans listeleri ayrılır.
- Revizyon notu güncellenir.

## 4. Dönüşüm

- Markdown kaynak: Pandoc.
- DOCX kaynak: python-docx, LibreOffice veya OOXML aracı.
- PDF hedef: LibreOffice veya Pandoc PDF engine.
- XLSX ek: openpyxl/pandas veya mevcut spreadsheet skill'i.

## 5. QA

- Dosya adı ve revizyon uyumu.
- Zorunlu bölümler.
- Başlık hiyerarşisi.
- Placeholder.
- Bozuk link/dosya referansı.
- PDF görsel kalite.
- Sayfa sonu ve tablo taşması.
- Onay sınırı.

## 6. Teslim Paketi

- Ana doküman.
- PDF.
- Ekler.
- Manifest.
- QA raporu.
- Revizyon notu.
- Transmittal veya gönderim özeti.
