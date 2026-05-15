# Quickstart Saha Kontrol ve Maliyet Senaryosu

Bu senaryo küçük bir demo proje üzerinden risk, uygunluk, iletişim, doküman, maliyet ve hakediş scriptlerini birlikte çalıştırır.

## Girdiler

Girdi dosyaları `inputs/` altındadır:

- `risk_register.json`
- `compliance_checklist.json`
- `compliance_evidence.json`
- `communication_pack.json`
- `site_report_with_issues.md`
- `cost_items.json`
- `progress_payment.json`

## Çalıştırma

```powershell
python scripts\run_examples.py --scenario quickstart --output-dir dist\example-runs\quickstart
```

Üretilen `summary.json`, her adımın durumunu ve ilgili script çıktılarının özet alanlarını içerir.

## Beklenen Öğrenme

Bu örnek, agent'in hangi skill'i ne zaman çağıracağını göstermeye odaklanır. Çıktılar resmi teknik, finansal veya İSG onayı değildir.
