# Risk Denetim İş Akışı

## 1. Kapsamı Sabitle

- Proje, tarih, lokasyon, iş paketi, denetçi, yüklenici/taşeron ve işveren temsilcisi.
- Geçerli kaynaklar: yerel mevzuat, sözleşme, işveren prosedürü, teknik şartname, method statement, ITP, izin formu, IDS.
- Dış kapsam: görülmeyen alanlar, erişilemeyen belgeler, doğrulanmamış beyanlar.

## 2. Gereksinim Kataloğu Kur

Her gereksinim için:

- `id`
- `source`
- `source_version`
- `requirement`
- `category`
- `mandatory`
- `evidence_required`
- `acceptance_criteria`

## 3. Kanıt Envanteri Kur

Kanıtlar şu alanlarla tutulur:

- `evidence_id`
- `requirement_id`
- `type`
- `file`
- `date`
- `location`
- `owner`
- `status`
- `notes`

## 4. Risk Register Üret

Risk kaydı şu çekirdek alanları taşımalıdır:

- `id`
- `activity`
- `hazard`
- `affected_people`
- `location`
- `likelihood`
- `severity`
- `controls`
- `residual_likelihood`
- `residual_severity`
- `owner`
- `due_date`
- `evidence`
- `status`

## 5. Skorlama ve Uygunluk Denetimi

- Olasılık x şiddet ile doğal risk hesaplanır.
- Artık risk sadece kontrol önlemleri uygulandıktan ve değerlendirildikten sonra ayrıca yazılır.
- Eksik kanıt, geçersiz belge, geçmiş termin ve sahipsiz aksiyon ayrı bayraklanır.
- Uygunluk sonucu `pass`, `fail`, `missing_evidence`, `pending`, `not_applicable` değerlerinden biri olmalıdır.

## 6. Aksiyon Planı

Her aksiyon şu bilgileri içermelidir:

- Bulgu id'si
- Gereksinim veya risk id'si
- Aksiyon
- Sorumlu
- Termin
- Kapatma kanıtı
- Doğrulama yöntemi
- Kalan risk

## 7. Raporlama Dili

- "Sağlanan kanıta göre uygun görünüyor" kullan.
- "Kanıt eksik olduğu için uygunluk doğrulanamadı" kullan.
- "Kritik risk, yetkili İSG/saha sorumlusu değerlendirmesi gerekir" kullan.
- "Kesin uygundur", "mevzuata tam uygundur" veya "sahada güvenlidir" gibi bağlayıcı ifadeleri kullanma.
