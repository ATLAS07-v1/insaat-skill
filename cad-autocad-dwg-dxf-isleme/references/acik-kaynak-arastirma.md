# Açık Kaynak Araştırması

Bu skill AutoCAD kaynaklı DWG/DXF dosyalarını doğrudan tek bir araca bağlamaz. DWG kapalı/proprietary bir format olduğu için en güvenilir açık kaynak yaklaşım, DWG'yi kontrollü şekilde DXF'e dönüştürmek ve DXF üzerinde güçlü analiz yapmaktır.

## Ana Araçlar

| Araç | Kaynak | Kullanım | Lisans/Not |
|---|---|---|---|
| ezdxf | https://github.com/mozman/ezdxf | DXF okuma, yazma, entity/layer/block analizi, audit, draw/export | MIT. Python hattının ana DXF aracı. |
| LibreDWG | https://github.com/LibreDWG/libredwg | DWG okuma/yazma, `dwg2dxf` dönüşümü, DWG CLI araçları | GPL-3.0. DWG dönüşümü için ana açık kaynak aday. |
| libdxfrw | https://github.com/LibreCAD/libdxfrw | ASCII/binary DXF okuma-yazma, basit DWG okuma | GPL-2.0+. LibreCAD altyapısında kullanılır. |
| LibreCAD | https://github.com/LibreCAD/LibreCAD | 2D CAD GUI, DXF/PDF/SVG çıktı, temel DWG okuma | GUI doğrulama ve insan QA için iyi. |
| FreeCAD | https://github.com/FreeCAD/FreeCAD | Parametrik CAD, Python API, import/export ve görsel kontrol | Daha geniş CAD dönüşüm ve 2D/3D kontrol için yararlı. |
| ACadSharp | https://github.com/DomCR/ACadSharp | .NET ile DXF/DWG okuma-yazma, entity/table çıkarımı | MIT. Windows/.NET hattı için güçlü alternatif. |
| IxMilia.Dxf | https://github.com/ixmilia/dxf | .NET ile DXF/DXB okuma-yazma | AutoCAD uyumluluğuna dair pratik uyarıları iyi. |
| Shapely | https://github.com/shapely/shapely | 2D geometri analizi, polygon/line işlem | DXF entity'leri geometriye çevrildikten sonra alan/ilişki kontrolünde yararlı. |

## Tercih Sırası

### DXF

1. `ezdxf`: İlk tercih.
2. `ezdxf audit`: Struktur ve entity hataları için.
3. `ezdxf draw`: PNG/SVG/PDF görsel çıktı için.
4. `LibreCAD`: GUI ile insan gözü kontrolü.
5. `.NET` gerekiyorsa `ACadSharp` veya `IxMilia.Dxf`.

### DWG

1. `LibreDWG dwg2dxf`: İlk açık kaynak dönüşüm denemesi.
2. `FreeCAD` veya `LibreCAD`: Dönüşüm/GUI kontrol.
3. `ACadSharp`: .NET ortamı uygunsa doğrudan DWG okuma/analiz.
4. AutoCAD kuruluysa: kullanıcı onaylı COM/AutoLISP export, sonra `ezdxf` analizi.

## Neden Bu Hibrit Yol?

- DWG kapalı format olduğu için açık kaynak okuma/dönüşümde geometri, hatch, text, dimension, xref veya custom object kaybı olabilir.
- DXF açık değişim formatıdır ve `ezdxf` gibi araçlarla daha denetlenebilir analiz sağlar.
- GUI araçları otomatik raporu doğrulamak için kullanılır; otomatik çıktı tek başına kesin kabul edilmez.

## Risk Notları

- Dönüşüm başarılı oldu diye çizim eksiksiz kabul edilmez.
- AutoCAD'in kabul ettiği her DXF'i diğer araçlar aynı şekilde yorumlamayabilir.
- Layer isimleri, block insert'leri, paperspace viewport'ları ve xref'ler özellikle QA ister.
- Lisanslar müşteri ürününe gömülmeden önce ayrıca kontrol edilmelidir.
