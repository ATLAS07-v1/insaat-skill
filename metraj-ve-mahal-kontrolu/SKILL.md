---
name: metraj-ve-mahal-kontrolu
description: İnşaat, mimari, BIM, CAD, PDF ve tablo kaynaklarından mahal listesi, room/space schedule, metraj, alan, hacim, adet, quantity takeoff, mahal kodu, kat, net/brüt alan ve kaynaklar arası sapma kontrolü yapmak için kullanılır.
---

# Metraj ve Mahal Kontrolü

## Ne Zaman Kullanılır

- Kullanıcı mahal listesi, metraj listesi, room schedule, space schedule, net/brüt alan, hacim, adet, BOQ/QTO veya quantity takeoff kontrolü istediğinde.
- IFC/Revit export, CAD ölçümü, PDF mahal listesi, Excel/CSV tablo veya manuel metraj kaynakları karşılaştırılacağında.
- Mahal adı/kodu, kat, kullanım tipi, alan, hacim, adet ve quantity farkları için sapma raporu hazırlanacağında.
- Model quantity ile keşif/metraj/mahal tablosu arasında tutarsızlık aranacağında.

Bu skill metraj ve mahal QA çıktısı üretir. Resmi keşif, hakediş, ihale, uygulama veya mali bağlayıcılığı olan sonuçlar için teknik/sözleşmesel onay gerekir.

## Girdi

- Mahal listesi: CSV/XLSX/JSON, PDF tablo, IFC `IfcSpace`, Revit/IFC export, CAD alan listesi.
- Zorunlu alanlar: mahal kodu veya adı, kat/seviye, net alan veya brüt alan, mümkünse hacim/adet.
- Karşılaştırma hedefi: model vs Excel, PDF vs CSV, revizyon A vs revizyon B, keşif vs BIM quantity.
- Tolerans: alan için varsayılan yüzde 1 veya 0.1 m2; adet için sıfır tolerans.
- Ölçüm kuralı: net/brüt ayrımı, boşluk düşümü, duvar merkez çizgisi/dış yüzey, mahal sınırı.

## Araç Stratejisi

| Durum | İlk tercih | İkinci tercih | Not |
|---|---|---|---|
| IFC mahal/space okuma | IfcOpenShell | xBIM / web-ifc | `IfcSpace`, `BaseQuantities`, storey ve property kontrolü. |
| IFC schedule export/import | IfcCSV | pandas CSV/XLSX | Mahal schedule ve property tablosu için. |
| IFC 5D/QTO | Ifc5D | QuantityTakeoff-Python | Cost/quantity ilişkileri ve BOQ bağlantıları. |
| XLSX/CSV mahal listesi | pandas/openpyxl | stdlib CSV | Kolon eşleştirme ve toplam kontrolü. |
| PDF mahal/metraj tablosu | pdfplumber | Camelot | Sadece text-based PDF güvenilir; tarama PDF OCR ister. |
| Mahal adı eşleştirme | RapidFuzz | stdlib difflib | Ad/kod farklarında aday eşleşme üretir. |
| CAD alan ölçümü | CAD skill'i | DXF entity QA | Alan polyline/layer kontrolü gerekir. |
| Hesap/formül | insaat-hesaplamalar | spreadsheet skill | Alan/hacim/fire hesapları için. |

## İş Akışı

1. Kaynakları sınıflandır: IFC, CSV/XLSX, PDF, CAD, manuel metin veya revizyon karşılaştırması.
2. Kolonları eşleştir: mahal kodu, mahal adı, kat, alan, hacim, adet, kategori, kaynak.
3. Birim ve ölçüm kuralını doğrula: m2/m3, net/brüt, mahal sınırı, boşluk düşümü, revizyon tarihi.
4. Normalizasyon yap: adları sadeleştir, katları standardize et, sayıları noktalı ondalığa çevir.
5. Tek kaynak QA yap: eksik kod/ad, duplicate mahal, negatif/0 alan, boş kat, aşırı değer, toplam kontrolü.
6. Çok kaynak karşılaştır: birebir kod, sonra ad+kat fuzzy aday eşleşme, sonra eşleşmeyen kayıtlar.
7. Sapmaları sınıflandır: alan farkı, hacim farkı, adet farkı, isim değişikliği, kat değişikliği, eksik/fazla mahal.
8. Sonuç üret: özet toplamlar, fark tablosu, kritik bayraklar, kontrol gerektiren eşleşmeler.
9. Gerekirse sonraki skill'e yönlendir: BIM model kontrolü, CAD ölçüm, hesaplamalar, müşteri/taşeron iletişimi.

## Çıktı Formatı

```markdown
## Metraj / Mahal Kontrol Özeti

## Kaynaklar ve Varsayımlar

## Kolon Eşleştirme

## Tek Kaynak QA

## Kaynaklar Arası Karşılaştırma

## Sapma Tablosu

## Kritik Bayraklar

## Onay / Sorumluluk Notu

## Sonraki Skill Önerisi
```

Makine çıktısı için `references/cikti-semalari.md` içindeki JSON şemalarını kullan.

## Kalite Kapısı

- Net alan ve brüt alan karıştırılmaz; karışık ise sonuç bayraklanır.
- Her mahalde kod veya ad bulunmalıdır; ikisi de yoksa eşleştirme güvenilmezdir.
- Kat/seviye bilgisi yoksa duplicate mahal riski artar ve raporlanır.
- Duplicate kod, duplicate ad+kat, 0/negatif alan, aşırı alan ve eksik quantity bayraklanır.
- IFC quantity değerleri modelden geldi diye otomatik doğru kabul edilmez; quantity set adı, `IfcSpace` sayısı ve storey ilişkisi kontrol edilir.
- PDF tablo çıkarımı düşük doğrulukluysa manuel doğrulama gerekir.
- Sapma toleransı raporda açık yazılır.

## Onay Sınırı

- Bu skill metraj kontrol ve sapma analizi yapar; kesin hakediş, ihale, sözleşme, satın alma veya resmi teslim sonucu üretmez.
- Mahallerin ölçüm kuralı proje/şartname/sözleşmeye bağlıysa kullanıcı veya teknik sorumlu tarafından onaylanmalıdır.
- Model, CAD veya PDF kaynaklarında eksik/yanlış veri varsa sonuç yalnız kontrol bulgusu olarak kullanılmalıdır.

## Referanslar

- Açık kaynak araştırması: `references/acik-kaynak-arastirma.md`
- Araç seçim matrisi: `references/arac-secim-matrisi.md`
- Mahal QA kontrol listesi: `references/mahal-qa-kontrol-listesi.md`
- Metraj karşılaştırma kuralları: `references/metraj-karsilastirma-kurallari.md`
- IFC quantity notları: `references/ifc-mahal-ve-quantity-notlari.md`
- Çıktı şemaları: `references/cikti-semalari.md`

## Yardımcı Scriptler

- `scripts/check_metraj_tools.py`: metraj/mahal kontrolü için araç ve Python modül durumunu raporlar.
- `scripts/plan_metraj_mahal_route.py`: kaynak türüne göre kontrol rotası ve QA kapıları üretir.
- `scripts/compare_room_schedules.py`: CSV/JSON mahal listelerini normalize ederek karşılaştırır.
- `scripts/extract_ifc_spaces_ifcopenshell.py`: IfcOpenShell varsa IFC içinden `IfcSpace` kayıtlarını ve temel quantity alanlarını çıkarır.
