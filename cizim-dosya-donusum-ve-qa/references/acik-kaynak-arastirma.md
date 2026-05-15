# Açık Kaynak Araştırması

Bu skill, tek bir evrensel dönüştürücü varsaymaz. İnşaat dosyaları farklı geometri, metadata, layer, property, sayfa ve lisans modellerine sahiptir. Bu yüzden en iyi yaklaşım, formata göre açık kaynak araç zinciri seçmek ve her dönüşümden sonra QA yapmaktır.

## Ana Referanslar

| Kaynak | Rol | Skill'e Alınan İlke |
|---|---|---|
| https://github.com/LibreDWG/libredwg | DWG okuma/yazma, DXF/SVG/JSON dönüşüm araçları | DWG kapalı formattır; LibreDWG iyi ilk açık kaynak denemedir ama sürüm/obje kaybı bayraklanır. |
| https://github.com/mozman/ezdxf | Python DXF okuma/yazma/render | DXF manifesti, entity/layer kontrolü ve basit PDF/SVG/PNG üretiminde güçlüdür. |
| https://github.com/LibreCAD/LibreCAD | 2D CAD, DXF/PDF/SVG akışı | 2D çizim kontrolü ve manuel görsel QA için iyi açık kaynak masaüstü aracı. |
| https://github.com/IfcOpenShell/IfcOpenShell | IFC parsing/geometri/IfcConvert | IFC -> OBJ/DAE/GLB/STP/IGS/SVG dönüşümü için ana açık BIM hattı. |
| https://github.com/FreeCAD/FreeCAD | 3D parametrik CAD ve çoklu import/export | STEP/IGES/STL/OBJ/IFC gibi solid/mesh dönüşümlerinde ana masaüstü/CLI hattı. |
| https://github.com/Open-Cascade-SAS/OCCT | CAD kernel, STEP/IGES/STL/BREP | Solid CAD dönüşümlerinde geometri çekirdeği ve veri değişim temeli. |
| https://github.com/assimp/assimp | Genel 3D model import/export | OBJ/FBX/DAE/STL/3MF/GLTF gibi mesh formatları arasında ara dönüştürücü. |
| https://github.com/KhronosGroup/glTF-Validator | GLB/GLTF doğrulama | Web/AR/3D teslimlerinden önce GLB/GLTF schema ve asset QA. |
| https://github.com/qpdf/qpdf | PDF yapı dönüştürme/onarım | PDF bozukluk, şifre, linearize, split/merge ve yapı kontrolü. |
| https://github.com/ArtifexSoftware/mupdf | PDF render/clean/show araçları | PDF sayfa render ve yapısal inceleme için `mutool`. |
| https://github.com/ImageMagick/ImageMagick | Raster/görsel dönüşüm | PNG/JPG/TIFF/WebP ve PDF raster render sonrası görüntü dönüştürme. |
| https://github.com/OSGeo/gdal | Raster/vector/GIS çevirici | KML/GeoJSON/GPKG/DXF ve koordinat sistemli veriler için OGR/GDAL hattı. |

## Hibrit Sonuç

1. Dosya türü belirlenmeden dönüşüm komutu önerilmez.
2. Kapalı formatlar için açık kaynak araç denenir ama kayıpsızlık garanti edilmez.
3. Solid CAD, mesh 3D, BIM IFC, 2D CAD ve PDF ayrı rotalara ayrılır.
4. Dönüşüm sonrası QA zorunludur: sadece dosya üretmek başarı sayılmaz.
5. Karmaşık formatlarda ilgili uzman skill'e yönlendirme yapılır: CAD, BIM, Blender, SketchUp.
