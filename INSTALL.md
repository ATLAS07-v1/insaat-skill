# Kurulum ve Dağıtım

Bu repo, Hermes/Codex benzeri agent'lerin skill klasörlerini doğrudan kopyalayarak kullanabileceği şekilde düzenlenmiştir.

## Güvenli Çalıştırma Uyarısı

LLM tarafından üretilen Python/Ruby scriptleri, CAD/BIM dönüşüm komutları, Blender/SketchUp otomasyonları ve OCR/fotoğraf işleme akışları host işletim sisteminde doğrudan çalıştırılmamalıdır. `agents/openai.yaml` içindeki `sandbox_required`, `max_runtime_seconds`, `network_access`, `writes_files` ve `resource_limits` alanları çalışma izni verirken dikkate alınmalıdır.

Agent şu işlemleri kullanıcı onayı olmadan yapmamalıdır: overwrite, silme, üçüncü tarafa gönderim, resmi onay, ödeme, satın alma, hukuki/İSG/teknik bağlayıcı karar.

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

Kurulu Python paketleri, opsiyonel açık kaynak CLI araçları ve manuel kurulum gerektiren ticari/harici araçları raporlamak için:

```powershell
python scripts\check_system_tools.py --format markdown
```

Örnek senaryo kontrolü için:

```powershell
python scripts\run_examples.py --scenario quickstart
```

Release paketi bütünlüğünü kontrol etmek için:

```powershell
python scripts\build_release_artifacts.py --version v0.1.1 --output-dir dist\release
python scripts\verify_release_package.py dist\release\insaat-skill-seti.zip --work-dir dist\release-verify
Get-Content dist\release\SHA256SUMS.txt
```

## Onay Sınırı

Kurulum scripti yalnızca yerel dosya kopyalar. Var olan skill klasörlerini değiştirmek için `--force` açıkça verilmelidir. Üçüncü taraf agent ortamına kurulumdan önce hedef klasörün doğru olduğundan emin olun.
