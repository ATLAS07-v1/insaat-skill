# Contributing

Bu repo skill setini agent tarafından kopyalanabilir ve doğrulanabilir tutmak için katı bir dosya sözleşmesi kullanır.

## Yeni Skill Ekleme

1. Kök dizinde yeni skill klasörü oluştur.
2. Şu yapıyı koru:
   - `SKILL.md`
   - `agents/openai.yaml`
   - `references/`
   - `scripts/`
3. `scripts/build_skill_manifests.py` içinde `ORDER`, `META`, `DEPENDENCY_GROUPS`, `SYSTEM_TOOLS` ve gerekirse `EXECUTION_PROFILES` alanlarını güncelle.
4. Manifestleri yeniden üret:

```powershell
python scripts\build_skill_manifests.py
```

5. Doğrula:

```powershell
python scripts\validate_skill_manifest.py --format markdown
python -m pytest
```

## Execution Policy Alanları

Her skill manifestinde şu alanlar bulunmalıdır:

- `sandbox_required`
- `execution_mode`
- `max_runtime_seconds`
- `network_access`
- `writes_files`
- `resource_limits`

Harici uygulama, generated script, CAD/BIM/OCR veya dosya dönüşümü içeren skill'lerde `sandbox_required: true` kullanılmalıdır.

## Test Beklentisi

- Her skill en az bir smoke test ile temsil edilmelidir.
- Opsiyonel bağımlılık yoksa script anlaşılır hata veya plan çıktısı üretmelidir.
- Yeni handoff formatı eklenirse `schemas/` altında JSON Schema dosyası eklenmelidir.

## Release Öncesi

Release öncesi şu komutlar geçmelidir:

```powershell
python scripts\validate_skill_manifest.py --format markdown
python -m pytest
python scripts\run_examples.py --scenario quickstart
python scripts\build_release_artifacts.py --version v0.1.0 --output-dir dist\release
```
