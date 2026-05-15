# Formatlar ve Entegrasyon

## Girdi Formatları

| Format | Kullanım | Not |
|---|---|---|
| `.blend` | Blender kaynak sahne | En yüksek sadakat |
| `.ifc` | BIM model | Bonsai/IfcOpenShell ile aç |
| `.dxf` | CAD çizim | Önce CAD skill ile QA |
| `.obj` | Mesh/geometri | Materyal kaybı olabilir |
| `.fbx` | Model/asset transfer | Ölçek ve materyal kontrolü gerekir |
| `.glb/.gltf` | Web/modern 3D transfer | Müşteri preview için iyi |
| `.stl` | 3D baskı/mesh | Materyal yoktur |
| `.png/.jpg/.exr` | Render çıktı | Kalite/çözünürlük kontrolü gerekir |

## Çıktı Formatları

- `.blend`: çalışma sahnesi.
- `.png`: sunum renderı.
- `.glb`: hafif paylaşılabilir 3D model.
- `.fbx/.obj`: başka 3D yazılımlara transfer.
- `.stl`: sadece mesh/üretim benzeri çıktı; inşaat sunumu için sınırlı.

## Entegrasyon

- IFC: `bim-revit-ifc-model-kontrolu`
- CAD/DXF: `cad-autocad-dwg-dxf-isleme`
- Tasarım brief'i: `insaat-tasarim-ve-konsept`
- Müşteri sunum metni: `musteri-ve-taseron-iletisim-hazirlayici`
- Doküman: `dokuman-standartlastirma-ve-formatlama`
