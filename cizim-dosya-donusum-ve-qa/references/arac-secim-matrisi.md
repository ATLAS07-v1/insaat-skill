# Araç Seçim Matrisi

| İhtiyaç | Önerilen Araç | İkinci Tercih | Not |
|---|---|---|---|
| DWG -> DXF | LibreDWG `dwg2dxf` | Kaynak CAD uygulaması export'u | DWG sürümü ve obje desteği kontrol edilir. |
| DWG -> SVG/JSON | LibreDWG | CAD skill'i | Görsel/metadata kaybı raporlanır. |
| DXF okuma/QA | ezdxf | LibreCAD | Entity/layer/block sayımı için iyi. |
| DXF -> PDF/SVG/PNG | ezdxf draw, LibreCAD | Inkscape ara SVG | Font/lineweight kaybı kontrol edilir. |
| IFC -> GLB/OBJ/STP/IGS/SVG | IfcConvert | Bonsai/Blender | Büyük koordinat ve property kaybı bayraklanır. |
| STEP/IGES -> STL/OBJ | FreeCADCmd, OCCT | Mayo | Solid to mesh dönüşümünde tessellation kaybı vardır. |
| OBJ/FBX/DAE/STL -> GLB | Assimp, Blender | glTF toolchain | Texture yolu ve normal kontrolü gerekir. |
| GLB/GLTF QA | glTF Validator | Blender import kontrolü | Web tesliminde zorunlu kabul edilir. |
| PDF yapı QA | qpdf | PyMuPDF | Şifre, bozuk xref, sayfa kontrolü. |
| PDF -> PNG | MuPDF/Poppler | ImageMagick | DPI ve rasterleşme açık yazılır. |
| SVG -> PDF/PNG | Inkscape | ImageMagick | Font ve sayfa boyutu kontrol edilir. |
| GIS/CAD vector | GDAL/OGR | QGIS | CRS ve koordinat kaybı kontrol edilir. |
| RVT/SKP | Kaynak uygulama export | IFC/OBJ/FBX ara format | Açık kaynak kayıpsız dönüşüm beklenmez. |

## Varsayılan Güvenlik

- Input dosya salt okunur kabul edilir.
- Output her zaman ayrı klasöre yazılır.
- Hedef formatın kullanım amacı yazılmadan kayıpsızlık iddiası kurulmaz.
- Lisanslı/proprietary araç gerekiyorsa işlem planı olarak kalır; otomatik kullanılmaz.
