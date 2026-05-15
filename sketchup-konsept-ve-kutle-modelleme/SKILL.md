---
name: sketchup-konsept-ve-kutle-modelleme
description: İnşaat, mimari, iç mekan, arsa, cephe ve şantiye bağlamında SketchUp ile hızlı konsept, kütle model, yerleşim, sahne/görünüş listesi, Ruby API otomasyonu, SKP/export planı ve model kalite kontrolü hazırlamak için kullanılır.
---

# SketchUp Konsept ve Kütle Modelleme

## Ne Zaman Kullanılır

- Kullanıcı SketchUp, SKP, konsept model, kütle model, hızlı yerleşim, vaziyet, iç mekan taslağı, cephe kütlesi veya görünüş/sahne listesi istediğinde.
- Metin brief'i, mahal listesi, ölçü listesi, arsa bilgisi veya müşteri talebinden temsilî 3D kütle çalışması üretileceğinde.
- SketchUp Ruby API ile model kurma, component/tag/material/page düzeni, export veya otomasyon script'i hazırlanacağı zaman.
- `.skp` teslimi doğrudan üretilemiyorsa SketchUp içinde çalıştırılacak güvenli Ruby script'i ve işlem planı hazırlanacağı zaman.

Bu skill uygulama projesi, statik hesap, ruhsat projesi veya kesin imalat detayı üretmez. Ölçü ve imar bilgisi eksikse çıktı konsept/temsili olarak işaretlenir.

## Girdi

- Metin brief'i, arsa/mahal ölçüleri, kat adedi, kat yüksekliği, yaklaşma mesafesi, cephe yönü, malzeme, kullanım senaryosu.
- Varsa DWG/DXF/PDF/IFC/OBJ/FBX/GLB/STL/SKP dosyaları.
- Hedef çıktı: SketchUp model brief'i, Ruby API script'i, SKP içinde tag/layer yapısı, sahne listesi, export planı, müşteri sunumu görsel brief'i.
- Ölçü birimi, ölçek, teslim formatı, model detay seviyesi ve lisans kısıtları.

## Araç Stratejisi

| Durum | İlk tercih | İkinci tercih | Not |
|---|---|---|---|
| SketchUp içinde model üretimi | SketchUp Ruby API | Ruby API örnekleri + stubs | API yalnız SketchUp içinde çalışır. |
| Hızlı kütle/konsept | Ruby script ile group/component | Manuel SketchUp brief'i | Ölçüler netse script üret. |
| Extension geliştirme | Resmi VSCode SketchUp template | RubyMine setup | RuboCop SketchUp ve stubs önerilir. |
| Test/CI | TestUp 2 | manuel SketchUp kontrol listesi | SketchUp içi testlerde kullanılır. |
| SKP okuma/yazma dış sistem | SketchUp C API / Live C API | SketchUp içinden export | SDK/lisans sınırları kontrol edilir. |
| Enerji/analiz bağlamı | OpenStudio SketchUp Plug-in | IFC/BIM skill hattı | Konsept enerji modeli için. |
| GLB/gltf export | SketchUp glTF Ruby exporter | Blender import/export | Teslim formatı web ise değerlidir. |
| CAD/BIM temizliği | CAD/BIM skill'leri | SketchUp import | Kirli DWG/IFC önce temizlenir. |

## İş Akışı

1. Hedefi sınıflandır: arsa/vaziyet, bina kütlesi, iç mekan, cephe, şantiye, müşteri konsepti veya export.
2. Kaynak veriyi kontrol et: ölçü, birim, kuzey/yön, kot, kat adedi, kat yüksekliği, mahal listesi, imar varsayımları.
3. SketchUp rotasını seç: manuel model brief'i, Ruby API script'i, extension iskeleti, SKP export planı veya başka skill'e yönlendirme.
4. Varsayımları açık yaz: net ölçü yoksa temsili kütle; imar/uygulama kararı değildir.
5. Model organizasyonunu kur: tag/layer, group/component, material, scene/page, section, annotation stratejisi.
6. Kütleleri üret: arsa düzlemi, yapı oturumu, kat blokları, çekme mesafeleri, ana giriş, açıklık/cephe işaretleri.
7. Sahne listesini hazırla: vaziyet, genel perspektif, cephe, kuşbakışı, iç hacim, müşteri sunum açısı.
8. Export planını hazırla: SKP, PNG, PDF, DWG/DXF, OBJ/FBX/GLB/STL ihtiyacına göre.
9. QA yap: ters yüzey, açık yüzey, tag karmaşası, nested group, ölçü sapması, sahne eksikleri, asset/lisans.
10. Sonraki skill öner: Blender render, CAD temizliği, metraj, müşteri iletişimi veya risk/uygunluk denetimi.

## Çıktı Formatı

```markdown
## SketchUp İş Özeti

## Kaynak Veri ve Varsayımlar

## Araç Rotası

## Model Organizasyonu

## Kütle / Yerleşim Adımları

## Sahne ve Görünüş Listesi

## Export / Teslim Planı

## Model QA Bayrakları

## Sonraki Skill Önerisi
```

Makine çıktısı için `references/cikti-semalari.md` içindeki JSON şemalarını kullan.

## Kalite Kapısı

- Ölçü, birim, kuzey/yön ve kat yüksekliği eksikse model "temsili" olarak işaretlenir.
- SketchUp Ruby API yalnız SketchUp içinde çalıştırılır; normal sistem Ruby'si ile `Sketchup` modülü beklenmez.
- Ruby script'i mevcut kullanıcı modelini kaydetmeden önce yeni dosya/çıktı yolu kullanmalı ve overwrite riskini belirtmelidir.
- Grup/component hiyerarşisi okunabilir olmalı; her ana elemanın adı ve tag'i bulunmalıdır.
- Yüzey yönleri, açık yüzeyler, gereksiz nested group ve orphan geometry kontrol edilir.
- Üçüncü taraf component, texture ve plugin lisansları müşteri tesliminden önce kontrol edilir.
- SKP dışı teslimlerde export sonrası geometri, malzeme ve ölçek kaybı bayraklanır.

## Onay Sınırı

- SketchUp konsept modeli ruhsat, uygulama, statik, yangın, akustik, MEP veya İSG uygunluk onayı yerine geçmez.
- İmar koşulları, çekme mesafeleri ve resmi proje kararları uzman/kurum onayı gerektirir.
- Kapalı kaynak SketchUp lisansı, eklenti lisansı ve ticari kullanım şartları ayrıca kontrol edilir.

## Referanslar

- Açık kaynak araştırması: `references/acik-kaynak-arastirma.md`
- Araç seçim matrisi: `references/arac-secim-matrisi.md`
- Ruby API akışı: `references/sketchup-ruby-is-akisi.md`
- Kütle model QA: `references/kutle-model-kalite-kapilari.md`
- Format ve entegrasyon: `references/formatlar-ve-entegrasyon.md`
- Çıktı şemaları: `references/cikti-semalari.md`

## Yardımcı Scriptler

- `scripts/check_sketchup_tools.py`: SketchUp, Ruby, Node ve ilgili geliştirme araçlarını kontrol eder.
- `scripts/plan_sketchup_job.py`: istenen iş türü için SketchUp rota planı ve komut taslağı üretir.
- `scripts/generate_sketchup_massing_ruby.py`: JSON ölçü brief'inden SketchUp içinde çalışacak Ruby kütle model script'i üretir.
