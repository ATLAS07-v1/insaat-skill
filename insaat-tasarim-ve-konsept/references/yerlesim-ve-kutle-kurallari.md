# Yerleşim ve Kütle Kuralları

## Kontrol Başlıkları

- Arsa ve yapı oturumu aynı birimde mi?
- Toplam brüt alan hedefi ile kat adedi tutarlı mı?
- Bina oturumu, çekme mesafeleri ve açık alan ihtiyacıyla çelişiyor mu?
- Giriş, servis, otopark ve yangın erişimi için net kurgu var mı?
- Kütle yönlenmesi güneş, rüzgar, manzara ve gürültüyle ilişkilendirildi mi?
- Mahal programı dikey ve yatay sirkülasyonla gerçekçi mi?

## Basit Metrikler

- `gross_floor_area = footprint_area * floors`
- `coverage_ratio = footprint_area / site_area`
- `floor_area_ratio = gross_floor_area / site_area`
- `open_space_ratio = max(site_area - footprint_area, 0) / site_area`
- `average_floor_plate = gross_floor_area / floors`

## Heuristikler

- Kompakt blok: daha düşük cephe maliyeti, daha az ısı kaybı, daha az plan çeşitliliği.
- Avlulu blok: sosyal alan ve ışık potansiyeli yüksek; küçük arsada alan verimi düşebilir.
- Lineer bar: yönlenme ve manzara güçlü; uzun koridor ve servis mesafesi riski vardır.
- Podium tower: yoğunluk sağlar; çekirdek, yangın, rüzgar ve gölge riski erken bayraklanmalıdır.
- Perimetre blok: kentsel cephe ve avlu dengesi sağlar; köşe ve derin plan kalitesi kontrol ister.
- Teraslı kütle: manzara ve eğim için güçlüdür; taşıyıcı ve su yalıtımı karmaşıklığı artar.

## Onay Notu

Bu kurallar konsept filtresidir. İmar, yangın, erişilebilirlik, otopark, statik ve MEP uygunluğu için ilgili mevzuat ve uzman doğrulaması gerekir.
