---
name: teklif-ve-maliyet-tablolama
description: İnşaat teklif, yaklaşık maliyet, BOQ, metraj-maliyet eşleştirme, birim fiyat, taşeron teklifi karşılaştırma, markup, KDV, risk payı, nakit akışı ve maliyet tablosu QA hazırlamak için kullanılır.
---

# Teklif ve Maliyet Tablolama

## Ne Zaman Kullanılır

- Kullanıcı inşaat teklifi, yaklaşık maliyet, BOQ, birim fiyat analizi, maliyet tablosu, keşif özeti, taşeron teklifi karşılaştırması veya ihale tablo taslağı istediğinde.
- Metraj/mahal, CAD/BIM/IFC quantity, PDF keşif, Excel/CSV fiyat listesi veya manuel kalemlerden maliyet tablosu hazırlanacağında.
- Malzeme, işçilik, ekipman, nakliye, fire, genel gider, kar, beklenmeyen gider, iskonto ve KDV kalemleri açık ayrıştırılacağında.
- BIM 5D maliyet, IfcOpenShell Ifc5D, OpenConstructionERP/DDC CWICR, ERPNext, OpenProject, GnuCash veya spreadsheet araç rotası seçileceğinde.
- Müşteri veya taşeron için bağlayıcı olmayan teklif metni/ek tablo iskeleti hazırlanacağında.

Bu skill maliyet modeli ve teklif tablosu hazırlar. Güncel piyasa fiyatı, vergi oranı, kur, sözleşme şartı veya bağlayıcı ticari teklif kesinliği için canlı veri ve yetkili onay gerekir.

## Girdi

- Kalem listesi: kod, açıklama, kategori, miktar, birim, birim fiyat, para birimi, kaynak, fire/zayiat, not.
- Metraj kaynağı: CSV/XLSX/JSON, PDF, CAD, BIM/IFC quantity, mahal/metraj skill çıktısı.
- Fiyat kaynağı: kullanıcı fiyat listesi, taşeron teklifi, tedarikçi katalogu, açık kaynak maliyet veri tabanı, önceki proje verisi.
- Markup: genel gider, kar, beklenmeyen gider, risk payı, iskonto, KDV, kur ve geçerlilik süresi.
- Teslim hedefi: Markdown özet, JSON, CSV, XLSX/ODS rotası, teklif eki, taşeron karşılaştırma veya takip bütçesi.

## Araç Stratejisi

| Durum | İlk tercih | İkinci tercih | Not |
|---|---|---|---|
| BOQ ve maliyet platformu | OpenConstructionERP | CSV/JSON bridge | Açık kaynak BOQ, CAD/BIM takeoff, 4D/5D ve validation referansı. |
| Açık maliyet veri tabanı | DDC CWICR | kullanıcı fiyat listesi | Bölge, tarih ve lisans kontrolü şarttır. |
| BIM 5D / IFC cost | IfcOpenShell Ifc5D | BIM skill'i | IFC quantity ve cost item ilişkisi doğrulanır. |
| Tablo üretimi | pandas + XlsxWriter | openpyxl / CSV | Profesyonel XLSX için; formül hesaplaması Excel/LibreOffice tarafında olabilir. |
| ODS / açık format | LibreOffice Calc / odfdo | CSV | Açık dosya formatı gerekiyorsa tercih edilir. |
| Teklif/satış/ERP | ERPNext | Odoo Community / CSV import | Quotation, item, project costing ve stok bağlantısı için. |
| Proje maliyet takibi | OpenProject | ERPNext / spreadsheet | Budget, cost reporting ve time cost takibi. |
| Muhasebe kayıtları | GnuCash | ERP muhasebe | Çift taraflı muhasebe ve SMB kayıtları için; teklif motoru değildir. |
| PDF teklif analizi | pypdf/pdfplumber | manuel çıkarım | Tarama PDF için OCR ve manuel doğrulama gerekir. |

## İş Akışı

1. Amacı sınıflandır: yaklaşık maliyet, detaylı BOQ, taşeron karşılaştırma, BIM 5D, teklif eki, bütçe/takip veya variation order.
2. Kaynakları ayır: metraj kaynağı, fiyat kaynağı, para birimi, tarih, revizyon, vergi ve sözleşme varsayımları.
3. Kalemleri normalize et: kod, açıklama, kategori, miktar, birim, birim fiyat, fire, kaynak, not, teklif kapsamı.
4. Hesapla: miktar x birim fiyat, fireli miktar, direkt maliyet, genel gider, kar, risk/beklenmeyen, iskonto, KDV ve toplam.
5. QA yap: eksik birim, sıfır miktar/fiyat, negatif değer, duplicate kod, yüksek fire, formül toplam farkı, kaynak belirsizliği.
6. Riskleri ayır: fiyat tarihi, kur, tedarik süresi, kapsam dışı işler, şartname belirsizliği, metraj belirsizliği, taşeron istisnası.
7. Çıktı üret: teklif özeti, maliyet kırılımı, kategori toplamları, markup tablosu, QA bayrakları, varsayımlar ve onay sınırı.
8. Gerekirse sonraki skill'e yönlendir: metraj-mahal kontrolü, teknik şartname kontrolü, müşteri/taşeron iletişimi, BIM 5D veya hesaplamalar.

## Çıktı Formatı

```markdown
## Teklif / Maliyet Özeti

## Kaynaklar ve Varsayımlar

## BOQ / Kalem Tablosu

## Kategori Toplamları

## Markup, KDV ve Toplam

## Taşeron / Tedarikçi Karşılaştırması

## QA Bayrakları

## Riskler ve Kapsam Dışı İşler

## Onay Sınırı ve Sonraki Aksiyonlar
```

Makine çıktısı için `references/cikti-semalari.md` içindeki JSON şemalarını kullan.

## Kalite Kapısı

- Her kalemde kod veya açıklama, miktar, birim ve birim fiyat bulunmalıdır.
- Para birimi, fiyat tarihi, kur varsayımı ve KDV durumu açık yazılmalıdır.
- Güncel piyasa fiyatı kullanıcı tarafından verilmediyse veya canlı araştırma yapılmadıysa sonuç "yaklaşık / doğrulanmamış fiyat" olarak işaretlenir.
- Metraj kaynağı doğrulanmadan maliyet kesin teklif gibi sunulmaz.
- KDV, stopaj, damga vergisi, gümrük, nakliye ve sözleşme özel şartları yerel mevzuata bağlıdır; onay gerekir.
- Taşeron teklifleri kapsam, istisna, marka/model, süre, ödeme ve garanti şartları eşitlenmeden sadece toplam fiyatla sıralanmaz.
- Formül ve toplamlar tekrar hesaplanmalı; spreadsheet formülleri tek doğruluk kaynağı kabul edilmemelidir.

## Referanslar

- Açık kaynak araştırması: `references/acik-kaynak-arastirma.md`
- Araç seçim matrisi: `references/arac-secim-matrisi.md`
- Teklif iş akışı: `references/teklif-is-akisi.md`
- BOQ ve maliyet kuralları: `references/boq-ve-maliyet-kurallari.md`
- Tablo kalite kapıları: `references/tablo-kalite-kapilari.md`
- Fiyat ve risk notları: `references/fiyat-ve-risk-notlari.md`
- Çıktı şemaları: `references/cikti-semalari.md`

## Yardımcı Scriptler

- `scripts/check_cost_tools.py`: maliyet, tablo, BOQ, PDF ve BIM 5D araç durumunu raporlar.
- `scripts/plan_bid_cost_route.py`: iş tipine göre araç rotası, QA kapıları ve çıktı seti üretir.
- `scripts/build_cost_table.py`: JSON kalem listesinden maliyet/markup/toplam tablosu üretir.
- `scripts/validate_cost_table.py`: JSON/CSV maliyet tablosunda eksik alan, toplam farkı, duplicate ve risk bayraklarını kontrol eder.
