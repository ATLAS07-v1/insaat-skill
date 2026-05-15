# Çıktı Şemaları

## Envanter JSON

```json
{
  "root": "C:/path/to/input",
  "files": [
    {
      "path": "C:/path/to/file.pdf",
      "name": "file.pdf",
      "extension": ".pdf",
      "size_bytes": 123456,
      "sha256": "hash",
      "category": "document",
      "recommended_tools": ["markitdown", "docling", "pymupdf", "pdfplumber"],
      "risk_flags": []
    }
  ]
}
```

## Çıkarılan Veri JSON

```json
{
  "source_file": "file.pdf",
  "extraction_method": "pdfplumber",
  "records": [
    {
      "discipline": "mimari",
      "space": "Salon",
      "work_item": "Seramik kaplama",
      "description": "60x120 seramik",
      "quantity": 42.5,
      "unit": "m2",
      "evidence": "page=3 table=1 row=8",
      "quality_flag": "unit_confirmed"
    }
  ],
  "warnings": []
}
```

## Araç Rotası Markdown

```markdown
| Dosya | Kategori | İlk Araç | İkinci Araç | Sebep | Risk |
|---|---|---|---|---|---|
| keşif.pdf | PDF tablo | pdfplumber | Docling | Tablo ve sayfa kanıtı gerekiyor | birleşik hücre olabilir |
```
