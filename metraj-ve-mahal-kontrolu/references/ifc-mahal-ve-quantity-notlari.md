# IFC Mahal ve Quantity Notları

## IFC Elemanları

- Mahal/oda genelde `IfcSpace` olarak gelir.
- Kat/seviye ilişkisi çoğunlukla `IfcBuildingStorey` ile kurulur.
- Alan/hacim değerleri `BaseQuantities` veya property setlerinde bulunabilir.
- `Name`, `LongName`, `ObjectType`, `GlobalId` ayrı anlamlar taşıyabilir.

## Kontrol İlkeleri

- `IfcSpace` sayısı mimari mahal listesiyle karşılaştırılır.
- Quantity adı açık yazılır: `NetFloorArea`, `GrossFloorArea`, `GrossVolume`, vb.
- Quantity yoksa geometriden hesap denenebilir ama bu daha yüksek risklidir.
- Büyük koordinat, storey kopukluğu ve property eksikliği ayrıca bayraklanır.
- IFC export ayarları Revit/Archicad/Tekla gibi kaynak yazılıma bağlıdır.

## Yönlendirme

- IFC model QA gerekiyorsa `bim-revit-ifc-model-kontrolu`.
- Dönüşüm gerekiyorsa `cizim-dosya-donusum-ve-qa`.
- Hesap/formül doğrulaması gerekiyorsa `insaat-hesaplamalar`.
