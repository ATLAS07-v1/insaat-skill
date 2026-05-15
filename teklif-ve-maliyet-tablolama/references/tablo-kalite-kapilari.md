# Tablo Kalite Kapıları

## Zorunlu Kontroller

- Her kalemde açıklama, miktar, birim ve birim fiyat var mı?
- Miktar ve fiyat sayısal mı?
- Negatif miktar veya fiyat var mı?
- Sıfır fiyatlı kalem bilerek mi bırakılmış?
- Duplicate poz kodu var mı?
- Aynı kapsam iki kez sayılmış mı?
- Kategori toplamları ana toplamla uyuşuyor mu?
- KDV ve markup hesap sırası açık mı?
- Para birimi karışık mı?
- Fiyat tarihi ve kaynak yazılmış mı?

## Toleranslar

- Satır toplam farkı: varsayılan 0.01 para birimi.
- Toplam farkı: varsayılan 0.05 para birimi.
- Fire uyarı eşiği: varsayılan yüzde 25.
- Genel gider/kar/risk oranları proje bağlamına göre değişir; aşırı oranlar manuel inceleme bayrağı alır.

## Spreadsheet Riskleri

- Formüller elle değişmiş olabilir.
- Gizli satır/sütun toplamları etkileyebilir.
- Kopyala-yapıştır ile para birimi veya ondalık ayraç bozulabilir.
- `openpyxl` formül hesaplamaz; mevcut dosyadaki son hesaplanmış değeri okuyabilir.
- Excel/LibreOffice formül yeniden hesaplaması ile Python hesap sonucu karşılaştırılmalıdır.
