# Format Rotaları

## CAD 2D

- `.dwg` -> `.dxf`: LibreDWG `dwg2dxf`; sonra DXF QA.
- `.dxf` -> `.svg/.pdf/.png`: ezdxf draw veya LibreCAD export; çıktı görsel QA.
- `.dxf` -> `.geojson/.gpkg`: GDAL/OGR, sadece uygun geometri ve CRS varsa.

## BIM

- `.ifc` -> `.glb/.obj/.dae/.stp/.igs/.svg`: IfcConvert.
- `.ifczip` -> `.ifc`: IfcOpenShell-Python veya zip çıkarma sonrası IFC QA.
- `.rvt` -> `.ifc`: Revit/export gerekir; açık kaynak doğrudan güvenilir rota yoktur.

## Solid CAD ve Mesh

- `.step/.stp/.iges/.igs/.brep` -> `.stl/.obj/.glb`: FreeCAD/OCCT/Mayo.
- `.stl/.obj/.fbx/.dae/.3mf` -> `.glb/.obj/.stl`: Assimp veya Blender.
- `.glb/.gltf`: glTF Validator ile schema ve asset kontrolü.

## PDF ve Görsel

- `.pdf` -> yapı QA: qpdf, PyMuPDF.
- `.pdf` -> raster: MuPDF `mutool draw`, Poppler `pdftoppm`, ImageMagick.
- `.svg` -> `.pdf/.png`: Inkscape.
- `.png/.jpg/.tiff/.webp`: ImageMagick.

## Kapalı Format Uyarısı

- `.rvt`, `.skp`, modern `.dwg`, bazı `.fbx` ve üreticiye özgü objeler açık kaynak araçlarla eksiksiz dönmeyebilir.
- Bu dosyalarda önce kaynak uygulamadan IFC/DXF/OBJ/FBX/GLB gibi nötr formata export alınması önerilir.
