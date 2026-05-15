# Uygunluk ve Kanıt Kuralları

## Temel İlke

Uygunluk iddiası, gereksinim ve kanıt arasında izlenebilir bağ olmadan kurulmaz. Bu skill "kanıt temelli ön denetim" üretir; resmi uygunluk onayı üretmez.

## Gereksinim Kuralı

Her gereksinim şu alanlarla tanımlanmalıdır:

- `id`: benzersiz madde kodu
- `source`: mevzuat, standart, prosedür, şartname veya IDS adı
- `source_version`: tarih, revizyon veya erişim tarihi
- `requirement`: kontrol edilecek açık ifade
- `category`: İSG, kalite, çevre, BIM, ekipman, eğitim, belge, izin
- `mandatory`: zorunlu mu?
- `evidence_required`: kanıt gerekli mi?
- `acceptance_criteria`: geçme koşulu

## Kanıt Kuralı

Kanıt kabulü için minimum alanlar:

- `evidence_id`
- `requirement_id`
- `type`: photo, pdf, certificate, training_record, inspection_record, permit, ifc, ids_report, bcf_issue, minutes
- `file` veya `reference`
- `date`
- `owner`
- `status`: provided, accepted, rejected, expired, pending
- `notes`

## Durum Sözlüğü

| Durum | Anlam |
|---|---|
| `pass` | Gereksinim karşılanmış ve kanıt yeterli görünüyor. |
| `fail` | Gereksinim karşılanmamış, kanıt reddedilmiş veya açık uygunsuzluk var. |
| `missing_evidence` | Gereksinim için kanıt zorunlu fakat sağlanmamış. |
| `pending` | İnceleme, onay veya ek bilgi bekliyor. |
| `not_applicable` | Kapsama uygulanmıyor; gerekçesi yazılmalı. |

## Uygunsuzluk Açma Kriteri

Aşağıdaki durumlardan biri varsa uygunsuzluk açılır:

- Zorunlu gereksinim başarısız.
- Kritik/yüksek risk için kontrol veya kanıt eksik.
- Kanıt süresi geçmiş veya belge kaynağı doğrulanamıyor.
- Sorumlu ya da termin yok.
- Aynı bulgu tekrar ediyor.
- BIM/IFC kontrolünde IDS gereksinimi başarısız ve modele bağlı aksiyon gerekiyor.

## Kapatma Kriteri

Bir uygunsuzluk şu şartlar olmadan kapatılmaz:

- Düzeltici aksiyon tamamlandı.
- Kapatma kanıtı eklendi.
- Yetkili kişi doğruladı.
- Artık risk kabul edilebilir seviyeye indirildi veya risk kabulü belgelenmiş.
- Tarih ve sorumlu kaydı mevcut.

## Dil Sınırı

- "Kanıta göre uygundur" denebilir.
- "Eksik kanıt nedeniyle doğrulanamadı" denebilir.
- "Yerel mevzuat uzmanı/İSG uzmanı onayı gerekir" denmelidir.
- "Kesin mevzuata uygundur" veya "sahada güvenlidir" denmez.
