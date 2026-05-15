# Dönüşüm Riskleri

## Yüksek Risk

- RVT veya SKP gibi kapalı formatları açık kaynak araçla doğrudan dönüştürmeye çalışmak.
- DWG'den kayıpsız dönüşüm beklemek; modern object enabler ve proxy object kaybı.
- PDF çizimini raster'e çevirip bunu vektör proje gibi sunmak.
- IFC'de property set, classification, storey, spatial hierarchy kaybını kontrol etmemek.
- STEP/IGES solid dosyasını düşük tessellation ile STL'e çevirip ölçüsel karar almak.
- GLB/GLTF dosyasını validator çalıştırmadan web/AR teslimine koymak.

## Orta Risk

- DXF font, lineweight, hatch ve block davranışlarının hedef araçta değişmesi.
- OBJ/FBX texture path'lerinin göreli yoldan kopması.
- Büyük koordinatlı IFC veya GIS verisinin GLB/OBJ formatında hassasiyet kaybetmesi.
- PDF sayfa boyutu, crop box ve rotation farklarının çıktı görselini bozması.

## Düşük Risk

- Raster formatları arasında PNG/JPG/TIFF dönüşümü; yine de DPI ve renk profili kontrol edilir.
- Basit OBJ/STL mesh dönüşümü; yine de normal ve scale kontrol edilir.

## Varsayılan Rapor Dili

- "Kayıpsız dönüştü" ifadesi sadece somut QA kanıtı varsa kullanılır.
- Aksi durumda "dönüşüm üretildi, şu farklar/risksiz alanlar kontrol edildi" denir.
