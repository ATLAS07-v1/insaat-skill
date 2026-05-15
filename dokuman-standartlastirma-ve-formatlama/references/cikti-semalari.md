# Çıktı Şemaları

## Document Package Manifest

```json
{
  "documents": [
    {
      "document_id": "DOC-001",
      "file_path": "C:/project/docs/SGA-MEK-MS-004-R02-2026-05-15.docx",
      "file_name": "SGA-MEK-MS-004-R02-2026-05-15.docx",
      "extension": ".docx",
      "document_type": "method_statement",
      "project_code": "SGA",
      "revision": "R02",
      "date": "2026-05-15",
      "status": "for_approval",
      "sha256": "abc123"
    }
  ]
}
```

## Markdown QA Output

```json
{
  "summary": {
    "heading_count": 8,
    "issue_count": 2,
    "status": "needs_review"
  },
  "issues": [
    {
      "line": 12,
      "flag": "heading_level_skip",
      "message": "H2 seviyesinden H4 seviyesine atlandı."
    }
  ]
}
```

## Package Inspection Output

```json
{
  "summary": {
    "file_count": 4,
    "supported_count": 3,
    "issue_count": 2
  },
  "files": [
    {
      "file_name": "SGA-MEK-MS-004-R02-2026-05-15.docx",
      "status": "ready",
      "flags": []
    }
  ]
}
```

## Markdown Rapor

```markdown
## Doküman Standardizasyon Özeti
## Dönüşüm Rotası
## Revizyon ve Dosya Adı Kontrolü
## Stil ve Format QA
## PDF QA
## Teslim Paketi Manifesti
## Onay Sınırı
```
