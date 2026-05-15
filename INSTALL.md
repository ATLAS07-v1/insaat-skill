# Kurulum ve Dağıtım

Bu repo, Hermes/Codex benzeri agent'lerin skill klasörlerini doğrudan kopyalayarak kullanabileceği şekilde düzenlenmiştir.

## En Hızlı Kullanım

Tüm skill setini bir hedef skill klasörüne kopyalamak için:

```powershell
python scripts\install_skills.py --target "C:\path\to\agent\skills" --force
```

Tek bir skill kurmak için:

```powershell
python scripts\install_skills.py --target "C:\path\to\agent\skills" --skill risk-guvenlik-ve-uygunluk-denetimi
```

Yazmadan önce ne yapılacağını görmek için:

```powershell
python scripts\install_skills.py --target "C:\path\to\agent\skills" --dry-run
```

`--target` verilmezse script önce `HERMES_SKILLS_DIR`, sonra `CODEX_HOME\skills` hedefini kullanır.

## Yayın Paketi Üretme

Tüm skill seti için taşınabilir paket ve zip arşivi üretmek için:

```powershell
python scripts\package_skills.py --force
```

Varsayılan çıktı:

- `dist/insaat-skill-seti/`
- `dist/insaat-skill-seti.zip`

Sadece seçili skill'lerden paket üretmek için:

```powershell
python scripts\package_skills.py --output-dir dist --name risk-paketi --skill risk-guvenlik-ve-uygunluk-denetimi --skill saha-fotograf-ve-kanit-analizi --force
```

Paket klasörü repo düzenini korur: `skill-index.json`, `manifest.schema.json`, `scripts/` ve skill klasörleri aynı seviyede kalır. Bu sayede paket açıldıktan sonra `scripts/install_skills.py` doğrudan çalıştırılabilir.

Tam paketlerde `examples/` klasörü de bulunur. Sadece seçili skill paketi üretildiğinde örnekler varsayılan olarak eklenmez; gerekiyorsa `--include-examples` kullanılabilir.

Örnekleri pakete dahil etmeden paket üretmek için:

```powershell
python scripts\package_skills.py --no-examples --force
```

## Kurulum Sonrası Kontrol

Kopyalanan skill klasörlerinde en az şu dosyalar bulunmalıdır:

- `SKILL.md`
- `agents/openai.yaml`
- `references/`
- `scripts/`

Repo veya paket kökünde doğrulama için:

```powershell
python scripts\validate_skill_manifest.py --format markdown
```

Örnek senaryo kontrolü için:

```powershell
python scripts\run_examples.py --scenario quickstart
```

## Onay Sınırı

Kurulum scripti yalnızca yerel dosya kopyalar. Var olan skill klasörlerini değiştirmek için `--force` açıkça verilmelidir. Üçüncü taraf agent ortamına kurulumdan önce hedef klasörün doğru olduğundan emin olun.
