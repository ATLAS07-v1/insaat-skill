# Changelog

Bu dosya, yayınlanabilir repo sürümlerindeki kullanıcıya dönük değişiklikleri takip eder.

## v0.1.1 - 2026-05-15

v0.1.0 sonrası agent denetim raporlarına göre mini sertleştirme sürümü.

- Ortak `schemas/handoff-envelope.schema.json` zarfı eklendi.
- Manifest validator'a çapraz execution policy kontrolleri eklendi.
- Release ZIP'i açıp paketin içinden manifest validator ve quickstart çalıştıran `scripts/verify_release_package.py` eklendi.
- CI ve release workflow'ları release paketini içerden doğrulayacak şekilde genişletildi.
- MIT `LICENSE` eklendi ve paket çıktısına dahil edildi.
- Ortam araç uygunluğu için kök `scripts/check_system_tools.py` eklendi.
- CAD/BIM/Blender/SketchUp/fotoğraf kanıt akışları için hedefli smoke/fixture testleri eklendi.
- Sistem araç, lisans, handoff envelope ve release doğrulama dokümantasyonu güncellendi.

## v0.1.0 - 2026-05-15

İlk yayınlanabilir inşaat skill seti.

- 17 yetenek skill'i eklendi: araç kullanımı, CAD, BIM/IFC, Blender, SketchUp, dosya dönüşümü, hesaplama, metraj/mahal, teknik şartname, konsept, teklif/maliyet, hakediş, tedarik, risk/uygunluk, iletişim, saha fotoğrafı ve doküman standardizasyonu.
- Her skill için `SKILL.md`, `references/`, `scripts/` ve `agents/openai.yaml` manifest düzeni oluşturuldu.
- `skill-index.json` ve `manifest.schema.json` ile makine-okunur skill index yapısı eklendi.
- Python bağımlılık grupları, sistem araçları matrisi ve kurulum notları eklendi.
- Manifest doğrulama, smoke testler ve GitHub Actions test hattı eklendi.
- Paketleme ve kurulum araçları eklendi: `scripts/package_skills.py`, `scripts/install_skills.py`.
- Quickstart örnek senaryosu ve `scripts/run_examples.py` eklendi.
- Execution safety alanları eklendi: `sandbox_required`, `execution_mode`, `max_runtime_seconds`, `network_access`, `writes_files`, `resource_limits`.
- JSON Schema tabanlı manifest/index doğrulaması eklendi.
- Skill routing, handoff schema ve bilinen kapsam sınırları dokümante edildi.
- Her skill'i temsil eden CLI smoke kapsamı ve release artifact testleri genişletildi.

## Unreleased

- Henüz yayınlanmamış değişiklik yok.
