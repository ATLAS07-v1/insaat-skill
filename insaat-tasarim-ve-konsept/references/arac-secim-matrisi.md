# Araç Seçim Matrisi

| İş | İlk tercih | Yedek | Not |
|---|---|---|---|
| Arsa analizi | QGIS / GeoPandas / OSMnx | Shapely | GIS verisi yoksa elle girilen arsa ölçülerinden basit metrik üretilir. |
| Parametrik kütle | FreeCAD | Blender/Bonsai | FreeCADCmd varsa scriptlenebilir; yoksa üretim brief'i verilir. |
| Native IFC konsepti | Bonsai / IfcOpenShell | FreeCAD BIM | IFC tabanlı sonraki BIM kontrolüne uygundur. |
| Görsel konsept | Blender | SketchUp + export | Render ve atmosfer için Blender skill'e devret. |
| Hızlı kütle/sahne | SketchUp skill | Blender script | SketchUp lisansı ve Ruby API ortamı kontrol edilir. |
| Gün ışığı | Ladybug/Honeybee/Radiance | Basit yön/gölge yorumu | Simülasyon yoksa kesin performans iddiası yoktur. |
| Enerji | OpenStudio/EnergyPlus | Honeybee Energy | Erken enerji modeli için doğru geometri ve zonlama gerekir. |
| Mekansal ilişki | TopologicPy | NetworkX / manuel adjacency | Mahal komşuluğu, erişim ve akış için. |
| Hesaplamalı tasarım | COMPAS | numpy/shapely | Dijital üretim, kafes, yüzey ve geometri deneyleri için. |
| Veri paylaşımı | IFC / Speckle | JSON/CSV | Platformlar arası aktarım ve revizyon izleme için. |

## Seçim Kuralları

- Kullanıcı görsel istiyorsa Blender/SketchUp; kullanıcı ölçü-parametre istiyorsa FreeCAD/IFC; kullanıcı çevre/arsa istiyorsa GIS hattı seçilir.
- Konsept kararları önce metrik ve varsayım tablosuyla netleştirilir, sonra modelleme aracına geçilir.
- Açık kaynak araç yoksa çıktı "modelleme brief'i" olarak hazırlanır; kapalı kaynak ortamda çalıştırılacak script varsa lisans/ortam sınırı yazılır.
- Tek seçenek üretme; en az iki gerçek alternatif ve karşılaştırma tablosu üret.
- Simülasyon sonucu yoksa "güneş/enerji ön değerlendirmesi" ifadesi kullanılır.
