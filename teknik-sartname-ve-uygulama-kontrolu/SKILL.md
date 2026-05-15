---
name: teknik-sartname-ve-uygulama-kontrolu
description: İnşaat teknik şartname, uygulama kriteri, malzeme onayı, test raporu, tolerans, saha kanıtı ve BIM/IDS/BCF uygunsuzluk kontrolü yapmak için kullanılır.
---

# Teknik Şartname ve Uygulama Kontrolü

## Ne Zaman Kullanılır

- Kullanıcı teknik şartname, özel şartname, proje notu, uygulama metodu, malzeme submittal'ı, test raporu veya saha kontrol tutanağı incelemesi istediğinde.
- Şartname maddelerinin kontrol listesine çevrilmesi, kanıt gereksinimlerinin çıkarılması ve eksik kanıtların işaretlenmesi gerektiğinde.
- İmalatın teknik şartnameye uygunluğu; tolerans, malzeme, numune, sertifika, test, mock-up, fotoğraf, ölçüm veya kabul kriterleri üzerinden kontrol edileceğinde.
- IFC/BIM model bilgi gereksinimleri IDS ile doğrulanacak, uygunsuzluklar BCF/OpenProject benzeri konu akışına taşınacaksa.
- Müşteri, saha ekibi veya taşeron için teknik ama bağlayıcı olmayan kontrol özeti hazırlanacağında.

Bu skill teknik kontrol ve QA çıktısı üretir. Resmi kabul, mühendislik onayı, hukuki yorum, sözleşmesel karar, iş durdurma veya ödeme/hakediş kararı üretmez.

## Girdi

- Kaynak dokümanlar: PDF, DOCX, TXT/MD, CSV/XLSX tablo, şartname kesiti, uygulama metodu, malzeme onay formu, test raporu, saha kontrol kaydı.
- Kontrol hedefi: malzeme uygunluğu, uygulama yöntemi, tolerans, test/deney, numune/mock-up, teslim dokümanı, BIM bilgi gereksinimi veya saha kanıtı.
- Proje bağlamı: disiplin, mahal/kat, imalat kalemi, revizyon, sözleşme öncelik sırası, geçerli standart veya işveren kriteri.
- Kanıt seti: fotoğraf listesi, test raporları, sertifikalar, ölçüm kayıtları, BCF/issue kayıtları, IFC/IDS raporu, kontrol tutanağı.
- Kabul toleransı: şartnameden çıkarılır; belirsizse varsayım olarak değil soru/bayrak olarak raporlanır.

## Araç Stratejisi

| Durum | İlk tercih | İkinci tercih | Not |
|---|---|---|---|
| PDF şartname metni | pdfplumber / pypdf | PyMuPDF | Taranmış PDF için OCR gerekir; otomatik çıkarım güven bayrağı ister. |
| DOCX şartname | python-docx | pandoc | Paragraf, tablo ve başlık yapısı korunur. |
| Şartname maddesi ayıklama | Deterministik madde çıkarıcı | LLM destekli sınıflandırma | LLM sadece sınıflandırır; kaynak madde numarası korunur. |
| Tablo kontrolü | pandas / openpyxl | CSV stdlib | Malzeme, test ve tolerans tabloları için. |
| Şema/kanıt doğrulama | JSON Schema / Great Expectations | stdlib kontrol | Kontrol çıktıları tekrar kullanılabilir hale gelir. |
| BIM bilgi şartı | IDS + IfcTester | BIMTester/Gherkin | IFC bilgi gereksinimi için makine-okunur kontrol. |
| Uygunsuzluk/issue | BCF API / BCF dosyası | OpenProject BCF API | Konu, kanıt, viewpoint ve sorumlu takibi. |
| İlgili hesap | insaat-hesaplamalar | metraj-ve-mahal-kontrolu | Tolerans veya miktar kontrolünde kullanılır. |

## İş Akışı

1. Kaynakları sınıflandır: şartname, uygulama metodu, submittal, test raporu, saha kanıtı, IFC/IDS veya issue kaydı.
2. Kaynak güvenilirliğini yaz: dosya türü, revizyon, sayfa/madde izi, metin çıkarım kalitesi, eksik sayfa veya tarama riski.
3. Şartname maddelerini çıkar: zorunluluk kelimeleri, toleranslar, kabul kriterleri, test ve teslim gereksinimleri.
4. Maddeleri normalize et: madde id, disiplin, imalat kalemi, kontrol kategorisi, kanıt türü, kabul durumu, sorumlu taraf.
5. Kontrol listesi üret: her madde için "ne kontrol edilir", "hangi kanıt gerekir", "hangi tolerans/standart geçerli", "hangi durumda uygunsuzluk açılır".
6. Kanıt setiyle eşleştir: fotoğraf, ölçüm, test raporu, sertifika, malzeme datasheet, numune onayı, as-built veya IFC/IDS raporu.
7. Eksik ve çelişkili durumları sınıflandır: eksik kanıt, uygunsuz kanıt, belirsiz şartname, revizyon çakışması, tolerans dışı değer, onaysız malzeme.
8. BIM kontrolü varsa IDS/IfcTester rotası hazırla; uygunsuzluklar BCF topic taslağına dönüştürülür.
9. Çıktıyı üret: teknik kontrol özeti, madde bazlı tablo, kritik bayraklar, kanıt listesi, takip aksiyonları ve onay sınırı.

## Çıktı Formatı

```markdown
## Teknik Şartname / Uygulama Kontrol Özeti

## Kaynaklar ve Revizyonlar

## Madde Bazlı Kontrol Listesi

## Kanıt Eşleştirme

## Uygunsuzluk ve Eksik Kanıtlar

## Tolerans / Test / Submittal Kontrolleri

## BIM / IDS / BCF Notları

## Kritik Bayraklar

## Onay Sınırı ve Sonraki Aksiyonlar
```

Makine çıktısı için `references/cikti-semalari.md` içindeki JSON şemalarını kullan.

## Kalite Kapısı

- Her bulgu kaynak madde, sayfa, revizyon veya dosya izine bağlanmalıdır.
- Şartnamede açık olmayan toleranslar uydurulmaz; "belirsiz / onay gerekir" olarak bayraklanır.
- Standart, yönetmelik veya üretici datasheet içeriği kullanıcı tarafından sağlanmadıysa özet doğrulama yapılamaz; yalnız eksik kaynak olarak raporlanır.
- Taranmış PDF, düşük kaliteli fotoğraf veya elle yazılmış tutanak otomatik metin çıkarımı için düşük güvenli kabul edilir.
- Kanıt ve şartname revizyonu aynı tarih/versiyon bağlamına oturmuyorsa sonuç nihai uygunluk olarak sunulmaz.
- BIM/IDS kontrolü sadece model bilgi gereksinimini doğrular; sahadaki imalat kalitesini tek başına ispatlamaz.
- Hukuki, sözleşmesel, ödeme, iş durdurma veya resmi kabul kararları kullanıcı/teknik sorumlu onayı gerektirir.

## Referanslar

- Açık kaynak araştırması: `references/acik-kaynak-arastirma.md`
- Araç seçim matrisi: `references/arac-secim-matrisi.md`
- Şartname madde çıkarma kuralları: `references/sartname-madde-cikarma-kurallari.md`
- Uygulama kontrol listesi: `references/uygulama-kontrol-listesi.md`
- IDS ve BCF model kontrol notları: `references/ids-ve-bcf-model-kontrol-notlari.md`
- Çıktı şemaları: `references/cikti-semalari.md`

## Yardımcı Scriptler

- `scripts/check_spec_tools.py`: şartname/uygulama kontrolü için araç ve Python modül durumunu raporlar.
- `scripts/plan_spec_review_route.py`: kaynak türüne göre kontrol rotası, araçlar, QA kapıları ve çıktı seti üretir.
- `scripts/extract_spec_clauses.py`: TXT/MD/CSV/JSON/PDF/DOCX kaynaklardan şartname maddesi adaylarını çıkarır.
- `scripts/compare_evidence_to_checklist.py`: madde bazlı kontrol listesini kanıt kayıtlarıyla eşleştirir ve eksik/uygunsuz kanıtları raporlar.
