# Kalite Kapıları

## Dosya Güvenliği

- Arşiv dosyaları önce listelenir, doğrudan çalıştırılmaz.
- Makro içerebilecek dosyalar işaretlenir.
- Parolalı veya bozuk dosyalar eksik veri olarak raporlanır.
- Kullanıcı onayı olmadan script, macro veya executable çalıştırılmaz.

## Belge ve PDF

- Sayfa numarası ve kaynak dosya olmadan kritik veri kabul edilmez.
- OCR metni kesin ölçü/fiyat gibi kullanılmaz; ikinci kontrol gerekir.
- PDF tablosunda birleşik hücre, satır kayması veya kırılmış tablo varsa kalite bayrağı konur.

## Excel / CSV

- Görünen değer, formül ve boş hücre ayrımı korunur.
- Birim ve para birimi yoksa varsayım yapılmaz.
- Sheet adı ve satır referansı tutulur.

## CAD / BIM

- Ölçek ve birim doğrulanmadan ölçü kesinleştirilmez.
- DWG dönüşümü sonrası layer/entity kaybı kontrol edilir.
- IFC modelinde eksik parametreler ayrıca listelenir.

## Görsel

- Fotoğraftan kesin ölçü çıkarılmaz; ölçü referansı yoksa sadece gözlem yazılır.
- Bulanık, düşük ışıklı veya kısmi görüntülerde güven seviyesi düşürülür.
