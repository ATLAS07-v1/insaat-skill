# Çıktı Şemaları

## Communication Brief JSON

```json
{
  "message_type": "rfi",
  "channel": "email",
  "recipient_type": "müşteri",
  "project": "Proje A",
  "subject": "RFI-024 - Mekanik şaft ölçüsü",
  "recipient": "İşveren temsilcisi",
  "sender": "Proje ekibi",
  "facts": [
    "A Blok 3. kat mekanik şaftta çizim ve saha ölçüsü arasında 12 cm fark görülmüştür."
  ],
  "request": "Uygulama öncesi revize ölçü veya tasarım teyidi rica ederiz.",
  "due_date": "2026-05-20",
  "references": ["M-301 Rev.04", "Toplantı-12 Madde 5"],
  "attachments": ["saha-fotograf-01.jpg"],
  "tone": "resmi",
  "approval_required": true
}
```

## Communication Draft Output

```json
{
  "subject": "RFI-024 - Mekanik şaft ölçüsü",
  "body": "Merhaba ...",
  "sections": {
    "context": [],
    "request": [],
    "actions": []
  },
  "risk_notes": [
    "Gönderim öncesi teknik yetkili onayı gerekir."
  ]
}
```

## Validation Output

```json
{
  "summary": {
    "message_count": 1,
    "issue_count": 2,
    "approval_required_count": 1
  },
  "messages": [
    {
      "id": "MSG-001",
      "status": "needs_review",
      "flags": ["approval_required", "missing_due_date"]
    }
  ],
  "issues": [
    {
      "message_id": "MSG-001",
      "flag": "missing_due_date"
    }
  ]
}
```

## Markdown Paket

```markdown
## İletişim Paketi
## Taslak Mesaj
## Referanslar
## Ekler
## Aksiyonlar
## Onay Gerektiren Noktalar
## Takip Kaydı
```
