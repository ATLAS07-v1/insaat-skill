# Risk Skorlama ve Önceliklendirme

## 5x5 Matris

| Değer | Olasılık | Şiddet |
|---|---|---|
| 1 | Çok düşük | Önemsiz / ilk yardım |
| 2 | Düşük | Hafif yaralanma / düşük hasar |
| 3 | Orta | Kayıp zamanlı yaralanma / orta hasar |
| 4 | Yüksek | Ağır yaralanma / büyük hasar |
| 5 | Çok yüksek | Ölüm / çoklu ağır yaralanma / kritik hasar |

Risk skoru:

```text
risk_score = likelihood * severity
```

## Seviye Eşikleri

| Skor | Seviye | Aksiyon |
|---|---|---|
| 1-4 | low | Normal takip, periyodik kontrol |
| 5-9 | medium | Planlı aksiyon ve sorumlu ataması |
| 10-16 | high | Öncelikli düzeltme, yönetici/İSG incelemesi |
| 17-25 | critical | Acil değerlendirme, yetkili karar ve iş planı revizyonu |

## Artık Risk

Artık risk, kontrol önlemleri tanımlandıktan ve uygulanabilirliği değerlendirildikten sonra ayrıca verilmelidir. Sadece "kontrol yazıldığı" için skor otomatik düşürülmez.

## Öncelik Bayrakları

- `critical_or_high`: risk seviyesi high veya critical.
- `missing_controls`: kontrol önlemi yok.
- `missing_owner`: sorumlu yok.
- `overdue`: termin geçmiş ve durum kapalı değil.
- `missing_evidence_for_high`: yüksek/kritik riskte kanıt yok.
- `residual_not_assessed`: artık risk değerleri yok.
- `needs_management_review`: yüksek/kritik artık risk veya kapatılmamış kritik bulgu.

## Risk Kabulü

Yüksek veya kritik artık risk kabul edilecekse:

- kabul gerekçesi,
- yetkili kişi,
- tarih,
- geçici kontrol,
- izleme periyodu,
- kalan risk iletişimi

kayda bağlanmalıdır.
