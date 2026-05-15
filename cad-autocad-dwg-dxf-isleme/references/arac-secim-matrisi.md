# Araç Seçim Matrisi

| İhtiyaç | Araç | Gerekçe | Çıktı |
|---|---|---|---|
| DXF hızlı özet | ezdxf | Python, güçlü DXF API, audit ve CLI desteği | JSON/Markdown entity özeti |
| DXF görsel ön izleme | ezdxf draw | PNG/SVG/PDF üretir | Ön izleme dosyası |
| DXF GUI kontrol | LibreCAD | Hafif 2D CAD ve layer görsel kontrol | İnsan QA notu |
| DWG dönüştürme | LibreDWG `dwg2dxf` | Açık kaynak DWG dönüşüm yolu | DXF çalışma kopyası |
| DWG/DXF .NET analizi | ACadSharp | DWG ve DXF table/entity modeline erişim | .NET tabanlı rapor |
| DXF uyumluluk alternatifi | IxMilia.Dxf | DXF okuma-yazma ve AutoCAD uyumluluk notları | .NET DXF kontrolü |
| Geniş CAD dönüşüm | FreeCAD | Python API, import/export ve görsel kontrol | CAD QA/dönüşüm notu |
| 2D geometri alan/ilişki | Shapely | Polygon/line geometri analizi | Alan, kesişim, geçersiz geometri notu |

## Basit Karar Ağacı

1. Dosya `.dxf` mi?
   - Evet: `ezdxf` ile aç, audit et, özet çıkar.
   - Hayır: 2. adıma geç.
2. Dosya `.dwg` mi?
   - Evet: `dwg2dxf` veya FreeCAD/LibreCAD ile çalışma kopyası üret, sonra `ezdxf` ile analiz et.
   - Hayır: `insaat-arac-kullanimlari` skill'ine geri dön.
3. Çıktı metraj için mi?
   - Birim/ölçek doğrulanmadan sadece aday metraj çıkar.
4. Çıktı revizyon için mi?
   - Entity farkı ve görsel QA olmadan kesin fark raporu yazma.
