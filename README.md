# İnşaat Skill Seti

Hermes/Codex benzeri agent'lerin kopyalayıp kullanabileceği inşaat operasyonlarına özel yetenek skill setidir.

Bu paket yönetim agent'leri değil, doğrudan iş yapan yetenek skill'leri içerir: CAD/BIM, Blender/SketchUp, dosya dönüşümü, hesaplama, metraj, teknik şartname, tasarım, teklif, hakediş, tedarik, risk/uygunluk, iletişim, saha fotoğraf kanıtı ve doküman standardizasyonu.

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

## Güvenlik ve Onay Sınırı

Bu skill seti teknik, mali, hukuki, İSG veya sözleşmesel nihai onay üretmez. Çıktılar ön analiz, taslak, kontrol listesi ve karar destek amaçlıdır. Yetkili mühendis, İSG uzmanı, hukuk, finans veya proje yönetimi onayı gereken noktalarda skill dosyalarındaki guardrail'ler esas alınmalıdır.
