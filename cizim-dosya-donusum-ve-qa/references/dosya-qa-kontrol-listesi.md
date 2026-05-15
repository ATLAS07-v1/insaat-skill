# Dosya QA Kontrol Listesi

## Ön Kontrol

- Dosya var mı, boş mu, çok büyük mü?
- Uzantı ile magic byte uyumlu mu?
- Hash ve boyut kaydedildi mi?
- Dosya yolu özel karakter, çok uzun path veya senkronizasyon klasörü riski taşıyor mu?
- PDF şifreli mi, bozuk xref içeriyor mu?
- ZIP tabanlı dosya gerçekten açılabiliyor mu?

## CAD/BIM Kontrolü

- DWG/DXF sürümü ve layer listesi alınabiliyor mu?
- DXF içinde `SECTION`, `ENTITIES`, `TABLES`, `BLOCKS` bölümleri var mı?
- IFC içinde STEP header, schema ve entity sayısı okunuyor mu?
- Birim, ölçek, koordinat sistemi ve büyük koordinat riski var mı?

## 3D Kontrolü

- Mesh/solid ayrımı yapıldı mı?
- Vertex/face sayısı ve dosya boyutu makul mü?
- Normal, materyal, texture ve external dependency riski var mı?
- GLB/GLTF validator hataları kayıt altına alındı mı?

## PDF/Görsel Kontrolü

- Sayfa sayısı, sayfa boyutu ve DPI hedefi var mı?
- Vector çizim raster'e çevrildiyse raporlandı mı?
- Font/subset ve çizgi kalınlıkları kontrol edildi mi?

## Teslim Kontrolü

- Output dosyası var mı ve sıfır byte değil mi?
- Output hash ve boyut manifestte var mı?
- Input-output sayfa/model/entity/katman farkı kontrol edildi mi?
- Teslim formatı amaca uygun mu?
