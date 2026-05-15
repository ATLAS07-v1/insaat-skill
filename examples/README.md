# Örnekler

Bu klasör, skill setini kuran agent veya kullanıcının hızlıca deneyebileceği küçük, deterministik örnekleri içerir.

## Quickstart

`quickstart` senaryosu şu akışları çalıştırır:

- risk register skorlama,
- uygunluk checklist ve kanıt denetimi,
- müşteri/taşeron iletişim paketi kontrolü,
- Markdown doküman QA,
- teklif/maliyet tablosu üretimi,
- hakediş hesap özeti.

Çalıştırmak için:

```powershell
python scripts\run_examples.py --scenario quickstart
```

Varsayılan çıktı klasörü:

```text
dist/example-runs/quickstart/
```

JSON çıktı almak için:

```powershell
python scripts\run_examples.py --scenario quickstart --format json
```
