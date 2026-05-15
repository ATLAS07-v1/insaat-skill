---
name: insaat-tasarim-ve-konsept
description: İnşaat, mimari, arsa, yerleşim, kütle, mahal programı, konsept alternatifleri, erken sürdürülebilirlik, tasarım brief'i, sunum taslağı ve açık kaynak tasarım araç rotası üretmek için kullanılır.
---

# İnşaat Tasarım ve Konsept

## Ne Zaman Kullanılır

- Kullanıcı inşaat/mimari konsept, arsa yerleşimi, kütle alternatifi, mahal programı, ilk tasarım fikri, cephe dili, iç mekan yaklaşımı veya proje hikayesi istediğinde.
- Metin brief'inden tasarım problemi, varsayımlar, program, kısıtlar, konsept seçenekleri ve karar matrisi çıkarılacağında.
- Arsa boyutu, emsal, TAKS/KAKS, kat adedi, fonksiyon, hedef alan, güneş/yön/rüzgar/bağlam gibi erken verilerle alternatif kütle üretilmesi gerektiğinde.
- FreeCAD, Blender/Bonsai, SketchUp, QGIS, OSMnx, Ladybug/Honeybee, OpenStudio/EnergyPlus veya IFC tabanlı açık kaynak rotası seçileceğinde.
- Tasarım çıktısı başka skill'lere devredilecekse: CAD çizim, BIM model, Blender render, SketchUp kütle, metraj veya teknik şartname kontrolü.

Bu skill konsept ve ön tasarım üretir. Ruhsat projesi, uygulama projesi, statik/MEP hesabı, yangın/imar kesin uygunluğu, mali bağlayıcı keşif veya resmi onay üretmez.

## Girdi

- Proje türü: konut, ofis, ticari, karma, endüstri, eğitim, sağlık, otel, depo, şantiye yerleşimi veya iç mekan.
- Arsa/veri: ölçüler, alan, cepheler, yol, komşular, kuzey, kot, eğim, manzara, iklim, imar notları, çekme mesafeleri.
- Program: mahal listesi, net/brüt alan hedefleri, kapasite, kat adedi, otopark, servis, sirkülasyon, açık alan.
- Tasarım hedefleri: ekonomik, prestij, hızlı inşaat, sürdürülebilirlik, doğal ışık, esneklik, modülerlik, marka dili.
- Hedef çıktı: konsept raporu, alternatif tablo, kütle brief'i, JSON tasarım opsiyonları, SketchUp/Blender/FreeCAD script rotası, sunum metni.

## Araç Stratejisi

| Durum | İlk tercih | İkinci tercih | Not |
|---|---|---|---|
| Parametrik kütle/konsept | FreeCAD / BIM Workbench | Blender/Bonsai | Açık kaynak, parametre ve IFC rotası güçlüdür. |
| Görsel konsept ve render | Blender skill'i | SketchUp skill'i | Malzeme, ışık, kamera ve sunum görseli için. |
| Hızlı kütle ve sahne brief'i | SketchUp skill'i | Blender script | Kapalı kaynak lisans varsa açıkça belirtilir. |
| Arsa ve kent bağlamı | QGIS / GeoPandas / OSMnx | Shapely stdlib fallback | OSM lisansı ve veri kalitesi bayraklanır. |
| Gün ışığı/enerji ön fikir | Ladybug/Honeybee | OpenStudio/EnergyPlus | Erken aşama performans göstergesidir, kesin enerji raporu değildir. |
| Mekansal/topolojik analiz | TopologicPy | COMPAS | Komşuluk, erişim, bağlantı ve topoloji kontrolü. |
| Veri paylaşımı | IFC / IfcOpenShell | Speckle | Platformlar arası tasarım verisi ve revizyon akışı. |
| Alternatif puanlama | JSON/CSV + script | spreadsheet skill | Kriter ağırlıklı tasarım kararı için. |

## İş Akışı

1. Brief'i netleştir: proje tipi, kullanıcı hedefi, arsa, program, kısıtlar, çıktı formatı ve tasarım sınırları.
2. Eksik kritik bilgiyi bayrakla: ölçü, kuzey, imar, çekme mesafesi, kot/eğim, hedef alan, bütçe, teslim düzeyi.
3. Tasarım stratejisini seç: arsa yerleşimi, kütle alternatifi, mahal bloklama, cephe konsepti, performans konsepti veya sunum hikayesi.
4. Alternatif üret: en az 2-4 seçenek; her biri için fikir, kütle mantığı, artı/eksi, risk, alan/kaplama metriği ve uygun araç rotası.
5. Performans ön filtresi uygula: güneş/yön, gölge, doğal ışık, rüzgar, açık alan, erişim, servis, yapım kolaylığı, maliyet karmaşıklığı.
6. Program ve mahal ilişkisini kontrol et: giriş, servis, sirkülasyon, çekirdek, ıslak hacim, teknik hacim, otopark ve açık alan.
7. Çıktıyı üret: konsept karar matrisi, tasarım brief'i, kütle üretim parametreleri, görsel/render brief'i ve sonraki skill rotası.
8. Onay sınırını yaz: konsepttir; resmi imar, ruhsat, statik/MEP, yangın ve uygulama projesi için uzman doğrulaması gerekir.

## Çıktı Formatı

```markdown
## Tasarım / Konsept Özeti

## Kaynak Veriler ve Varsayımlar

## Tasarım Hedefleri

## Alternatifler

## Alan / Kütle / Program Kontrolü

## Erken Performans Notları

## Karar Matrisi

## Araç Rotası

## Riskler ve Onay Sınırı

## Sonraki Skill Önerisi
```

Makine çıktısı için `references/cikti-semalari.md` içindeki JSON şemalarını kullan.

## Kalite Kapısı

- Arsa ölçüsü, birim ve kuzey bilgisi yoksa kütle "temsili" olarak işaretlenir.
- İmar, çekme mesafesi, yükseklik, yangın ve otopark şartları doğrulanmadıysa alternatifler resmi uygunluk iddiası taşımaz.
- Alan metriklerinde net/brüt, emsal alanı ve toplam inşaat alanı ayrımı açık yazılır.
- Her alternatifin artısı, eksisi, riskleri ve uygun araç rotası bulunmalıdır.
- Performans analizi erken aşama göstergedir; EnergyPlus/OpenStudio/Ladybug sonucu yoksa "simülasyonsuz ön değerlendirme" denir.
- Açık kaynak veri kullanılırken OSM/veri lisansı, doğruluk ve güncellik riski belirtilir.
- Konsept tasarım çıktısı başka teknik skill'e devredilecekse hedef format ve varsayımlar korunur.

## Referanslar

- Açık kaynak araştırması: `references/acik-kaynak-arastirma.md`
- Araç seçim matrisi: `references/arac-secim-matrisi.md`
- Konsept iş akışı: `references/konsept-is-akisi.md`
- Yerleşim ve kütle kuralları: `references/yerlesim-ve-kutle-kurallari.md`
- Performans ve sürdürülebilirlik notları: `references/performans-ve-surdurulebilirlik-notlari.md`
- Çıktı şemaları: `references/cikti-semalari.md`

## Yardımcı Scriptler

- `scripts/check_design_tools.py`: tasarım/konsept araç ve Python modül durumunu raporlar.
- `scripts/plan_design_concept_route.py`: iş tipine göre tasarım rotası, araçlar ve sonraki skill önerisi üretir.
- `scripts/generate_concept_options.py`: JSON brief'inden konsept kütle/yerleşim alternatifleri ve metrikler üretir.
- `scripts/score_design_options.py`: alternatifleri ağırlıklı kriterlerle puanlar ve karar matrisi çıkarır.
