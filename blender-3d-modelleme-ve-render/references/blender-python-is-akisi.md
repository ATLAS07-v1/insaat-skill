# Blender Python İş Akışı

## Standart Komut

```powershell
blender --background --python create_construction_scene.py -- --spec scene.json --output output
```

## Script Prensipleri

- Orijinal dosyayı değiştirme.
- Çıktı klasörü oluştur.
- Sahne birimini ayarla.
- Obje adlarını anlamlı ver: `Wall_North`, `Floor_Main`, `Window_01`.
- Malzeme adlarını sade tut: `Mat_Wall_Paint`, `Mat_Glass_Clear`.
- Kamera ve ışıkları adlandır.
- Render çözünürlüğünü açıkça yaz.
- İş sonunda JSON raporu üret.

## Modelleme Sırası

1. Scene cleanup.
2. Unit setup.
3. Collections: `Architecture`, `Furniture`, `Lighting`, `Cameras`, `Annotations`.
4. Geometry creation/import.
5. Materials.
6. Lighting.
7. Camera setup.
8. Render/export.
9. QA report.

## Ölçü Varsayımı

Ölçü verilmemişse varsayılan metrik oda:

- genişlik: 5.0 m
- derinlik: 4.0 m
- yükseklik: 3.0 m
- duvar kalınlığı: 0.15 m

Bu varsayım kesin proje bilgisi değildir.
