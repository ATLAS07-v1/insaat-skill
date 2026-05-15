# Çıktı Şemaları

## Madde Çıkarma JSON

```json
{
  "metadata": {
    "source": "technical-spec.pdf",
    "source_type": "pdf",
    "extraction_confidence": "medium",
    "created_at": "2026-05-15T12:00:00Z"
  },
  "clauses": [
    {
      "id": "SPEC-001",
      "source_ref": "page 12 / 03 30 00 3.2",
      "text": "Concrete compressive strength shall be verified by test reports.",
      "category": "test",
      "discipline": "structural",
      "evidence_required": ["test_report"],
      "acceptance_criteria": "compressive strength value from source clause",
      "severity": "high",
      "flags": ["requires_source_standard"]
    }
  ]
}
```

## Kanıt Eşleştirme JSON

```json
{
  "summary": {
    "total_clauses": 24,
    "passed": 12,
    "failed": 2,
    "missing_evidence": 7,
    "pending": 3
  },
  "results": [
    {
      "clause_id": "SPEC-001",
      "status": "missing_evidence",
      "matched_evidence": [],
      "required_evidence": ["test_report"],
      "action": "Test raporu veya laboratuvar sonucu istenmeli."
    }
  ]
}
```

## BCF Issue Taslağı JSON

```json
{
  "topic": {
    "title": "SPEC-001 test raporu eksik",
    "topic_type": "Issue",
    "topic_status": "Open",
    "priority": "High",
    "labels": ["Specification", "QA", "MissingEvidence"]
  },
  "comment": {
    "body": "Şartname maddesi SPEC-001 test raporu gerektiriyor; kanıt paketinde eşleşen rapor bulunamadı."
  }
}
```

## Markdown Rapor Bölümleri

```markdown
## Teknik Şartname / Uygulama Kontrol Özeti
## Kaynaklar ve Revizyonlar
## Madde Bazlı Kontrol Listesi
## Kanıt Eşleştirme
## Uygunsuzluk ve Eksik Kanıtlar
## Tolerans / Test / Submittal Kontrolleri
## BIM / IDS / BCF Notları
## Kritik Bayraklar
## Onay Sınırı ve Sonraki Aksiyonlar
```
