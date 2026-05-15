# Malzeme Karşılaştırma Kuralları

## Teknik Kriter Türleri

| Kriter | Örnek | Kontrol |
|---|---|---|
| Minimum değer | basınç dayanımı >= 30 MPa | Teklif değeri minimumu karşılamalı. |
| Maksimum değer | VOC <= 50 g/L | Teklif değeri maksimumu aşmamalı. |
| Aralık | kalınlık 8-10 mm | Teklif değeri aralık içinde olmalı. |
| Metin/eşdeğer | yangın sınıfı A2-s1,d0 | Aynı veya teknik sorumlu onaylı eşdeğer olmalı. |
| Zorunlu belge | CE, TSE, EN test raporu | Belge yoksa kritik bayrak. |
| Marka/model | onaylı marka listesi | Muadil ürün teknik onay ister. |

## Uygunluk Durumları

- `pass`: kriter karşılandı.
- `fail`: kriter karşılanmadı.
- `missing`: teklif/datasheet bilgisi yok.
- `needs_approval`: muadil, belirsiz veya standart yorumu gerekiyor.

## Kritik Bayraklar

- Sertifika eksik.
- Test raporu eksik.
- Teknik değer belirsiz.
- Şartname maddesiyle çelişiyor.
- Fiyat ucuz ama teknik olarak uygunsuz.
- Muadil ürün onayı yok.
- Datasheet tarihi/revizyonu belirsiz.

## Onay Notu

Bu kontrol datasheet/teklif verisine dayanır. Ürün onayı için teknik şartname, proje şartları, numune, laboratuvar testi ve yetkili teknik onay gerekir.
