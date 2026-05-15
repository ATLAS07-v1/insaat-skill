# DXF Entity Kontrol Listesi

## Header

- DXF versiyonu (`$ACADVER`)
- Birim (`$INSUNITS`)
- Extents (`$EXTMIN`, `$EXTMAX`)
- Modelspace/paperspace varlığı

## Tables

- Layers
- Linetypes
- Text styles
- Dimension styles
- Blocks
- UCS / views

## Entity Grupları

| Grup | Entity örnekleri | Kontrol |
|---|---|---|
| Çizgi | LINE, LWPOLYLINE, POLYLINE, ARC, CIRCLE, ELLIPSE, SPLINE | Layer, kapalı/açık, uzunluk/alan adayı |
| Metin | TEXT, MTEXT, ATTRIB, ATTDEF | Mahal, pafta, revizyon, not ayrıştırma |
| Ölçü | DIMENSION, LEADER, MLEADER | Ölçü stili, gerçek değer/metin override |
| Blok | INSERT, BLOCK | Block adı, insert noktası, ölçek, attribute |
| Dolgu | HATCH, SOLID, WIPEOUT | Alan/metraj adayı, dönüşüm kaybı riski |
| Referans | XREF, IMAGE, UNDERLAY | Harici dosya bağımlılığı |
| Proxy | ACAD_PROXY_ENTITY | AutoCAD özel nesne kaybı riski |

## Kalite Bayrakları

- `missing_units`
- `unknown_scale`
- `proxy_entity_present`
- `xref_present`
- `image_underlay_present`
- `open_polyline_for_area`
- `dimension_text_override`
- `modelspace_paperspace_conflict`
- `dwg_conversion_required`
- `dwg_conversion_unverified`
