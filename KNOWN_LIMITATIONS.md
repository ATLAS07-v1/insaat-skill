# Known Limitations

Bu dosya `v0.1.0` için bilinçli kapsam sınırlarını ve güvenli kullanım notlarını listeler.

## Execution Safety

- LLM tarafından üretilen Python, Ruby, Blender, SketchUp veya CAD komutları doğrudan host işletim sisteminde çalıştırılmamalıdır.
- `sandbox_required: true` olan skill'ler izole çalışma dizini, süre limiti ve mümkünse container veya VM sınırı ile çalıştırılmalıdır.
- Harici uygulama çağrıları dosya yazabilir, uzun sürebilir veya lisanslı/proprietary araç gerektirebilir.
- Agent, kullanıcı onayı olmadan dosya silme, overwrite, dış sisteme gönderim, satın alma, ödeme, resmi onay veya üçüncü taraf iletişimi yapmamalıdır.

## v0.1.0 Kapsam Dışı Alanlar

Şu alanlar bu sürümde ayrı skill olarak yer almaz:

- iş programı, Primavera P6, MS Project, CPM, delay analysis,
- sözleşme, claim, süre uzatımı ve hukuki ihtilaf analizi,
- MEP koordinasyon ve disiplin bazlı tesisat kontrolü,
- geoteknik ve zemin etüdü uzman analizi,
- taşıyıcı sistem hesabı, deprem/yapısal nihai mühendislik kontrolü,
- drone fotogrametri, point cloud ve OpenDroneMap/WebODM iş akışları,
- ERP/muhasebe aktarım şemaları ve canlı sistem entegrasyonu.

Bu alanlar `v0.2+` domain genişletme adaylarıdır.

## Test Sınırı

- CI hızlı smoke ve schema doğrulaması yapar; ağır CAD/BIM/OCR araçlarının gerçek doğruluk testi her ortamda çalıştırılmaz.
- Opsiyonel araç yoksa ilgili script anlaşılır hata veya plan çıktısı üretmelidir.
- Resmi şantiye, finans, hukuk, İSG veya teknik kararlar yetkili insan onayı gerektirir.

## Data Privacy

- Fotoğraf, EXIF, GPS, yüz, plaka, imza, sözleşme, fiyat ve kişisel veri içeren dosyalar paylaşım öncesi ayrıca temizlenmelidir.
- Bu repo veri anonimleştirme veya otomatik gizlilik garantisi vermez.
