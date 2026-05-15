# Mahal QA Kontrol Listesi

## Zorunlu Alanlar

- Mahal kodu veya mahal adı.
- Kat/seviye bilgisi.
- Net alan veya brüt alan.
- Kaynak ve revizyon bilgisi.

## Tek Kaynak Bayrakları

- Eksik mahal adı/kodu.
- Duplicate mahal kodu.
- Aynı kat içinde duplicate mahal adı.
- 0 veya negatif alan/hacim/adet.
- Aşırı büyük/küçük alan.
- Net/brüt alan karışıklığı.
- Birim eksikliği.
- Kat/seviye boşluğu.

## IFC Bayrakları

- `IfcSpace` yok veya sayısı beklenenden düşük.
- `IfcSpace` storey ilişkisi eksik.
- `BaseQuantities` yok.
- NetFloorArea/GrossFloorArea karışık.
- Space name/long name boş.
- Quantity set adı tutarsız.

## PDF/Tablo Bayrakları

- PDF scanned veya OCR gerektiriyor.
- Tablo extraction accuracy düşük.
- Kolon başlıkları belirsiz.
- Ondalık ayracı ve binlik ayracı karışık.
- Birden fazla sayfada bölünen tablolar var.
