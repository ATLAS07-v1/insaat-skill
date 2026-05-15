# Release Süreci

Bu repo için release çıktısı, aynı paketleme aracından üretilen zip arşivi ve checksum dosyasıdır.

## Yerel Release Artifact Üretimi

```powershell
python scripts\build_release_artifacts.py --version v0.1.1 --output-dir dist\release
python scripts\verify_release_package.py dist\release\insaat-skill-seti.zip --work-dir dist\release-verify
```

Üretilen dosyalar:

- `dist/release/insaat-skill-seti.zip`
- `dist/release/SHA256SUMS.txt`
- `dist/release/release-metadata.json`
- `dist/release/release-notes.md`

## GitHub Release

Tag push ile otomatik release:

```powershell
git tag v0.1.1
git push origin v0.1.1
```

GitHub Actions `Release` workflow'u testleri çalıştırır, release artifact'lerini üretir ve GitHub release'e yükler.

Manual dispatch için Actions sekmesinden `Release` workflow'u çalıştırılıp `version` alanına `v0.1.1` gibi bir tag adı verilebilir.

## Yayın Öncesi Kontrol

Release öncesinde şu kontrollerin geçmesi beklenir:

```powershell
python scripts\validate_skill_manifest.py --format markdown
python -m pytest
python scripts\run_examples.py --scenario quickstart
python scripts\build_release_artifacts.py --version v0.1.1 --output-dir dist\release
python scripts\verify_release_package.py dist\release\insaat-skill-seti.zip --work-dir dist\release-verify
```

`SHA256SUMS.txt` dosyasındaki hash, yayımlanan zip arşivinin bütünlük kontrolü için kullanılmalıdır.
