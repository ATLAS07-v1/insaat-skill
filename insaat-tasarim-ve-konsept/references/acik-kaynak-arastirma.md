# Açık Kaynak Araştırması

Bu skill için referanslar, konsept tasarımın açık kaynak araçlarla üretilebilir ve denetlenebilir hale gelmesi için seçildi.

## Çekirdek Referanslar

| Referans | Kullanım | Hibrit yaklaşımdaki rol |
|---|---|---|
| FreeCAD | Parametrik 3D modelleme, mimari/BIM ön model, 2D-3D geçiş | Kütle ve konsept model için açık kaynak CAD çekirdeği. |
| FreeCAD BIM Workbench | Mimari/BIM nesneleri ve IFC odaklı akış | Konsept kütleyi erken BIM diline taşır. |
| IfcOpenShell / Bonsai | IFC okuma-yazma, Blender içinde native IFC authoring | Konseptin IFC, BCF, IDS ve sonraki BIM kontrollerine bağlanması. |
| Blender | Görsel konsept, malzeme, ışık, kamera, render | Sunum ve atmosfer çıktısı için. |
| SketchUp Ruby API | Hızlı kütle ve sahne üretimi | Kapalı kaynak aracı varsa script/brief rotası; açık kaynak alternatifi Blender/FreeCAD. |
| QGIS | Arsa, çevre, ulaşım, kot, GIS katmanları | Bağlam ve vaziyet analizi için. |
| OSMnx | OpenStreetMap'ten yol, bina, POI ve ağ analizi | Site çevresi, erişim, yaya/araç ağı ve kent dokusu ön analizi. |
| GeoPandas / Shapely | Geometri, buffer, alan, mesafe ve spatial işlem | Arsa/çekme mesafesi/yerleşim hesapları için Python çekirdeği. |
| Ladybug / Honeybee | Gün ışığı, radyasyon, enerji ön analizi | Erken tasarım performans kararlarını besler. |
| OpenStudio / EnergyPlus | Enerji modeli ve simülasyon motoru | Konseptten enerji senaryosuna geçiş rotası. |
| COMPAS | Hesaplamalı tasarım, geometri ve dijital üretim | Parametrik veya üretim odaklı konseptlerde. |
| TopologicPy | Mekansal/topolojik analiz ve building intelligence | Mahal komşuluğu, erişim ve ilişkisel tasarım kontrolü. |
| Speckle | AEC veri paylaşımı, versiyonlama, model aktarımı | Konsept verisinin platformlar arası paylaşımı. |

## Hibrit Çalışma

1. Brief ve arsa/program verisi standart JSON yapısına alınır.
2. Hafif metrikler stdlib ile hesaplanır: emsal, kaplama, toplam alan, açık alan, kat yüksekliği, basit uygunluk bayrakları.
3. Arsa/bağlam verisi varsa QGIS, GeoPandas, Shapely veya OSMnx rotası önerilir.
4. Kütle üretimi gerekiyorsa FreeCAD/BIM Workbench veya Blender/Bonsai rotası seçilir; SketchUp varsa kapalı kaynak lisans sınırı belirtilir.
5. Performans sorusu varsa Ladybug/Honeybee/OpenStudio/EnergyPlus hattına geçilir.
6. Alternatifler ağırlıklı karar matrisiyle puanlanır; sonuç kesin proje değil konsept önerisi olarak raporlanır.
7. Bir sonraki üretim adımı için ilgili skill'e yönlendirilir: CAD, BIM, Blender, SketchUp, metraj, hesap veya teknik kontrol.

## Kaynak Linkleri

- FreeCAD: https://github.com/FreeCAD/FreeCAD
- FreeCAD BIM Workbench: https://github.com/yorikvanhavre/BIM_Workbench
- IfcOpenShell / Bonsai: https://github.com/IfcOpenShell/IfcOpenShell
- Ladybug / Honeybee: https://www.ladybug.tools/honeybee.html
- Ladybug Tools GitHub: https://github.com/ladybug-tools
- OpenStudio: https://github.com/NREL/OpenStudio
- EnergyPlus: https://github.com/NREL/EnergyPlus
- QGIS: https://github.com/qgis/QGIS
- OSMnx: https://github.com/gboeing/osmnx
- GeoPandas: https://github.com/geopandas/geopandas
- Shapely: https://github.com/shapely/shapely
- COMPAS: https://github.com/compas-dev/compas
- TopologicPy: https://github.com/wassimj/topologicpy
- Speckle: https://github.com/specklesystems
