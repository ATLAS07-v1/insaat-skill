# İnşaat Skill Seti

Hermes/Codex benzeri agent'lerin kopyalayıp kullanabileceği inşaat operasyonlarına özel yetenek skill setidir.

Bu paket yönetim agent'leri değil, doğrudan iş yapan yetenek skill'leri içerir: CAD/BIM, Blender/SketchUp, dosya dönüşümü, hesaplama, metraj, teknik şartname, tasarım, teklif, hakediş, tedarik, risk/uygunluk, iletişim, saha fotoğraf kanıtı ve doküman standardizasyonu.

> Uyarı: LLM tarafından üretilen script, CAD/BIM dönüşüm komutu, Blender/SketchUp otomasyonu veya OCR/fotoğraf işleme komutları doğrudan host sistemde çalıştırılmamalıdır. `sandbox_required: true` olan skill'ler izole çalışma dizini, süre limiti ve kullanıcı onayı ile kullanılmalıdır.

## Skill Listesi

- `insaat-arac-kullanimlari`
- `cad-autocad-dwg-dxf-isleme`
- `bim-revit-ifc-model-kontrolu`
- `blender-3d-modelleme-ve-render`
- `sketchup-konsept-ve-kutle-modelleme`
- `cizim-dosya-donusum-ve-qa`
- `insaat-hesaplamalar`
- `metraj-ve-mahal-kontrolu`
- `teknik-sartname-ve-uygulama-kontrolu`
- `insaat-tasarim-ve-konsept`
- `teklif-ve-maliyet-tablolama`
- `hakedis-ve-mutabakat-kontrolu`
- `tedarik-ve-malzeme-karsilastirma`
- `risk-guvenlik-ve-uygunluk-denetimi`
- `musteri-ve-taseron-iletisim-hazirlayici`
- `saha-fotograf-ve-kanit-analizi`
- `dokuman-standartlastirma-ve-formatlama`

## Kullanım

Her klasör bağımsız bir skill olarak düzenlenmiştir:

- `SKILL.md`: skill tetikleme açıklaması ve ana kullanım yönergesi.
- `agents/openai.yaml`: agent metadata.
- `references/`: iş akışı, kaynak araştırması, kontrol kuralları ve çıktı şemaları.
- `scripts/`: deterministik yardımcı kontrol, rota ve hesaplama scriptleri.

Skill'i kullanacak agent ilgili klasörü kendi skill dizinine kopyalayabilir veya doğrudan bu repo içindeki `SKILL.md` dosyasını entrypoint olarak okuyabilir.

## Kurulum

Python 3.10 veya üstü önerilir.

PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Bash:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Domain bağımlılıklarının tamamını kurmak için:

```bash
pip install -e ".[cad,bim,pdf-doc,spreadsheet,image-ocr,data-quality,communication]"
```

Bağımlılık grupları ve sistem araçları için [DEPENDENCIES.md](DEPENDENCIES.md) dosyasına bakın.

Kurulu Python paketleri ve opsiyonel sistem araçlarını raporlamak için:

```powershell
python scripts\check_system_tools.py --format markdown
```

## Kurulum ve Paketleme

Skill'leri bir agent skill klasörüne kopyalamak için:

```powershell
python scripts\install_skills.py --target "C:\path\to\agent\skills" --force
```

Taşınabilir dağıtım paketi ve zip arşivi üretmek için:

```powershell
python scripts\package_skills.py --force
```

Ayrıntılı kurulum ve paketleme adımları için [INSTALL.md](INSTALL.md) dosyasına bakın.

## Örnek Senaryolar

Quickstart örneğini çalıştırmak için:

```powershell
python scripts\run_examples.py --scenario quickstart
```

Örnek girdiler ve açıklamalar [examples/README.md](examples/README.md) altında tutulur. Çıktılar varsayılan olarak `dist/example-runs/` altına yazılır.

## Routing, Sınırlar ve Katkı

- Skill seçim kuralları: [SKILL_ROUTING.md](SKILL_ROUTING.md)
- Bilinen kapsam sınırları: [KNOWN_LIMITATIONS.md](KNOWN_LIMITATIONS.md)
- Yeni skill veya script ekleme süreci: [CONTRIBUTING.md](CONTRIBUTING.md)
- Skill'ler arası JSON handoff şemaları ve ortak zarf: [schemas/](schemas/)
- Lisans: [LICENSE](LICENSE)

## Release

Yayın artifact'lerini yerelde üretmek için:

```powershell
python scripts\build_release_artifacts.py --version v0.1.1 --output-dir dist\release
python scripts\verify_release_package.py dist\release\insaat-skill-seti.zip --work-dir dist\release-verify
```

Release süreci ve tag tabanlı GitHub Actions yayını için [RELEASE.md](RELEASE.md) dosyasına bakın.

## Manifest ve Doğrulama

Kök `skill-index.json` dosyası tüm skill'lerin makine-okunur index'idir. Her skill içinde aynı şemayı kullanan `agents/openai.yaml` manifesti bulunur.

Manifestleri yeniden üretmek için:

```bash
python scripts/build_skill_manifests.py
```

Manifest ve index doğrulaması için:

```bash
python scripts/validate_skill_manifest.py --format markdown
```

## Test ve CI

Yerel smoke testleri çalıştırmak için:

```powershell
python -m pip install -e ".[dev]"
python -m pytest
```

GitHub Actions hattı her push ve pull request için manifest doğrulaması ile pytest smoke testlerini çalıştırır.

## Güvenlik ve Onay Sınırı

Bu skill seti teknik, mali, hukuki, İSG veya sözleşmesel nihai onay üretmez. Çıktılar ön analiz, taslak, kontrol listesi ve karar destek amaçlıdır. Yetkili mühendis, İSG uzmanı, hukuk, finans veya proje yönetimi onayı gereken noktalarda skill dosyalarındaki guardrail'ler esas alınmalıdır.
