# Metraj ve Malzeme Formülleri

## Alan ve Hacim

- Dikdörtgen alan: `A = uzunluk * genişlik`
- Duvar yüzeyi: `A = uzunluk * yükseklik - boşluklar`
- Döşeme hacmi: `V = alan * kalınlık`
- Kiriş hacmi: `V = uzunluk * genişlik * yükseklik`
- Kolon hacmi: `V = en * boy * yükseklik * adet`
- Kazı hacmi: `V = uzunluk * genişlik * derinlik`

## Kalıp

- Kolon kalıp: `A = 2 * (en + boy) * yükseklik * adet`
- Kiriş yan kalıp yaklaşık: `A = 2 * yükseklik * uzunluk + alt_genişlik * uzunluk`
- Perde kalıp yaklaşık: `A = 2 * uzunluk * yükseklik`
- Döşeme alt kalıp: `A = döşeme alanı`

## Donatı

- Birim ağırlık: `kg/m = çap_mm^2 / 162`
- Toplam ağırlık: `kg = toplam_boy_m * kg/m * (1 + fire_oranı)`
- Toplam boy: `boy_m * adet` veya poz listesinden toplam.

## Kaplama

- Sıva/boya: `net_alan = brüt_duvar_alanı - boşluklar`
- Seramik/kaplama: `net_alan * (1 + fire_oranı)`
- Şap: `alan * kalınlık`

## Eğim

- Yüzde eğim: `eğim_% = kot_farkı / yatay_mesafe * 100`
- Rampa oranı: `1 / (yatay_mesafe / kot_farkı)`

## Not

Bu formüller metraj ve ön hesap içindir. Standart, şartname, statik proje ve imalat detayları sonuçları değiştirebilir.
