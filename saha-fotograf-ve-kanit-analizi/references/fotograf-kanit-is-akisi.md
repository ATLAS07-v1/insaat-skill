# Fotoğraf Kanıt İş Akışı

## 1. Teslim Alma

- Kaynak kişi/ekip
- Teslim tarihi
- Dosya kaynağı
- Orijinal klasör
- İş paketi veya saha amacı
- İlgili RFI/NCR/aksiyon/hakediş

## 2. Bütünlük Kaydı

Her dosya için:

- `evidence_id`
- `file_path`
- `file_name`
- `sha256`
- `file_size`
- `captured_at`
- `modified_at`
- `width`
- `height`
- `exif_present`
- `gps_present`

## 3. Bağlam Eşleştirme

- proje,
- blok/kat/mahal,
- disiplin,
- iş kalemi,
- taşeron,
- ilgili çizim/revizyon,
- ilgili aksiyon veya tutanak.

## 4. Görsel İnceleme

Gözlem şu ayrımla yazılır:

- fotoğrafta açıkça görülen,
- bağlamla desteklenen,
- varsayım,
- doğrulanması gereken,
- karar/aksiyon gerektiren.

## 5. Kanıt Seviyesi

| Seviye | Tanım |
|---|---|
| strong | Orijinal dosya, hash, tarih/konum, bağlam ve ilişkilendirilmiş aksiyon var. |
| medium | Dosya ve bağlam var; metadata veya ek doğrulama eksik. |
| weak | Metadata, mahal, tarih veya ilişki eksik; yalnızca görsel gözlem var. |
| rejected | Dosya açılamıyor, kaynak belirsiz, manipülasyon şüphesi veya kapsam dışı. |

## 6. Raporlama

- Kanıt register
- Özet bulgular
- Fotoğraf bazlı aksiyon
- Eksik kanıtlar
- Gizlilik ve paylaşım notu
- Yetkili doğrulama gereksinimi
