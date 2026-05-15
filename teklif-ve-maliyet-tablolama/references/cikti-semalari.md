# Çıktı Şemaları

## Maliyet Girdi JSON

```json
{
  "project": "Demo Project",
  "currency": "TRY",
  "items": [
    {
      "code": "C-001",
      "description": "C30/37 hazır beton",
      "category": "Kaba yapı",
      "quantity": 120,
      "unit": "m3",
      "unit_price": 2750,
      "waste_percent": 2,
      "source": "user_provided",
      "notes": "Pompa dahil değil"
    }
  ],
  "markups": {
    "overhead_percent": 10,
    "profit_percent": 12,
    "contingency_percent": 5,
    "discount_percent": 0,
    "vat_percent": 20
  }
}
```

## Maliyet Çıktı JSON

```json
{
  "summary": {
    "direct_total": 336600,
    "overhead_amount": 33660,
    "profit_amount": 40392,
    "contingency_amount": 16830,
    "discount_amount": 0,
    "subtotal_before_tax": 427482,
    "vat_amount": 85496.4,
    "grand_total": 512978.4,
    "currency": "TRY"
  },
  "items": [],
  "category_totals": {},
  "qa_flags": []
}
```

## Taşeron Karşılaştırma JSON

```json
{
  "package": "Alçıpan işleri",
  "quotes": [
    {
      "supplier": "Firma A",
      "total": 120000,
      "currency": "TRY",
      "included": ["malzeme", "işçilik"],
      "excluded": ["iskele", "nakliye"],
      "risk_flags": ["scope_exclusion"]
    }
  ],
  "normalized_comparison": []
}
```

## Markdown Rapor Bölümleri

```markdown
## Teklif / Maliyet Özeti
## Kaynaklar ve Varsayımlar
## BOQ / Kalem Tablosu
## Kategori Toplamları
## Markup, KDV ve Toplam
## Taşeron / Tedarikçi Karşılaştırması
## QA Bayrakları
## Riskler ve Kapsam Dışı İşler
## Onay Sınırı ve Sonraki Aksiyonlar
```
