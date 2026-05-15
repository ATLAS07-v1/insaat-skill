# Fiyat ve Risk Notları

## Fiyat Kaynağı Sınıfları

- `user_provided`: kullanıcı verdi; tarih ve kapsam sorulur.
- `supplier_quote`: taşeron/tedarikçi teklifi; kapsam ve istisna eşitlenir.
- `open_database`: açık kaynak veri tabanı; bölge/tarih/lisans doğrulanır.
- `historical_project`: önceki proje verisi; eskalasyon ve kapsam farkı gerekir.
- `live_market_research`: canlı web araştırması; kaynak linki ve tarih yazılır.

## Risk Başlıkları

- Fiyat eskalasyonu.
- Döviz kuru.
- Nakliye ve lojistik.
- Tedarik süresi.
- Marka/model muadili.
- Metraj belirsizliği.
- Şartname belirsizliği.
- Taşeron istisnası.
- İş programı hızlandırma.
- Vergi ve sözleşme özel şartları.

## Raporlama Dili

- Güncel fiyat doğrulanmadıysa "yaklaşık maliyet" yaz.
- KDV dahil/hariç açık değilse toplam bağlayıcı verilmez.
- Kur kullanılacaksa kur tarihi ve kaynak yaz.
- Taşeron teklifleri sadece toplam fiyatla değil, kapsam ve riskle karşılaştırılır.
- Müşteri metninde "nihai teklif" yerine "taslak teklif / ön maliyet çalışması" kullanılır; kullanıcı açıkça bağlayıcı teklif isterse onay sınırı belirtilir.
