# AutoCAD Otomasyon Notları

Bu skill açık kaynak hattı önce kullanır. AutoCAD kuruluysa ve kullanıcı açıkça izin verirse AutoCAD otomasyonu yardımcı yol olabilir.

## Kullanılabilecek Yollar

| Yol | Kullanım | Sınır |
|---|---|---|
| pyautocad / COM | Windows'ta AutoCAD uygulamasını Python ile kontrol etmek | AutoCAD lisansı ve açık uygulama gerekir. |
| pywin32 COM | Daha düşük seviye COM otomasyonu | Hata yönetimi ve sürüm farkları zor olabilir. |
| AutoLISP | AutoCAD içinde batch komut ve çizim otomasyonu | Kullanıcı onayı olmadan çalıştırılmaz. |
| SCRIPT `.scr` | AutoCAD komutlarını sıralı çalıştırmak | Ortam ve command-line davranışı sürüme göre değişebilir. |

## Ne İçin Kullanılır?

- DWG'yi AutoCAD'in kendi motoruyla DXF'e export etmek.
- Layer freeze/thaw, purge, audit gibi AutoCAD içi işlemleri kullanıcı onayıyla yapmak.
- Pafta çıktılarını üretmek.

## Ne İçin Kullanılmaz?

- Kullanıcı onayı olmadan DWG üzerinde değişiklik yapmak.
- Orijinal dosyayı overwrite etmek.
- Resmi teknik uygunluk kararı vermek.

## Güvenli Prensip

AutoCAD otomasyonu varsa bile analiz mümkün olduğunca export edilmiş çalışma kopyası üzerinden yapılır. Orijinal DWG korunur.
