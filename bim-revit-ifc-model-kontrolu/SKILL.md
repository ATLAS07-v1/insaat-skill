---
name: bim-revit-ifc-model-kontrolu
description: Revit/IFC/BIM modellerini açık kaynak araçlarla güvenli incelemek, Revit'ten IFC export rotası planlamak, IFC modelinden proje/kat/mahal/eleman/tip/quantity/property verisi çıkarmak, BIM QA raporu ve eksik parametre listesi üretmek için kullanılır.
---

# BIM Revit IFC Model Kontrolü

## Ne Zaman Kullanılır

- Kullanıcı `.ifc`, `.ifczip`, Revit modeli, BIM modeli, IFC export, mahal/kat/eleman listesi veya model QA istediğinde.
- Revit modelinden açık kaynak araçlarla veri çıkarılması gerektiğinde.
- Modelde eleman, mahal, kat, tip, property set, quantity, sınıflandırma, koordinat veya export kalitesi kontrol edileceğinde.
- Metraj, teknik şartname, hakediş, maliyet veya risk skill'leri için BIM kaynak verisi hazırlanacağı zaman.

Bu skill Revit'in yerel `.rvt` dosyasını açık kaynakla kesin okuyormuş gibi davranmaz. Güvenilir açık kaynak ana yol: Revit veya başka BIM aracından IFC export alınır, sonra IFC IfcOpenShell/xBIM/web-ifc/FreeCAD/Bonsai hattıyla kontrol edilir.

## Girdi

- `.ifc`, `.ifczip` veya Revit'ten export edilmiş IFC.
- Varsa `.rvt` için Revit sürümü ve IFC export ayarları.
- Disiplin: mimari, statik, mekanik, elektrik, altyapı, koordinasyon.
- Beklenen kontrol: mahal, kat, eleman, metraj, property set, quantity, koordinat, clash/uyumsuzluk, IDS/teslim gereksinimi.

## Araç Stratejisi

| Durum | İlk tercih | İkinci tercih | Not |
|---|---|---|---|
| IFC parse/veri çıkarımı | IfcOpenShell Python | xBIM | Python hattında ana araç IfcOpenShell. |
| IFC geometry/export | IfcConvert / Bonsai | FreeCAD | Geometry ağırsa kontrollü çalıştır. |
| IFC görsel/model QA | Bonsai Blender add-on | FreeCAD, xeokit | Görsel doğrulama otomatik raporu tamamlar. |
| Revit IFC export | Autodesk revit-ifc | Revit UI, pyRevit | Revit kurulu ve lisanslı ortam gerekir. |
| Revit otomasyon | pyRevit | RevitPythonShell, Dynamo/Revit API | Sadece kullanıcı onayıyla. |
| Web IFC okuma | web-ifc | xeokit | Viewer/web entegrasyonu için. |
| IDS doğrulama | IfcTester | Bonsai/IfcOpenShell ekosistemi | Teslim gereksinimleri için. |
| Model server/version | BIMserver, Speckle | CDE | Proje ölçeğinde ikinci faz. |

## İş Akışı

1. Dosya türünü belirle: IFC, IFCZIP, RVT, model export paketi veya bilinmeyen.
2. RVT ise doğrudan açık kaynak parse iddiası kurma; IFC export planı üret.
3. IFC ise orijinali koru ve çalışma klasöründe rapor üret.
4. Şema ve header kontrolü yap: IFC2x3, IFC4, IFC4x3, authoring tool, timestamp.
5. Proje hiyerarşisini çıkar: IfcProject, IfcSite, IfcBuilding, IfcBuildingStorey, IfcSpace.
6. Eleman türlerini say: wall, slab, door, window, beam, column, roof, stair, flow terminal, distribution element vb.
7. Property set ve quantity set varlığını kontrol et.
8. Kat/mahal/eleman ilişkilerinde eksikleri işaretle.
9. GlobalId, Name, Type, ObjectType, PredefinedType, Tag, Classification ve material alanlarını kontrol et.
10. Koordinat/georeferencing ve unit bilgilerini bayrakla.
11. Görsel QA gerekiyorsa Bonsai/FreeCAD/xeokit/web-ifc rotası öner.
12. Sonraki skill önerisini üret: metraj, teknik şartname, teklif/maliyet, hakediş, risk veya doküman formatlama.

## Çıktı Formatı

```markdown
## BIM Dosya Özeti

## Araç Rotası

## Proje Hiyerarşisi

## Eleman / Tip / Mahal Özeti

## Property ve Quantity Kontrolü

## Koordinat / Birim / Export QA Bayrakları

## Eksik Parametre Listesi

## Model Revizyon / Teslim Notları

## Sonraki Skill Önerisi
```

Makine çıktısı için `references/cikti-semalari.md` içindeki JSON şemalarını kullan.

## Kalite Kapısı

- RVT dosyası için açık kaynak doğrudan veri çıkarımı kesin kabul edilmez; IFC export veya Revit API gerekir.
- IFC export tek başına Revit modelinin birebir temsili sayılmaz; export ayarları rapora yazılır.
- Quantity değerleri varsa kaynak property/quantity set adıyla yazılır; yoksa geometri tabanlı hesap ayrıca bayraklanır.
- Unit, storey, space containment, material ve classification eksikleri kalite bayrağıdır.
- Görsel model QA yapılmadan geometry eksiksiz kabul edilmez.
- Revit/pyRevit/RevitPythonShell işlemleri kullanıcı onayı ve yerel Revit kurulumu olmadan çalıştırılmaz.

## Onay Sınırı

- Resmi proje uygunluğu, statik/MEP teknik doğruluk, iş güvenliği, ruhsat/standart uyumluluğu ve sözleşmesel teslim kabulü insan uzman onayı gerektirir.
- Bu skill'in çıktısı BIM veri/QA hazırlığıdır; imzalı proje kontrol raporu değildir.

## Referanslar

- Açık kaynak araştırması: `references/acik-kaynak-arastirma.md`
- Araç seçim matrisi: `references/arac-secim-matrisi.md`
- IFC model kontrol listesi: `references/ifc-model-kontrol-listesi.md`
- Revit IFC export notları: `references/revit-ifc-export-notlari.md`
- IDS ve teslim gereksinimi notları: `references/ids-ve-teslim-gereksinimi.md`
- Çıktı şemaları: `references/cikti-semalari.md`

## Scriptler

- `scripts/check_bim_tools.py`: sistemde kullanılabilir BIM/IFC araçlarını kontrol eder.
- `scripts/inspect_ifc_ifcopenshell.py`: IfcOpenShell varsa IFC proje, kat, mahal, eleman ve property/quantity özetini JSON üretir.
- `scripts/plan_revit_ifc_export.py`: RVT veya Revit kaynaklı model için güvenli IFC export planı üretir.
