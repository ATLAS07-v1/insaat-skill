---
name: cizim-dosya-donusum-ve-qa
description: İnşaat, mimari, BIM, CAD, PDF, görsel ve 3D model dosyalarında DWG, DXF, PDF, IFC, RVT, SKP, OBJ, FBX, GLB, STL, STEP, IGES, SVG, PNG ve benzeri formatlar arası dönüşüm rotası, açık kaynak araç seçimi, dosya manifesti ve kalite kontrol raporu hazırlamak için kullanılır.
---

# Çizim Dosya Dönüşüm ve QA

## Ne Zaman Kullanılır

- Kullanıcı çizim, proje, CAD, BIM, PDF, görsel veya 3D dosyalarının format dönüşümünü istediğinde.
- DWG/DXF/PDF/IFC/RVT/SKP/OBJ/FBX/GLB/STL/STEP/IGES/SVG/PNG dosyaları için en güvenli açık kaynak rota seçileceğinde.
- Dönüşüm öncesi dosya manifesti, hash, boyut, uzantı/magic kontrolü ve risk bayrakları çıkarılacağında.
- Dönüşüm sonrası ölçek, geometri, layer/tag, materyal, sayfa, koordinat ve dosya bütünlüğü QA raporu hazırlanacağında.

Bu skill gerçek dönüşüm yapmadan önce rota ve risk belirler. Kapalı/proprietary formatlarda güvenilir dönüşüm için kaynak uygulama lisansı gerekebilir; bu durum açıkça bayraklanır.

## Girdi

- Dosya yolu, klasör yolu veya dosya listesi.
- Kaynak ve hedef format: ör. DWG -> DXF, DXF -> PDF, IFC -> GLB, PDF -> PNG, STEP -> STL, OBJ -> GLB.
- Teslim amacı: arşiv, metraj, render, müşteri sunumu, BIM koordinasyonu, saha paylaşımı, web görüntüleme.
- Ölçek, birim, koordinat sistemi, pafta/sayfa beklentisi, gizlilik ve lisans kısıtları.

## Araç Stratejisi

| Kaynak | Hedef | İlk tercih | QA odağı |
|---|---|---|---|
| DWG | DXF/SVG/JSON | LibreDWG | DWG sürümü, layer, text, block kaybı |
| DXF | SVG/PDF/PNG | ezdxf, LibreCAD, Inkscape | entity sayısı, layer, ölçü, font |
| IFC | GLB/OBJ/DAE/STP/IGS/SVG | IfcOpenShell / IfcConvert | eleman sayısı, koordinat, birim, property kaybı |
| STEP/IGES/BREP | STL/OBJ/GLB | FreeCAD / OCCT / Mayo | solid-mesh kaybı, tessellation, birim |
| OBJ/FBX/DAE/STL | GLB/OBJ/STL | Assimp, Blender | mesh, normal, materyal, texture yolu |
| GLB/GLTF | GLB/GLTF | Khronos glTF Validator | schema, texture, buffer, extension uyumu |
| PDF | PNG/SVG/text/QA | qpdf, MuPDF, Poppler, PyMuPDF | sayfa, şifre, bozuk yapı, raster/vector ayrımı |
| SVG/AI/PDF | PDF/PNG/SVG | Inkscape, ImageMagick | rasterleşme, sayfa boyutu, font |
| raster | PNG/JPG/TIFF/WebP | ImageMagick | çözünürlük, DPI, renk profili |
| GIS/CAD | GeoJSON/KML/GPKG/DXF | GDAL/OGR | CRS, geometri tipi, koordinat kaybı |
| RVT/SKP | IFC/OBJ/FBX/GLB | Kaynak uygulama export'u | kapalı format, lisans, export ayarı |

## İş Akışı

1. Kaynak dosyaları tara: uzantı, boyut, hash, magic byte, klasör yapısı.
2. Dosyaları sınıflandır: CAD, BIM, PDF, raster, vector, mesh, solid CAD, proprietary.
3. Hedef format ve teslim amacını netleştir.
4. Açık kaynak dönüşüm rotasını seç; kapalı format gerekiyorsa bunu ayrı risk olarak yaz.
5. Dönüşüm öncesi QA yap: bozuk/boş dosya, beklenmeyen magic, şifreli PDF, eksik texture, büyük koordinat, eski DWG.
6. Komut planı üret: araç, input, output, güvenli çıktı klasörü, overwrite önlemi.
7. Dönüşüm sonrası QA planı hazırla: dosya varlığı, boyut, sayfa/model/entity sayısı, geometri ve ölçek kontrolü.
8. Gerekirse sonraki skill'e yönlendir: CAD temizliği, BIM kontrolü, Blender render, SketchUp konsept veya metraj.

## Çıktı Formatı

```markdown
## Dönüşüm İş Özeti

## Kaynak Dosya Manifesti

## Hedef Format ve Teslim Amacı

## Önerilen Araç Rotası

## Komut / İşlem Planı

## Dönüşüm Öncesi QA

## Dönüşüm Sonrası QA

## Risk Bayrakları

## Sonraki Skill Önerisi
```

Makine çıktısı için `references/cikti-semalari.md` içindeki JSON şemalarını kullan.

## Kalite Kapısı

- Orijinal dosyalar overwrite edilmez; her dönüşüm ayrı çıktı klasörüne yazılır.
- Her input/output için hash, boyut, uzantı ve tarih bilgisi tutulur.
- Dönüşüm sonrası dosya oluşması tek başına başarı değildir; sayfa/model/entity/geometri kontrolleri yapılır.
- Kapalı formatlar (`.rvt`, `.skp`, bazı `.dwg`, bazı `.fbx`) açık kaynak araçlarla kayıpsız dönüştürülmeyebilir.
- PDF dönüşümünde vector çizimin raster'e dönüşmesi açıkça raporlanır.
- IFC/3D dönüşümünde birim, büyük koordinat, malzeme, property ve eleman kaybı kontrol edilir.
- GLB/GLTF çıktılarında validator raporu alınmadan web teslimi önerilmez.

## Onay Sınırı

- Dönüştürülen dosya resmi proje, ruhsat, imalat veya ihale teslimi için kullanılacaksa teknik sorumlu onayı gerekir.
- Lisanslı/proprietary kaynak uygulama veya eklenti kullanımı kullanıcı onayına ve mevcut lisansa bağlıdır.
- Üçüncü taraf dosyalarda gizlilik, telif ve müşteri verisi kısıtları kontrol edilmeden paylaşım/export yapılmaz.

## Referanslar

- Açık kaynak araştırması: `references/acik-kaynak-arastirma.md`
- Araç seçim matrisi: `references/arac-secim-matrisi.md`
- Format rotaları: `references/format-rotalari.md`
- QA kontrol listesi: `references/dosya-qa-kontrol-listesi.md`
- Dönüşüm riskleri: `references/donusum-riskleri.md`
- Çıktı şemaları: `references/cikti-semalari.md`

## Yardımcı Scriptler

- `scripts/check_conversion_tools.py`: dönüşüm araçlarını ve Python modüllerini kontrol eder.
- `scripts/plan_file_conversion.py`: input/hedef formata göre güvenli dönüşüm rotası ve komut taslağı üretir.
- `scripts/inspect_conversion_package.py`: dosya manifesti, hash, magic byte ve temel QA bayrakları üretir.
