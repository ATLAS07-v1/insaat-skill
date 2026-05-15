---
name: cad-autocad-dwg-dxf-isleme
description: AutoCAD kaynaklı DWG/DXF çizimlerini açık kaynak araçlarla güvenli incelemek, DWG'yi DXF'e dönüştürme rotası seçmek, DXF layer/block/entity/ölçü/mahal/ölçek kontrolü yapmak, çizim QA raporu ve revizyon-markup listesi üretmek için kullanılır.
---

# CAD AutoCAD DWG/DXF İşleme

## Ne Zaman Kullanılır

- Kullanıcı DWG, DXF, AutoCAD çıktısı, plan, kesit, görünüş, detay çizimi veya çizim revizyonu verdiğinde.
- Çizimde layer, block, text, ölçü, mahal, entity, modelspace/paperspace veya ölçek kontrolü gerektiğinde.
- DWG dosyasının açık kaynak araçlarla dönüştürülüp analiz edilmesi gerektiğinde.
- Metraj, mahal kontrolü, teknik şartname kontrolü veya teklif öncesi CAD verisi hazırlanacağı zaman.

Bu skill mimari/teknik onay vermez. Çizimi işler, kanıtlı veri çıkarır, kalite bayrağı koyar ve sonraki skill'e hazırlar.

## Girdi

- `.dxf` veya `.dwg` dosyası.
- Varsa çizim disiplini: mimari, statik, mekanik, elektrik, altyapı, peyzaj.
- Varsa beklenen birim, ölçek, revizyon, mahal listesi veya iş kalemi listesi.
- Kullanıcının izin verdiği araçlar: yalnızca açık kaynak, AutoCAD kurulu, FreeCAD kurulu, .NET kullanılabilir vb.

## Araç Stratejisi

| Durum | İlk tercih | İkinci tercih | Not |
|---|---|---|---|
| DXF okuma/analiz | ezdxf | libdxfrw, IxMilia.Dxf, ACadSharp | Python hattı için ezdxf ana araçtır. |
| DXF render/export | ezdxf draw | LibreCAD, FreeCAD | PNG/SVG/PDF ön izleme için kullan. |
| DXF audit | ezdxf audit | LibreCAD aç-kontrol | Hatalı entity ve struktur sorunlarını raporla. |
| Büyük DXF | ezdxf iterdxf | C++/.NET araç | Bellek riski varsa streaming kullan. |
| DWG dönüştürme | LibreDWG `dwg2dxf` | FreeCAD/LibreCAD/libdxfrw | Dönüşüm sonrası QA zorunlu. |
| DWG doğrudan okuma | ACadSharp veya LibreDWG | AutoCAD COM, kullanıcı onaylı | DWG kapalı/proprietary format olduğu için kesinlik iddiası yapma. |
| GUI kontrol | LibreCAD | FreeCAD | İnsan gözüyle layer/ölçek/eksik geometri kontrolü. |
| AutoCAD kuruluysa | pyautocad/COM veya AutoLISP | DXF export + ezdxf | Sadece kullanıcı ortamında ve onayla. |

## İş Akışı

1. Dosya türünü belirle: DWG, DXF, PDF'e basılmış çizim veya bilinmeyen.
2. Orijinali değiştirme; çalışma kopyası veya çıktı klasörü kullan.
3. DWG ise önce dönüştürme rotası seç: `dwg2dxf`, FreeCAD, LibreCAD veya AutoCAD export.
4. DXF ise `ezdxf` ile açmayı dene; olmazsa `recover`/audit veya alternatif araç öner.
5. Header/birim/versiyon/modelspace/paperspace bilgisini çıkar.
6. Layer, block, text, dimension, hatch, polyline, line, circle, arc, insert sayımlarını çıkar.
7. Ölçü ve metraj için kullanılabilecek entity'leri işaretle; birim doğrulanmadıkça kesin metraj üretme.
8. Mahal ve not metinlerini ayır: oda adı, mahal kodu, açıklama, revizyon notu, pafta etiketi.
9. Kalite sorunlarını bayrakla: kapalı olmayan polyline, eksik unit, bilinmeyen scale, proxy entity, xref, image underlay, wipeout, hatch kaybı.
10. Çıktıyı üret: CAD kontrol raporu, entity özeti, layer/block tablosu, markup listesi ve sonraki skill önerisi.

## Çıktı Formatı

```markdown
## CAD Dosya Özeti

## Araç Rotası

## Layer / Block / Entity Özeti

## Mahal ve Text Çıkarımı

## Ölçü / Metraj Adayları

## Dönüşüm ve QA Bayrakları

## Revizyon / Mark-up Listesi

## Sonraki Skill Önerisi
```

Makine çıktısı için `references/cikti-semalari.md` içindeki JSON şemalarını kullan.

## Kalite Kapısı

- DWG'den gelen DXF, dönüşüm sonrası orijinalle görsel/istatistiksel QA almadan kesin kabul edilmez.
- Birim ve ölçek doğrulanmadan alan, uzunluk veya adet hesapları kesinleştirilmez.
- XREF, proxy entity, image underlay, custom object, hatch ve dimension style kaybı özellikle raporlanır.
- Modelspace ile paperspace ayrımı korunur.
- CAD dosyasında revizyon tarihi/pafta adı/ölçek birden fazla yerde farklıysa çatışma olarak yazılır.
- AutoCAD/COM/AutoLISP yalnızca kullanıcı onayı ve yerel kurulum varsa kullanılır.

## Onay Sınırı

- Statik/mimari/MEP teknik doğruluk, resmi proje uygunluğu, uygulama onayı ve iş güvenliği kararı insan uzman onayı gerektirir.
- Bu skill'in çıktısı uygulama projesi değil, analiz ve hazırlık çıktısıdır.

## Referanslar

- Açık kaynak araştırması: `references/acik-kaynak-arastirma.md`
- Araç seçim matrisi: `references/arac-secim-matrisi.md`
- DXF entity kontrol listesi: `references/dxf-entity-kontrol-listesi.md`
- DWG dönüşüm QA: `references/dwg-donusum-qa.md`
- AutoCAD otomasyon notları: `references/autocad-otomasyon-notlari.md`
- Çıktı şemaları: `references/cikti-semalari.md`

## Scriptler

- `scripts/check_cad_tools.py`: sistemde kullanılabilir CAD araçlarını kontrol eder.
- `scripts/inspect_dxf_ezdxf.py`: ezdxf varsa DXF layer/block/entity/text özetini JSON üretir.
- `scripts/plan_dwg_conversion.py`: DWG için güvenli dönüşüm planı ve komut önerisi üretir.
