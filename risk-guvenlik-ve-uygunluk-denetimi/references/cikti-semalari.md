# Çıktı Şemaları

## Risk Register JSON

```json
{
  "risks": [
    {
      "id": "R-001",
      "activity": "Cephe iskelesinde çalışma",
      "hazard": "Yüksekten düşme",
      "location": "Blok A / Cephe",
      "affected_people": ["çalışan", "taşeron"],
      "likelihood": 4,
      "severity": 5,
      "controls": ["iskele etiketi", "kenar koruma", "emniyet kemeri"],
      "residual_likelihood": 2,
      "residual_severity": 5,
      "owner": "Şantiye şefi",
      "due_date": "2026-05-20",
      "evidence": ["iskele-kontrol-formu.pdf"],
      "status": "open"
    }
  ]
}
```

## Compliance Checklist JSON

```json
{
  "requirements": [
    {
      "id": "PTW-001",
      "source": "İşveren sıcak iş prosedürü",
      "source_version": "Rev.03 / 2026-04-10",
      "category": "sıcak iş",
      "requirement": "Sıcak iş başlamadan önce geçerli sıcak iş izni alınmalıdır.",
      "mandatory": true,
      "evidence_required": true,
      "owner": "Taşeron saha sorumlusu",
      "due_date": "2026-05-15"
    }
  ]
}
```

## Evidence Register JSON

```json
{
  "evidence": [
    {
      "evidence_id": "EV-001",
      "requirement_id": "PTW-001",
      "type": "permit",
      "file": "sicak-is-izni-2026-05-15.pdf",
      "date": "2026-05-15",
      "owner": "İSG uzmanı",
      "status": "accepted",
      "notes": "İzin saha sorumlusu ve İSG tarafından imzalı."
    }
  ]
}
```

## Compliance Audit Output

```json
{
  "summary": {
    "requirement_count": 1,
    "pass_count": 1,
    "fail_count": 0,
    "missing_evidence_count": 0,
    "pending_count": 0,
    "not_applicable_count": 0
  },
  "results": [
    {
      "id": "PTW-001",
      "status": "pass",
      "category": "sıcak iş",
      "requirement": "Sıcak iş başlamadan önce geçerli sıcak iş izni alınmalıdır.",
      "evidence_count": 1,
      "flags": []
    }
  ],
  "issues": []
}
```

## Markdown Rapor Bölümleri

```markdown
## Kapsam
## Kaynaklar
## Kritik Bulgular
## Risk Register
## Uygunluk Matrisi
## Kanıt Eksikleri
## Aksiyon Planı
## Onay Sınırı
```
