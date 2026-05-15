---
name: blender-3d-modelleme-ve-render
description: İnşaat, mimari, iç mekan, cephe, şantiye ve BIM/IFC bağlamında Blender ile ölçülü 3D kütle model, konsept sahne, uygulama detayı, malzeme/ışık/kamera kurulumu, render/export ve kalite kontrol çıktıları üretmek için kullanılır.
---

# Blender 3D Modelleme ve Render

## Ne Zaman Kullanılır

- Kullanıcı Blender, 3D model, render, kütle model, konsept görsel, iç mekan, cephe, uygulama detayı veya sahne üretimi istediğinde.
- IFC/BIM, CAD/DXF, ölçülü metraj veya tasarım brief'inden 3D anlatım sahnesi hazırlanacağı zaman.
- Müşteri sunumu, teknik açıklama görseli, uygulama öncesi konsept veya hızlı hacim modeli gerektiğinde.
- Blender Python (`bpy`) ile parametrik sahne/model üretimi isteniyorsa.

Bu skill resmi uygulama projesi, statik hesap veya kesin teknik uygunluk kararı vermez. Model, render ve görsel anlatım çıktısı üretir; ölçü/ölçek varsayımlarını açıkça yazar.

## Girdi

- Metin brief'i, mahal/ölçü listesi, konsept, malzeme listesi veya örnek görsel.
- Varsa IFC/DXF/OBJ/FBX/GLB/STL/BLEND dosyası.
- Hedef çıktı: `.blend`, PNG render, GLB/FBX/OBJ/STL export, kamera listesi, modelleme script'i.
- Ölçek, birim, mekan boyutu, kat yüksekliği, malzeme ve istenen atmosfer.

## Araç Stratejisi

| Durum | İlk tercih | İkinci tercih | Not |
|---|---|---|---|
| Kodla ölçülü sahne üretimi | Blender Python `bpy` | BlenderProc | En güvenilir üretim yolu script'tir. |
| Fotogerçekçi render pipeline | BlenderProc | Blender Cycles/EEVEE script | Render otomasyonu ve veri çıktıları için iyi. |
| IFC/BIM model açma | Bonsai / IfcOpenShell | FreeCAD export + Blender import | IFC için açık BIM hattı. |
| CAD/DXF import | Blender resmi add-on'ları, DXF export/import | Önce `cad-autocad-dwg-dxf-isleme` | DXF karmaşıksa önce CAD skill ile temizle. |
| Parametrik mimari geometri | Sverchok | bpy script | Görsel node tabanlı parametrik tasarım için. |
| Hızlı bina kütlesi | Building Tools | bpy script | Floor, door, window, roof, stair gibi hızlı modelleme. |
| Arazi/OSM/topografya | BlenderGIS | QGIS/DEM hazırlığı | Gerçek konumlu kentsel/arsa görselleştirme için. |
| Asset/malzeme | BlenderKit | Yerel asset kütüphanesi | Lisans ve kullanım hakkı ayrıca kontrol edilmeli. |

## İş Akışı

1. Hedefi sınıflandır: konsept, teknik detay, iç mekan, cephe, şantiye, BIM/IFC, arazi veya sunum render.
2. Kaynak veriyi kontrol et: ölçü, birim, ölçek, mahal, kat yüksekliği, malzeme, renk, dosya formatı.
3. Araç rotasını seç: doğrudan `bpy`, BlenderProc, Bonsai, BlenderGIS, Sverchok veya Building Tools.
4. Varsayımları yaz: ölçü yoksa model temsili kabul edilir; kesin metraj/uygulama verisi değildir.
5. Sahne birimini ayarla: metrik, metre/milimetre, ölçek ve origin.
6. Modeli üret veya import et: hacim, duvar, döşeme, açıklık, mobilya, cephe, zemin, peyzaj.
7. Malzeme ve ışık kur: PBR malzeme adları, renk, roughness, cam/metal/ahşap/seramik.
8. Kamera ve render ayarla: lens, çözünürlük, kadraj, görünüş listesi.
9. Export/render üret: PNG, `.blend`, GLB/FBX/OBJ/STL veya script.
10. QA yap: boş sahne, ölçü/ölçek, kamera kadrajı, model görünürlüğü, materyal eksikleri, render dosyası.
11. Sonraki skill öner: tasarım konsept, müşteri iletişimi, metraj, teknik kontrol veya doküman formatlama.

## Çıktı Formatı

```markdown
## Blender İş Özeti

## Kaynak Veri ve Varsayımlar

## Araç Rotası

## Modelleme Adımları

## Malzeme / Işık / Kamera Ayarları

## Üretilen Dosyalar

## Render / Model QA Bayrakları

## Sonraki Skill Önerisi
```

Makine çıktısı için `references/cikti-semalari.md` içindeki JSON şemalarını kullan.

## Kalite Kapısı

- Ölçü, birim ve ölçek net değilse model "temsili" olarak işaretlenir.
- Render üretilirse dosya varlığı, boyut, çözünürlük ve boş görüntü riski kontrol edilir.
- Kamera kadrajı modelin tamamını ya da istenen detayı görmelidir.
- Import edilen IFC/DXF/OBJ/FBX/GLB dosyalarında geometri kaybı veya materyal kaybı bayraklanır.
- Asset ve materyal lisansları müşteri teslimine gömülmeden önce kontrol edilir.
- Blender script'i orijinal kaynak dosyaları overwrite etmez; çıktı klasörü kullanır.

## Onay Sınırı

- Render görseli uygulama projesi veya imalat detayı yerine geçmez.
- Statik, yangın, akustik, MEP, İSG ve resmi proje uygunluğu uzman onayı gerektirir.
- Gerçek müşteri sunumunda marka/asset/lisans kullanımı ayrıca onaylanır.

## Referanslar

- Açık kaynak araştırması: `references/acik-kaynak-arastirma.md`
- Araç seçim matrisi: `references/arac-secim-matrisi.md`
- Blender Python iş akışı: `references/blender-python-is-akisi.md`
- Render kalite kapıları: `references/render-kalite-kapilari.md`
- Format ve entegrasyon notları: `references/formatlar-ve-entegrasyon.md`
- Çıktı şemaları: `references/cikti-semalari.md`

## Scriptler

- `scripts/check_blender_tools.py`: Blender, Node, Python modülleri ve yardımcı araçları kontrol eder.
- `scripts/plan_blender_job.py`: bir Blender iş planı ve komut önerisi üretir.
- `scripts/create_construction_scene.py`: Blender içinde çalışan örnek ölçülü oda/kütle sahnesi script'i.
