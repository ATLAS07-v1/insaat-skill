# Çıktı Şemaları

## Tedarikçi Teklif Girdi JSON

```json
{
  "currency": "TRY",
  "required_delivery_days": 21,
  "items": [
    {"code": "MAT-001", "description": "Yangın kapısı", "quantity": 12, "unit": "adet"}
  ],
  "quotes": [
    {
      "supplier": "Firma A",
      "currency": "TRY",
      "items": [
        {"code": "MAT-001", "unit_price": 8500, "quantity": 12, "lead_time_days": 18, "technical_status": "pass"}
      ],
      "warranty_months": 24,
      "stock_confirmed": true,
      "certificates": ["CE"],
      "exclusions": []
    }
  ]
}
```

## Malzeme Teknik Uygunluk Girdi JSON

```json
{
  "requirements": [
    {"attribute": "fire_rating_min", "min": 60, "unit": "min"},
    {"attribute": "certificate", "required_values": ["CE", "TSE"]}
  ],
  "offers": [
    {
      "supplier": "Firma A",
      "product": "FD-90",
      "attributes": {"fire_rating_min": 90, "certificate": ["CE", "TSE"]}
    }
  ]
}
```

## Karşılaştırma Çıktısı JSON

```json
{
  "ranking": [
    {
      "supplier": "Firma A",
      "total_price": 102000,
      "score": 8.4,
      "risk_flags": [],
      "decision_note": "Dengeli teknik ve ticari aday."
    }
  ],
  "issues": []
}
```

## Markdown Rapor Bölümleri

```markdown
## Tedarik / Malzeme Karşılaştırma Özeti
## İhtiyaç ve Şartname Kriterleri
## Tedarikçi Teklif Matrisi
## Malzeme Teknik Uygunluk Matrisi
## Fiyat, Termin, Stok ve Ödeme Karşılaştırması
## Riskler ve Eksik Belgeler
## Önerilen Aksiyonlar
## Onay Sınırı
```
