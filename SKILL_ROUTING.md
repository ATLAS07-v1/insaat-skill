# Skill Routing

Bu doküman agent'in 17 skill arasında deterministik seçim yapması için kullanılır.

## Öncelik Sırası

1. Kullanıcının dosya türü ve istenen çıktı türünü belirle.
2. Önce en dar domain skill'ini seç.
3. Dosya envanteri gerekiyorsa `insaat-arac-kullanimlari` ile başla.
4. Dönüşüm, export veya format QA gerekiyorsa `cizim-dosya-donusum-ve-qa` veya `dokuman-standartlastirma-ve-formatlama` skill'ine geçir.
5. Finansal, teknik, İSG, sözleşmesel veya üçüncü taraf çıktılarda insan onayı sınırını yaz.

## Sınır Kararları

| Talep | Ana skill | Handoff |
|---|---|---|
| Dosya paketi geldi, hangi araçla açılır? | `insaat-arac-kullanimlari` | Gerekirse ilgili domain skill'e yönlendir. |
| DWG/DXF layer, block, ölçü veya mark-up kontrolü | `cad-autocad-dwg-dxf-isleme` | Dönüşüm gerekiyorsa `cizim-dosya-donusum-ve-qa`. |
| IFC/BIM model, Revit export planı, IDS/BCF | `bim-revit-ifc-model-kontrolu` | Metraj için `metraj-ve-mahal-kontrolu`. |
| Genel dosya dönüşümü ve paket QA | `cizim-dosya-donusum-ve-qa` | CAD/BIM içerik analizi için ilgili skill. |
| Beton, donatı, kalıp, alan, hacim, birim/formül hesabı | `insaat-hesaplamalar` | Quantity takeoff veya mahal listesi için `metraj-ve-mahal-kontrolu`. |
| Mahal, room schedule, BOQ/IFC quantity karşılaştırma | `metraj-ve-mahal-kontrolu` | Fiyatlandırma için `teklif-ve-maliyet-tablolama`. |
| Konsept alternatifi, yerleşim skoru, tasarım trade-off | `insaat-tasarim-ve-konsept` | 3D üretim için Blender veya SketchUp skill'i. |
| Blender sahne/script/render | `blender-3d-modelleme-ve-render` | Konsept girdisi için `insaat-tasarim-ve-konsept`. |
| SketchUp kütle/Ruby script/export planı | `sketchup-konsept-ve-kutle-modelleme` | Görselleştirme için Blender skill'i. |
| Teklif, BOQ, maliyet tablosu, markup, KDV | `teklif-ve-maliyet-tablolama` | Tedarik teklifleri için `tedarik-ve-malzeme-karsilastirma`. |
| Hakediş, fatura, ödeme, kesinti, mutabakat | `hakedis-ve-mutabakat-kontrolu` | Metraj farkı için `metraj-ve-mahal-kontrolu`. |
| Malzeme, tedarikçi, datasheet, RFQ karşılaştırma | `tedarik-ve-malzeme-karsilastirma` | Şartname uygunluğu için `teknik-sartname-ve-uygulama-kontrolu`. |
| Şartname maddesi, uygulama kanıtı, teknik checklist | `teknik-sartname-ve-uygulama-kontrolu` | Risk/uygunsuzluk için `risk-guvenlik-ve-uygunluk-denetimi`. |
| İSG, risk register, uygunluk, permit, nonconformance | `risk-guvenlik-ve-uygunluk-denetimi` | Fotoğraf kanıtı için `saha-fotograf-ve-kanit-analizi`. |
| Müşteri/taşeron e-postası, RFI, submittal, toplantı | `musteri-ve-taseron-iletisim-hazirlayici` | Doküman formatı için `dokuman-standartlastirma-ve-formatlama`. |
| Saha fotoğrafı, EXIF, kanıt register, duplicate | `saha-fotograf-ve-kanit-analizi` | Risk aksiyonu için `risk-guvenlik-ve-uygunluk-denetimi`. |
| DOCX/PDF/Markdown/XLSX format, revizyon, paket QA | `dokuman-standartlastirma-ve-formatlama` | İçerik domain kontrolü için ilgili skill. |

## Handoff Kuralı

- Handoff çıktısı JSON veya Markdown özet olabilir.
- Makine-okunur çıktı için `schemas/` altındaki schema dosyaları tercih edilir.
- Skill'ler arası genel aktarımda `schemas/handoff-envelope.schema.json` ortak zarf olarak kullanılmalıdır.
- `payload_schema`, zarf içindeki `payload` alanının hangi domain şemasıyla yorumlanacağını göstermelidir.
- Handoff sırasında kaynak dosya, varsayım, tarih, onay sınırı ve eksik veri bayrakları korunmalıdır.
