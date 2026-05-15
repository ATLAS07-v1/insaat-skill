# Şartname Madde Çıkarma Kuralları

## Madde Adayı İşaretleri

- Sayısal başlıklar: `1`, `1.1`, `03 30 00`, `2.4.3`.
- Liste başlıkları: `a)`, `A.`, `-`, `•`.
- Zorunluluk kelimeleri: `shall`, `must`, `required`, `olmalıdır`, `zorunludur`, `gereklidir`, `yapılacaktır`, `sağlanacaktır`.
- Kabul ve tolerans kelimeleri: `tolerans`, `limit`, `en az`, `en çok`, `minimum`, `maximum`, `±`, `%`, `mm`, `m2`, `MPa`.
- Kanıt kelimeleri: `test`, `deney`, `rapor`, `sertifika`, `numune`, `mock-up`, `onay`, `kontrol formu`, `fotoğraf`, `ölçüm`.
- Malzeme kelimeleri: `malzeme`, `ürün`, `datasheet`, `teknik föy`, `CE`, `TSE`, `uygunluk belgesi`.
- Uygulama kelimeleri: `uygulanacaktır`, `montaj`, `serim`, `döküm`, `kür`, `astar`, `ankraj`, `derz`, `yalıtım`.

## Sınıflandırma

| Kategori | Belirteç | Kanıt örneği |
|---|---|---|
| Malzeme | ürün, marka, teknik föy, sertifika | Onaylı submittal, datasheet, sertifika. |
| Uygulama | montaj, serim, döküm, kür, derz | Saha fotoğrafı, kontrol tutanağı, method statement. |
| Test/deney | test, deney, numune, laboratuvar | Test raporu, numune sonuçları, kalibrasyon. |
| Tolerans | mm, %, limit, minimum, maximum | Ölçüm kaydı, total station çıktısı, tolerans tablosu. |
| Teslim/Submittal | onay, teslim, rapor, as-built | Onay formu, çizim, O&M, garanti, as-built. |
| BIM/model | IFC, property, classification, parameter | IDS raporu, IfcTester JSON/HTML/BCF çıktısı. |

## Güven Kuralları

- Madde numarası kaybolursa otomatik id `CL-001` gibi verilir ve kaynak satır/sayfa korunur.
- Aynı satırda hem şart hem istisna varsa `manual_review` bayrağı eklenir.
- Tolerans değeri çıkarılamıyorsa "kabul kriteri belirsiz" olarak raporlanır.
- Standart adı geçiyor ama standart metni yoksa "harici standart doğrulanamadı" bayrağı eklenir.
- Şartname revizyonu ve kanıt tarihi çakışıyorsa nihai uygunluk yerine revizyon riski yazılır.
