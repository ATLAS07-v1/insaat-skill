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

## Güvenlik ve Onay Sınırı

Bu skill seti teknik, mali, hukuki, İSG veya sözleşmesel nihai onay üretmez. Çıktılar ön analiz, taslak, kontrol listesi ve karar destek amaçlıdır. Yetkili mühendis, İSG uzmanı, hukuk, finans veya proje yönetimi onayı gereken noktalarda skill dosyalarındaki guardrail'ler esas alınmalıdır.
