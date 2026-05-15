---
name: insaat-hesaplamalar
description: İnşaat, mimari, kaba yapı, ince işler, metraj, malzeme, alan, hacim, kazı-dolgu, beton, kalıp, donatı, birim dönüşümü, ön taşıyıcı sistem hesabı ve hesap kontrol raporu hazırlamak için kullanılır; mühendislik onayı yerine geçmez.
---

# İnşaat Hesaplamalar

## Ne Zaman Kullanılır

- Kullanıcı alan, hacim, metraj, malzeme miktarı, kazı-dolgu, beton, kalıp, donatı, boya, şap, sıva, seramik, duvar, çatı, eğim veya birim dönüşümü hesabı istediğinde.
- Mahal listesi, ölçü listesi, CAD/BIM çıktısı veya saha notlarından hesap tablosu/raporu hazırlanacağında.
- Ön boyutlandırma, yaklaşık taşıyıcı sistem yorumu veya açık kaynak hesap motoru seçimi gerektiğinde.
- Hesap formülleri, varsayımlar, birimler, ara adımlar ve QA bayrakları isteniyorsa.

Bu skill uygulama projesi, imzalı mühendislik hesabı, statik proje, deprem hesabı, zemin tasarımı, yangın/MEP uygunluğu veya resmi mevzuat onayı vermez. Kritik taşıyıcı sistem ve mevzuat hesapları yetkili uzman tarafından doğrulanmalıdır.

## Girdi

- Ölçüler: uzunluk, genişlik, yükseklik, kalınlık, adet, aks aralığı, kat sayısı, mahal adı.
- Hedef hesap: alan, hacim, beton, kalıp, donatı, boya, sıva, şap, seramik, kazı, dolgu, eğim, yaklaşık maliyet veya ön taşıyıcı rota.
- Birimler: m, cm, mm, m2, m3, kg, ton, adet; karışık birimler varsa dönüşüm istenir.
- Kaynak: metin brief'i, tablo, CSV/XLSX, CAD/BIM metrajı, IFC quantity, PDF keşif notu.
- Varsayımlar: fire, bindirme, açıklık düşümü, kapı/pencere boşluğu, zayiat, sıkıştırma kabarması, yoğunluk.

## Araç Stratejisi

| Durum | İlk tercih | İkinci tercih | Not |
|---|---|---|---|
| Günlük metraj/ön hesap | Stdlib script + tablo | Spreadsheet skill | Formül ve varsayım açık yazılır. |
| Birim dönüşümü | Pint | stdlib dönüşüm tablosu | Boyutsal hata riski azaltılır. |
| Sembolik/formül kontrolü | SymPy | manuel formül dökümü | Türetme/denklem açıklığı için. |
| BIM/IFC quantity | IfcOpenShell / Ifc5D | BIM skill'i | IFC quantities eksik olabilir. |
| 2D çerçeve/kiriş/truss | anaStruct | Frame3DD | Ön analiz; proje hesabı değildir. |
| 3D elastik analiz | PyNite | Frame3DD | Basit elastik modelleme için. |
| Nonlinear/deprem/geoteknik | OpenSees / OpenSeesPy | uzman modelleme | Yüksek uzmanlık ve doğrulama gerekir. |
| Kesit özellikleri | sectionproperties | manuel dikdörtgen/daire formülü | Karma kesitlerde kullanışlı. |
| Betonarme kesit | concreteproperties | structuralcodes | Kullanıcı sorumluluğu ve mevzuat kontrolü şart. |
| Tasarım kodu yardımcıları | structuralcodes | yerel yönetmelik dokümanı | Kod sürümü açık yazılmalı. |

## İş Akışı

1. Hesap türünü sınıflandır: metraj, malzeme, birim dönüşümü, ön analiz, kesit, BIM quantity veya mevzuat kontrolü.
2. Kaynak veriyi kontrol et: ölçü, birim, kat/mahal, adet, boşluk, fire, yoğunluk, zayiat.
3. Eksik veya çelişkili bilgileri bayrakla; makul varsayım kullanılacaksa açık yaz.
4. Formülü seç ve ara adımları göster.
5. Hesabı makine çıktısı olarak üret: tablo/JSON/Markdown.
6. QA yap: birim tutarlılığı, negatif/0 ölçü, aşırı değer, duplicate mahal, fire oranı, toplam kontrolü.
7. Kritik yapısal veya mevzuat etkisi varsa "ön hesap" olarak işaretle ve uzman onayı gerektir.
8. Gerekirse sonraki skill'e yönlendir: metraj-mahal, risk/güvenlik/uygunluk, BIM/CAD kontrol, müşteri/taşeron iletişimi.

## Çıktı Formatı

```markdown
## Hesap Özeti

## Girdi ve Varsayımlar

## Formüller

## Ara Hesaplar

## Sonuç Tablosu

## QA Bayrakları

## Onay / Sorumluluk Notu

## Sonraki Skill Önerisi
```

Makine çıktısı için `references/cikti-semalari.md` içindeki JSON şemalarını kullan.

## Kalite Kapısı

- Her sonuçta birim bulunmalıdır.
- Her formülün girdileri ve varsayımları yazılmalıdır.
- Metrajda boşluk düşümleri ve fire/zayiat ayrı kalem olmalıdır.
- Donatı hesabında çap, toplam boy, bindirme/fire ve kg/m formülü ayrı gösterilmelidir.
- Beton/kalıp hesabında aynı eleman çift sayılmamalıdır.
- BIM/IFC quantity değerleri "modelden geldi" diye otomatik doğru kabul edilmez; eleman sınıfı ve quantity adı kontrol edilir.
- Taşıyıcı sistem veya mevzuat hesabı uzman onayı gerektirir; çıktı uygulama projesi değildir.

## Onay Sınırı

- Statik, deprem, temel, perde/kolon/kiriş, betonarme/çelik/timber tasarım, zemin, yangın ve resmi mevzuat kararları yetkili mühendis onayı gerektirir.
- Yerel yönetmelik, malzeme standardı ve proje şartnamesi belirtilmeden kesin uygunluk verilmez.
- Fiyat, iş programı veya satın alma kararı için güncel piyasa verisi ve sözleşme şartları ayrıca doğrulanır.

## Referanslar

- Açık kaynak araştırması: `references/acik-kaynak-arastirma.md`
- Araç seçim matrisi: `references/arac-secim-matrisi.md`
- Hesap kapsamları: `references/hesaplama-kapsamlari.md`
- Birim ve varsayım kapıları: `references/birim-ve-varsayim-kapilari.md`
- Metraj ve malzeme formülleri: `references/metraj-ve-malzeme-formulleri.md`
- Çıktı şemaları: `references/cikti-semalari.md`

## Yardımcı Scriptler

- `scripts/check_calculation_tools.py`: hesaplama kütüphaneleri ve ortam araçlarını kontrol eder.
- `scripts/plan_calculation_route.py`: hesap türüne göre güvenli araç rotası ve QA listesi üretir.
- `scripts/basic_quantity_calculator.py`: JSON girdiden temel alan/hacim/beton/kalıp/donatı/metraj hesabı yapar.
