---
name: hakedis-ve-mutabakat-kontrolu
description: İnşaat hakediş, ara ödeme, kesin hesap, metraj-mutabakat, fatura-ödeme eşleştirme, taşeron hakedişi, avans, teminat, kesinti, KDV, sözleşme kalemi ve ödeme farkı kontrolü yapmak için kullanılır.
---

# Hakediş ve Mutabakat Kontrolü

## Ne Zaman Kullanılır

- Kullanıcı ana yüklenici veya taşeron hakedişi, ara ödeme sertifikası, kesin hesap, metraj-mutabakat, fatura-ödeme eşleştirme veya tahakkuk kontrolü istediğinde.
- Sözleşme BOQ kalemi, önceki hakediş, cari imalat miktarı, onaylı miktar, birim fiyat, kesinti ve ödeme toplamları karşılaştırılacağında.
- Avans mahsubu, nakit teminat/retention, iş güvenliği/ceza kesintisi, stopaj, KDV, fiyat farkı, variation order veya iş artışı/azalışı ayrıştırılacağında.
- ERPNext/Mint, OpenProject, OpenConstructionERP, IfcOpenShell Ifc5D, Beancount/Ledger, Frictionless veya spreadsheet araç rotası seçileceğinde.
- Müşteri/taşeron için bağlayıcı olmayan mutabakat özeti ve fark listesi hazırlanacağında.

Bu skill hakediş ve mutabakat kontrol raporu üretir. Resmi hakediş onayı, ödeme talimatı, vergi yorumu, hukuki/sözleşmesel karar veya muhasebe kaydı kesinliği üretmez.

## Girdi

- Sözleşme kalemleri: poz kodu, açıklama, birim, sözleşme miktarı, birim fiyat, para birimi.
- Hakediş verisi: önceki onaylı miktar, cari imalat miktarı, cari onaylı miktar, kümülatif miktar, önceki tutar, cari tutar.
- Mutabakat kaynakları: metraj tablosu, BOQ, fatura, ödeme dekontu, ERP kayıtları, banka hareketleri, taşeron icmali.
- Kesintiler ve ekler: avans mahsubu, teminat/retention, ceza, fiyat farkı, iş artışı/azalışı, KDV, stopaj, iskonto, diğer kesintiler.
- Teslim hedefi: Markdown rapor, JSON, CSV, XLSX/ODS rotası, fark tablosu, ödeme kontrol listesi veya taşeron mutabakat taslağı.

## Araç Stratejisi

| Durum | İlk tercih | İkinci tercih | Not |
|---|---|---|---|
| Hakediş hesap çekirdeği | `calculate_progress_payment.py` | spreadsheet skill | Önceki/cari/kümülatif tutar ve kesinti hesaplar. |
| Kaynak karşılaştırma | `compare_progress_sources.py` | pandas / RapidFuzz | Hakediş-fatura-ödeme-BOQ farklarını bulur. |
| BOQ ve inşaat ERP | OpenConstructionERP | teklif-ve-maliyet-tablolama | BOQ, 4D/5D, cost item ve validation referansı. |
| BIM 5D | IfcOpenShell Ifc5D | BIM skill'i | Quantity-cost ilişkisi ve kümülatif metraj için. |
| ERP / fatura / ödeme | ERPNext | Mint / Settler | Payment reconciliation ve invoice matching için. |
| Proje bütçe-gerçekleşen | OpenProject | ERPNext / CSV | Time, unit cost, budget ve cost report export. |
| Çift kayıt muhasebe | Beancount / Ledger | GnuCash | Mutabakat kanıtı ve muhasebe disiplin referansı. |
| Tablo kalite kontrolü | Frictionless / Great Expectations | stdlib validator | CSV/XLSX şema ve veri kalite doğrulaması. |
| PDF hakediş/fatura | pypdf / pdfplumber | OCR + manuel QA | Tarama PDF düşük güvenli kabul edilir. |

## İş Akışı

1. Kontrol tipini sınıflandır: ana sözleşme hakedişi, taşeron hakedişi, fatura-ödeme mutabakatı, kesin hesap, variation/fiyat farkı veya bütçe-gerçekleşen.
2. Kaynakları ayır: sözleşme BOQ, önceki hakediş, cari ölçüm, onaylı metraj, fatura, ödeme, banka/ERP kaydı.
3. Kalemleri normalize et: kod, açıklama, birim, sözleşme miktarı, önceki miktar, cari onaylı miktar, kümülatif miktar, birim fiyat.
4. Tutarları hesapla: önceki tutar, cari brüt, kümülatif hakediş, sözleşme üstü miktar, kesintiler, KDV/vergiler ve net ödenecek.
5. Kaynakları karşılaştır: hakediş vs metraj, hakediş vs fatura, fatura vs ödeme, ERP vs banka, önceki hakediş vs cari kümülatif.
6. Farkları sınıflandır: miktar farkı, tutar farkı, birim fiyat farkı, duplicate poz, eksik fatura, eksik ödeme, fazla ödeme, sözleşme üstü miktar, kesinti uyuşmazlığı.
7. Onay sınırını yaz: vergi, sözleşme, ceza, teminat ve ödeme kararı teknik/ticari/muhasebe onayı gerektirir.
8. Sonraki skill'i öner: teklif-maliyet, metraj-mahal, teknik şartname, müşteri/taşeron iletişimi veya risk-uygunluk denetimi.

## Çıktı Formatı

```markdown
## Hakediş / Mutabakat Özeti

## Kaynaklar ve Varsayımlar

## Sözleşme ve Önceki Hakediş Kontrolü

## Cari Hakediş Hesabı

## Kesinti, Avans, Teminat ve KDV

## Fatura / Ödeme Mutabakatı

## Fark ve Uyuşmazlık Tablosu

## Kritik QA Bayrakları

## Onay Sınırı ve Sonraki Aksiyonlar
```

Makine çıktısı için `references/cikti-semalari.md` içindeki JSON şemalarını kullan.

## Kalite Kapısı

- Her kalemde kod, açıklama, birim, önceki/cari/kümülatif miktar ve birim fiyat bulunmalıdır.
- Kümülatif miktar önceki miktardan küçükse revizyon/geri alma açıklaması gerekir.
- Kümülatif miktar sözleşme miktarını aşıyorsa iş artışı/variation onayı aranır.
- Fatura tutarı ve hakediş net tutarı birebir eşleşmeyebilir; KDV, kesinti, avans, teminat ve stopaj mantığı ayrıştırılır.
- Ödeme kaydı, dekont/banka/ERP referansı olmadan "ödenmiş" kabul edilmez.
- Vergi, stopaj, KDV, damga vergisi ve yasal kesintiler yerel mevzuata bağlıdır; onay gerekir.
- Spreadsheet formülü tek doğruluk kaynağı kabul edilmez; Python/CSV hesap sonucu ile çapraz kontrol edilir.

## Referanslar

- Açık kaynak araştırması: `references/acik-kaynak-arastirma.md`
- Araç seçim matrisi: `references/arac-secim-matrisi.md`
- Hakediş iş akışı: `references/hakedis-is-akisi.md`
- Mutabakat kontrol kuralları: `references/mutabakat-kontrol-kurallari.md`
- Kesinti, avans, teminat ve KDV notları: `references/kesinti-avans-teminat-kdv-notlari.md`
- Veri kolonları ve şema notları: `references/veri-kolonlari-ve-sema-notlari.md`
- Çıktı şemaları: `references/cikti-semalari.md`

## Yardımcı Scriptler

- `scripts/check_progress_payment_tools.py`: hakediş, mutabakat, tablo, PDF, ERP ve 5D araç durumunu raporlar.
- `scripts/plan_progress_payment_route.py`: kontrol tipine göre araç rotası, QA kapıları ve çıktı seti üretir.
- `scripts/calculate_progress_payment.py`: JSON sözleşme/hakediş girdisinden cari hakediş, kesinti ve net ödeme hesabı üretir.
- `scripts/compare_progress_sources.py`: JSON/CSV kaynaklar arasında kod bazlı miktar/tutar mutabakat farklarını çıkarır.
