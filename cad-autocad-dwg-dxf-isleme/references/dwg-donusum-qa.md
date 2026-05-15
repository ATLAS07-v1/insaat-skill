# DWG Dönüşüm QA

DWG dosyası açık kaynak araçlarla işlendiğinde dönüşüm sonrası kalite kontrol zorunludur.

## Önerilen Akış

1. Orijinal DWG'yi salt okunur kaynak kabul et.
2. Çalışma klasöründe kopya veya çıktı üret.
3. İlk dönüşüm denemesi:

```powershell
dwg2dxf input.dwg
```

4. Çıkan DXF'i `ezdxf audit` veya `scripts/inspect_dxf_ezdxf.py` ile kontrol et.
5. Mümkünse LibreCAD/FreeCAD ile görsel açılış kontrolü yap.
6. Çıktıda entity sayısı, layer sayısı, block sayısı, xref/proxy bayrakları ve görüntü notunu raporla.

## Kontrol Noktaları

- DWG sürümü destekleniyor mu?
- DXF dosyası oluştu mu?
- DXF açılabiliyor mu?
- Layer sayısı beklenen seviyede mi?
- Text ve dimension entity'leri kaybolmuş mu?
- Hatch veya wipeout kaybı var mı?
- External reference var mı?
- Paperspace viewport'ları korunmuş mu?
- Unit/scale bilgisi okunabiliyor mu?

## Rapor Dili

Kötü:

> DWG başarıyla dönüştü, metraj kesin.

Doğru:

> DWG'den DXF çalışma kopyası üretildi. DXF açıldı ve entity özeti çıkarıldı. Birim/ölçek doğrulanmadığı ve xref bulunduğu için metraj adayı kesin değildir; görsel QA ve kaynak çizim kontrolü gerekir.
