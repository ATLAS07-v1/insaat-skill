# Çıktı Şemaları

## Hakediş Girdi JSON

```json
{
  "project": "Demo Project",
  "payment_no": "HP-03",
  "currency": "TRY",
  "items": [
    {
      "code": "C-001",
      "description": "C30/37 beton",
      "unit": "m3",
      "contract_quantity": 500,
      "unit_price": 2750,
      "previous_quantity": 120,
      "current_quantity": 80,
      "approved_current_quantity": 75
    }
  ],
  "deductions": {
    "retention_percent": 5,
    "advance_recovery_amount": 20000,
    "other_deductions": 0,
    "vat_percent": 20
  }
}
```

## Hakediş Çıktı JSON

```json
{
  "summary": {
    "current_gross": 206250,
    "retention_amount": 10312.5,
    "advance_recovery_amount": 20000,
    "net_before_tax": 175937.5,
    "vat_amount": 35187.5,
    "payable_current": 211125,
    "currency": "TRY"
  },
  "items": [],
  "qa_flags": []
}
```

## Mutabakat Fark JSON

```json
{
  "summary": {
    "source_a_count": 5,
    "source_b_count": 4,
    "matched_count": 4,
    "issue_count": 1
  },
  "issues": [
    {
      "type": "amount_mismatch",
      "key": "C-001",
      "source_a_amount": 206250,
      "source_b_amount": 205000,
      "delta_amount": 1250
    }
  ]
}
```

## Markdown Rapor Bölümleri

```markdown
## Hakediş / Mutabakat Özeti
## Kaynaklar ve Varsayımlar
## Sözleşme ve Önceki Hakediş Kontrolü
## Cari Hakediş Hesabı
## Kesinti, Avans, Teminat ve KDV
## Fatura / Ödeme Mutabakatı
## Fark ve Uyuşmazlık Tablosu
## Kritik QA Bayrakları
## Onay Sınırı ve Sonraki Aksiyonlar
```
