# Çıktı Şemaları

## Photo Evidence Register JSON

```json
{
  "photos": [
    {
      "evidence_id": "PH-0001",
      "file_path": "C:/project/photos/img001.jpg",
      "file_name": "img001.jpg",
      "sha256": "abc123",
      "file_size": 2451220,
      "extension": ".jpg",
      "width": 4032,
      "height": 3024,
      "captured_at": "2026-05-15T10:42:00",
      "modified_at": "2026-05-15T11:00:00",
      "exif_present": true,
      "gps_present": false,
      "project": "Proje A",
      "location": "A Blok / 3. Kat",
      "subject": "Mekanik şaft kontrolü",
      "source": "Saha ekibi",
      "tags": ["quality_defect"]
    }
  ]
}
```

## Validation Output

```json
{
  "summary": {
    "photo_count": 1,
    "ready_count": 0,
    "needs_review_count": 1,
    "issue_count": 2
  },
  "photos": [
    {
      "evidence_id": "PH-0001",
      "status": "needs_review",
      "flags": ["missing_location", "gps_present"]
    }
  ],
  "issues": [
    {
      "evidence_id": "PH-0001",
      "flag": "missing_location"
    }
  ]
}
```

## Markdown Rapor

```markdown
## Kanıt Paketi Özeti
## Fotoğraf Register
## Metadata ve Hash Kontrolü
## Duplicate / Near-Duplicate Bulguları
## Görsel Bulgular
## Eksik Kanıtlar
## Gizlilik Bayrakları
## Aksiyon Planı
```
