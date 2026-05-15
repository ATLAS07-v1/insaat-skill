---
name: tedarik-ve-malzeme-karsilastirma
description: İnşaat tedarik, RFQ, tedarikçi teklif karşılaştırma, malzeme teknik uygunluk, datasheet/sertifika/numune kontrolü, fiyat-termin-stok-risk analizi ve satın alma karar tablosu hazırlamak için kullanılır.
---

# Tedarik ve Malzeme Karşılaştırma

## Ne Zaman Kullanılır

- Kullanıcı malzeme, ürün, marka/model, teknik föy, sertifika, numune, tedarikçi teklifleri veya RFQ karşılaştırması istediğinde.
- Tedarikçi teklifleri fiyat, para birimi, termin, stok, nakliye, ödeme şartı, garanti, kapsam dışı işler ve teknik uygunluk üzerinden karşılaştırılacağında.
- Teknik şartname gereksinimleri ile tedarikçi datasheet/sertifika/ürün bilgisi eşleştirileceğinde.
- ERPNext, OpenBoxes, Dolibarr, Odoo Community, Akeneo/OpenPIM, OpenRefine, Frictionless veya spreadsheet araç rotası seçileceğinde.
- Satın alma öncesi bağlayıcı olmayan öneri, risk listesi ve onay gerektiren teknik/ticari maddeler hazırlanacağında.

Bu skill satın alma kararı, sözleşme, ödeme talimatı veya resmi ürün onayı vermez. Teknik şartname, kalite, vergi, ithalat, garanti ve ticari kararlar yetkili kişi tarafından onaylanmalıdır.

## Girdi

- Malzeme ihtiyacı: poz kodu, ürün adı, miktar, birim, şartname maddesi, kritik teknik kriterler, sertifika gereksinimi.
- Tedarikçi teklifleri: tedarikçi, marka/model, birim fiyat, para birimi, termin, stok, nakliye, ödeme, garanti, alternatif ürün, kapsam dışı işler.
- Teknik kaynaklar: datasheet, TDS/SDS, CE/TSE/EN/ISO belgesi, test raporu, numune onayı, teknik şartname, uygulama metodu.
- Karşılaştırma hedefi: en ucuz değil; şartnameye uygun, teslim edilebilir, riskleri açık ve toplam sahip olma maliyeti net seçenek.
- Teslim formatı: JSON, CSV, Markdown tablo, teklif karşılaştırma matrisi, teknik uygunluk matrisi veya satın alma onay özeti.

## Araç Stratejisi

| Durum | İlk tercih | İkinci tercih | Not |
|---|---|---|---|
| RFQ / tedarik akışı | ERPNext Procurement | Dolibarr / Odoo Community | Material request, RFQ, supplier quotation, PO ve receipt akışı. |
| Stok / lot / sevkiyat | OpenBoxes | ERPNext Stock | Lot, expiry, depo, sevkiyat ve stok izleme için. |
| Ürün bilgi yönetimi | Akeneo / OpenPIM | CSV/PIM bridge | Ürün attribute, datasheet ve kanal verisi tekilleştirme. |
| Malzeme teknik uygunluk | `compare_material_specs.py` | teknik şartname skill'i | Datasheet/sertifika ile gereksinim eşleştirme. |
| Tedarikçi teklif karşılaştırma | `compare_supplier_quotes.py` | teklif-ve-maliyet-tablolama | Fiyat, termin, teknik uygunluk ve risk skorlaması. |
| Veri temizleme/eşleştirme | OpenRefine / RapidFuzz | stdlib difflib | Ürün adı, marka, model ve tedarikçi eşleştirme. |
| Tablo doğrulama | Frictionless / Great Expectations | stdlib validator | CSV/XLSX kolon ve veri kalite kontrolü. |
| Kamu/ihale veri modeli | OCDS / OpenProcurement | CSV/JSON | Tender, award, contract, supplier veri yapısı referansı. |
| PDF/datasheet çıkarımı | pypdf / pdfplumber | OCR + manuel QA | Tarama PDF ve üretici katalogları manuel doğrulama ister. |

## İş Akışı

1. İhtiyacı sınıflandır: RFQ hazırlığı, tedarikçi teklif karşılaştırması, malzeme teknik uygunluğu, stok/termin kontrolü, satın alma onay özeti veya teslim kabul.
2. Gereksinimi normalize et: ürün kodu, açıklama, miktar, birim, zorunlu teknik kriterler, sertifika, kalite ve teslim koşulları.
3. Tedarikçi tekliflerini normalize et: fiyat, para birimi, termin, stok, marka/model, teknik uygunluk, ödeme, nakliye, garanti ve istisnalar.
4. Teknik uygunluğu kontrol et: şartname kriteri vs datasheet/sertifika/test raporu; eksik belge ve muadil ürün bayrakları.
5. Ticari karşılaştırma yap: toplam fiyat, nakliye/ek maliyet, termin, ödeme şartı, garanti, tedarik riski ve kapsam dışı işler.
6. Riskleri sınıflandır: teknik uygunsuzluk, eksik sertifika, fiyat geçerlilik tarihi yok, stok belirsiz, uzun termin, kur/ithalat riski, marka/model muadili.
7. Karar matrisi üret: en düşük fiyat, en hızlı termin, en yüksek teknik uygunluk ve dengeli öneri ayrı gösterilir.
8. Onay sınırını yaz: teknik onay, satın alma onayı, sözleşme/ödeme ve güncel fiyat doğrulaması kullanıcı tarafındadır.

## Çıktı Formatı

```markdown
## Tedarik / Malzeme Karşılaştırma Özeti

## İhtiyaç ve Şartname Kriterleri

## Tedarikçi Teklif Matrisi

## Malzeme Teknik Uygunluk Matrisi

## Fiyat, Termin, Stok ve Ödeme Karşılaştırması

## Riskler ve Eksik Belgeler

## Önerilen Aksiyonlar

## Onay Sınırı
```

Makine çıktısı için `references/cikti-semalari.md` içindeki JSON şemalarını kullan.

## Kalite Kapısı

- Birim ve miktar tüm tedarikçilerde aynı ölçü sistemine normalize edilmelidir.
- Para birimi, kur tarihi, fiyat geçerlilik tarihi ve KDV/nakliye dahil-hariç durumu açık olmalıdır.
- Teknik şartnameye uymayan en ucuz teklif öneri olarak sunulmaz; "ticari ucuz ama teknik riskli" olarak ayrılır.
- Eksik datasheet, sertifika, test raporu veya numune onayı satın alma öncesi kritik bayrak alır.
- Muadil ürünlerde marka/model, performans ve garanti eşdeğerliği teknik sorumlu tarafından onaylanmalıdır.
- Stok ve termin bilgisi yazılı teyit veya teklif referansı olmadan kesin kabul edilmez.
- Satın alma, sözleşme, ödeme, ithalat/gümrük ve garanti kararları yetkili onay gerektirir.

## Referanslar

- Açık kaynak araştırması: `references/acik-kaynak-arastirma.md`
- Araç seçim matrisi: `references/arac-secim-matrisi.md`
- Tedarik iş akışı: `references/tedarik-is-akisi.md`
- Malzeme karşılaştırma kuralları: `references/malzeme-karsilastirma-kurallari.md`
- Tedarikçi teklif karşılaştırma kuralları: `references/tedarikci-teklif-karsilastirma-kurallari.md`
- Stok, termin ve risk notları: `references/stok-termin-risk-notlari.md`
- Çıktı şemaları: `references/cikti-semalari.md`

## Yardımcı Scriptler

- `scripts/check_procurement_tools.py`: tedarik, PIM, tablo, PDF ve veri kalite araç durumunu raporlar.
- `scripts/plan_procurement_route.py`: iş tipine göre araç rotası, QA kapıları ve çıktı seti üretir.
- `scripts/compare_supplier_quotes.py`: tedarikçi tekliflerini fiyat, termin, uygunluk ve riskle skorlar.
- `scripts/compare_material_specs.py`: malzeme teknik özelliklerini şartname kriterleriyle karşılaştırır.
