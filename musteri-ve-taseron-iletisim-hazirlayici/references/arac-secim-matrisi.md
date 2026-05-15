# Araç Seçim Matrisi

## İletişim Tipine Göre Rota

| İş tipi | Veri | Ana araç | Destek araç | Çıktı |
|---|---|---|---|---|
| Müşteri durum güncellemesi | proje durumu, risk, karar, aksiyon | `draft_construction_message.py` | OpenProject / ERPNext | resmi e-posta, aksiyon listesi |
| Taşeron iş talimatı | mahal, çizim revizyonu, kapsam, termin | `draft_construction_message.py` | OpenProject work package | saha talimatı, takip görevi |
| RFI | soru, referans, etki, beklenen cevap | `draft_construction_message.py` | OpenProject / ERPNext | RFI e-postası, kayıt özeti |
| Submittal / transmittal | belge listesi, revizyon, ekler | `draft_construction_message.py` | doküman yönetimi | transmittal notu, ek listesi |
| Toplantı tutanağı | katılımcı, karar, aksiyon, tarih | OpenProject Meetings modeli | `validate_communication_pack.py` | tutanak, aksiyon tablosu |
| Müşteri destek/talep | çok kanallı talep | Chatwoot / Zammad | CRM | conversation/ticket özeti |
| CRM kayıt hazırlığı | kişi, kurum, proje, fırsat, konu | EspoCRM / SuiteCRM / ERPNext | Dolibarr | CRM kayıt taslağı |
| BIM issue iletişimi | IFC, viewpoint, BCF, issue | OpenProject BIM / BCF | BIM skill'i | model tabanlı issue mesajı |
| İç operasyon mesajı | kısa bilgi, görev, aciliyet | Mattermost | Markdown | kanal mesajı, playbook adımı |

## Seçim Kuralları

- Resmi ve kayıt altına alınması gereken konularda e-posta/tutanak formatını tercih et.
- Hızlı saha koordinasyonunda kısa mesaj kullanılabilir; ancak karar ve talimatlar sonradan kayıt altına alınmalıdır.
- Müşteri mesajında ticari/sözleşmesel risk varsa yetkili onay olmadan gönderim önerme.
- Taşeron talimatında çizim revizyonu, mahal, kapsam, güvenlik/kalite koşulu ve termin açık olmalıdır.
- RFI'da "karar istenen soru" net değilse önce soru formunu düzelt.
- Submittal/transmittal'da ek listesi, revizyon ve teslim amacı yazılmadan paket tamam sayılmaz.
