---
name: risk-guvenlik-ve-uygunluk-denetimi
description: İnşaat risk kaydı, İSG saha denetimi, çalışma izni, uygunsuzluk, kanıt/evidence kontrolü, BIM/IFC IDS uyumluluk denetimi, BCF issue ve kapatma aksiyonu hazırlamak için kullanılır.
---

# Risk, Güvenlik ve Uygunluk Denetimi

## Ne Zaman Kullanılır

- Kullanıcı inşaat projesi için risk değerlendirmesi, İSG denetimi, uygunsuzluk listesi, çalışma izni kontrolü, saha güvenliği checklist'i veya aksiyon planı istediğinde.
- Risk kaydı; olasılık, şiddet, mevcut kontrol, artık risk, sorumlu, termin ve kanıt durumuna göre skorlanacağı zaman.
- Mevzuat, standart, teknik şartname, işveren prosedürü veya saha talimatı gereksinimleri kanıtlarla eşleştirileceğinde.
- IFC/IDS tabanlı BIM uygunluk kontrolü, BCF issue üretimi veya OpenProject benzeri issue takibi için araç rotası seçileceğinde.
- Denetim çıktısının bağlayıcı karar değil; kontrol, eksik kanıt, risk bayrağı ve onay gerektiren aksiyon listesi olması gerektiğinde.

Bu skill iş güvenliği uzmanı, yapı denetim, hukuk, resmi uygunluk beyanı veya saha çalışmasını durdurma kararı yerine geçmez. Yerel mevzuat, proje sözleşmesi ve saha yetkilileri esas alınmalıdır.

## Girdi

- Proje bağlamı: ülke/şehir, iş tipi, işveren prosedürü, sözleşme, faz, mahal, disiplin, yüklenici/taşeron, denetim tarihi.
- Risk verisi: tehlike, faaliyet, lokasyon, etkilenen kişiler, olasılık, şiddet, mevcut kontroller, artık risk, sorumlu, termin, durum.
- Uygunluk kaynağı: mevzuat maddesi, standart, teknik şartname, method statement, ITP, işveren kontrol listesi, IDS dosyası, çalışma izni formu.
- Kanıtlar: fotoğraf, PDF, saha formu, sertifika, eğitim kaydı, ekipman periyodik kontrolü, izin formu, model elemanı, BCF issue, tutanak.
- Teslim formatı: Markdown denetim raporu, JSON, CSV, risk register, uygunsuzluk listesi, aksiyon planı veya BCF/issue özet seti.

## Araç Stratejisi

| Durum | İlk tercih | İkinci tercih | Not |
|---|---|---|---|
| Risk kaydı skorlama | `score_risk_register.py` | spreadsheet | Olasılık x şiddet matrisi, artık risk, overdue ve eksik kontrol bayrakları. |
| Uygunluk checklist denetimi | `audit_compliance_checklist.py` | Frictionless / Great Expectations | Gereksinim, kanıt, durum ve sorumlu eşleştirme. |
| BIM/IFC uygunluk | IfcOpenShell IfcTester + IDS | BIM skill'i | IFC modelini IDS gereksinimleriyle denetle; raporu JSON/HTML/BCF'e çevir. |
| BIM issue takibi | BCF API / OpenProject BIM | BCF XML | Uygunsuzluğu viewpoint, element GUID, sorumlu, öncelik ve due date ile izlenebilir yap. |
| Uyumluluk-as-code | OSCAL / OpenSCAP yaklaşımı | JSON/YAML kontrol kataloğu | İnşaat dışı formatlar doğrudan mevzuat değildir; kanıt modeli ve otomasyon disiplini için referanstır. |
| Tablo/veri kalite kontrolü | Frictionless / Great Expectations | stdlib validator | Kolon, zorunlu alan, enum, tarih, benzersiz id ve şema kontrolü. |
| Saha İSG kontrolü | OSHA / HSE / NIOSH / yerel mevzuat kaynakları | işveren prosedürü | Güncel ve yetkili kaynak doğrulanmadan mevzuat iddiası kurma. |
| Aksiyon yönetimi | OpenProject work package / issue tracker | Markdown aksiyon tablosu | Her bulguya sorumlu, termin, kanıt, durum ve kapatma kriteri bağla. |

## İş Akışı

1. Denetim kapsamını sabitle: proje, lokasyon, iş tipi, tarih, taraflar, geçerli kaynaklar ve dış kapsam.
2. Gereksinim kataloğunu çıkar: mevzuat/prosedür/şartname/IDS maddelerini tekil id ile listele.
3. Kanıt envanterini normalize et: belge, fotoğraf, eğitim kaydı, ekipman kontrolü, saha formu, model veya BCF issue.
4. Riskleri tanımla: tehlike, maruziyet, etkilenen kişi, mevcut kontrol, eksik kontrol, olasılık, şiddet, artık risk.
5. Uygunluk denetimi yap: her gereksinim için uygun, uygunsuz, eksik kanıt, uygulanmaz veya beklemede durumu üret.
6. Önceliklendir: yüksek/çok yüksek artık risk, kanıtsız kritik kontrol, termin geçmiş aksiyon ve tekrarlayan uygunsuzluklar en üste alınır.
7. Aksiyon planını yaz: kapatma kriteri, sorumlu, termin, kanıt tipi, doğrulama yöntemi ve onay gerektiren kararlar.
8. Çıktıyı sınırlı ifade et: "kesin uygunluk" yerine "sağlanan kanıta göre", "eksik kanıt", "yetkili doğrulama gerekir" gibi kanıt temelli dil kullan.

## Çıktı Formatı

```markdown
## Risk / Güvenlik / Uygunluk Denetim Özeti

## Kapsam ve Geçerli Kaynaklar

## Kritik Bulgular

## Risk Register

## Uygunluk ve Kanıt Matrisi

## Uygunsuzluklar ve Aksiyon Planı

## BIM / BCF / Model Bulguları

## Onay Sınırı ve Kalan Risk
```

Makine çıktısı için `references/cikti-semalari.md` içindeki JSON şemalarını kullan.

## Kalite Kapısı

- Her mevzuat/standart/prosedür maddesinin kaynak adı, madde id'si, tarih/sürüm ve uygulanabilirlik notu olmalıdır.
- Kritik veya yüksek risklerde kontrol önlemi, sorumlu, termin ve kapatma kanıtı olmadan "kapanmış" denmez.
- Fotoğraf veya belge kanıtı tarih, lokasyon, ilişkilendirilen gereksinim ve doğrulama notu olmadan zayıf kanıt sayılır.
- Uygunsuzluk bulgusu, en az bir gereksinim id'sine ve bir kapatma kriterine bağlanmalıdır.
- BIM denetiminde element GUID, model dosyası, IDS/BCF referansı ve viewpoint bilgisi mümkünse korunmalıdır.
- Yerel mevzuat ve işveren prosedürü güncel değilse rapora "kaynak güncelliği doğrulanmadı" notu eklenir.
- Bu skill resmi uygunluk beyanı, hukuki görüş, İSG uzmanı kararı veya saha durdurma emri üretmez; yetkili onay gerekir.

## Referanslar

- Açık kaynak ve resmi kaynak araştırması: `references/acik-kaynak-ve-resmi-kaynak-arastirma.md`
- Araç seçim matrisi: `references/arac-secim-matrisi.md`
- Risk denetim iş akışı: `references/risk-denetim-is-akisi.md`
- İSG kontrol listesi: `references/isg-kontrol-listesi.md`
- Uygunluk ve kanıt kuralları: `references/uygunluk-ve-kanit-kurallari.md`
- Risk skorlama ve önceliklendirme: `references/risk-skorlama-ve-onceliklendirme.md`
- Çıktı şemaları: `references/cikti-semalari.md`

## Yardımcı Scriptler

- `scripts/check_risk_compliance_tools.py`: risk, İSG, BIM, veri kalite ve uygunluk araçlarının durumunu raporlar.
- `scripts/plan_risk_compliance_route.py`: iş tipine göre araç rotası, QA kapıları ve çıktı seti üretir.
- `scripts/score_risk_register.py`: risk kayıtlarını olasılık, şiddet, artık risk, termin ve kanıt durumuna göre skorlar.
- `scripts/audit_compliance_checklist.py`: gereksinim checklist'i ile kanıt listesinin uygunluk durumunu denetler.
