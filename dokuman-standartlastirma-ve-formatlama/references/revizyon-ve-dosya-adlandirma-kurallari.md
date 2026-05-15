# Revizyon ve Dosya Adlandırma Kuralları

## Önerilen Dosya Adı

```text
PROJEKODU-DISIPLIN-DOKTURU-DOKNO-REV-TARIH-kisa-konu.ext
```

Örnek:

```text
SGA-MEK-MS-004-R02-2026-05-15-mekanik-saft-method-statement.docx
```

## Minimum Alanlar

- Proje kodu
- Disiplin
- Doküman türü
- Doküman no
- Revizyon
- Tarih
- Kısa konu
- Uzantı

## Revizyon Tablosu

Her revizyon satırı:

- revizyon kodu,
- tarih,
- açıklama,
- hazırlayan,
- kontrol eden,
- onaylayan,
- durum

alanlarını taşımalıdır.

## Bayraklar

- `missing_revision`: dosya adında veya dokümanda revizyon yok.
- `revision_conflict`: dosya adı revizyonu ve doküman içi revizyon farklı.
- `missing_date`: tarih yok.
- `unsafe_filename`: boşluk, Türkçe karakter, özel karakter veya çok uzun dosya adı var.
- `duplicate_base_name`: aynı dokümanın birden fazla kopyası var.
- `unsupported_extension`: teslim formatı desteklenmiyor.

## Not

Türkçe karakterler doküman içinde doğal olarak kullanılabilir. Ancak teslim dosya adında kurum standardı yoksa ASCII ve kısa dosya adı tercih edilir.
