---
name: musteri-ve-taseron-iletisim-hazirlayici
description: İnşaat projelerinde müşteri, işveren, taşeron, tedarikçi ve proje ekibi için RFI, submittal, transmittal, toplantı tutanağı, saha talimatı, aksiyon takibi, durum güncellemesi, gecikme/variasyon taslağı ve resmi olmayan iletişim paketleri hazırlamak için kullanılır.
---

# Müşteri ve Taşeron İletişim Hazırlayıcı

## Ne Zaman Kullanılır

- Kullanıcı müşteri, işveren, taşeron, tedarikçi veya saha ekibine gönderilecek e-posta, yazı, WhatsApp/Teams mesajı veya toplantı notu taslağı istediğinde.
- RFI, submittal, transmittal, saha talimatı, aksiyon takip listesi, haftalık durum özeti, eksik bilgi talebi, teslim/imalat teyidi veya uygunsuzluk yanıtı hazırlanacağında.
- Ton, kapsam, eksik bilgi, ekler, sorumlular, termin, kayıt numarası ve onay sınırı kontrol edileceğinde.
- OpenProject, ERPNext, Dolibarr, CRM/helpdesk veya kanal bazlı mesaj araçları için iletişim/issue/aksiyon kaydı tasarlanacağında.
- Mesaj gönderilmeden önce riskli ifade, eksik veri, kanıt eksikliği, sözleşmesel/hukuki risk ve onay gereksinimi işaretleneceğinde.

Bu skill üçüncü tarafla iletişime geçmez, e-posta göndermez, sözleşmesel bildirim veya hukuki ihtar yerine geçmez. Bağlayıcı, ticari, hukuki veya sözleşmesel mesajlar yetkili kişi tarafından onaylanmalıdır.

## Girdi

- Taraflar: müşteri/işveren, taşeron, tedarikçi, tasarımcı, danışman, saha ekibi, iç ekip.
- Konu: proje adı, iş paketi, mahal, disiplin, belge numarası, revizyon, tarih, termin, sözleşme/şartname referansı.
- İletişim tipi: RFI, submittal, transmittal, meeting minutes, saha talimatı, aksiyon takip, durum güncellemesi, gecikme/variasyon taslağı, ödeme/hakediş takip, tedarik takip.
- Gerçekler: doğrulanmış olaylar, ölçümler, kararlar, ekler, fotoğraflar, çizim/model referansları, önceki yazışmalar.
- İstenen aksiyon: cevap, onay, bilgi, revizyon, teslim, saha hazırlığı, toplantı, kapatma kanıtı.
- Ton ve kanal: resmi e-posta, kısa operasyon mesajı, toplantı tutanağı, müşteri özeti, taşeron iş talimatı, iç aksiyon notu.

## Araç Stratejisi

| Durum | İlk tercih | İkinci tercih | Not |
|---|---|---|---|
| Mesaj/eposta taslağı | `draft_construction_message.py` | Markdown şablonları | Konu, hitap, gerçekler, talep, termin, ekler ve onay sınırı üretir. |
| İletişim paketi kontrolü | `validate_communication_pack.py` | manuel QA | Eksik alan, riskli ifade, onay ihtiyacı ve ek kontrolü yapar. |
| İş takibi ve aksiyon | OpenProject work packages | ERPNext Projects / Odoo / Dolibarr | Sorumlu, termin, durum, toplantı sonucu ve issue bağlamak için. |
| CRM / müşteri ilişkisi | EspoCRM / SuiteCRM | ERPNext CRM / Dolibarr CRM | Müşteri, fırsat, hesap, kişi ve yazışma bağlamı için. |
| Destek/talep yönetimi | Chatwoot / Zammad | e-posta klasörü + tablo | Gelen müşteri taleplerini kanal bazlı ticket/conversation olarak toplamak için. |
| Ekip içi hızlı iletişim | Mattermost | Teams/Slack taslağı | Operasyonel kısa mesaj, playbook ve kanal notu hazırlamak için. |
| BIM model tabanlı iletişim | OpenProject BIM / BCF | BIM skill'i | Model viewpoint, element, issue ve sorumlu bağlamak için. |
| Belge ve tablo üretimi | DOCX/PDF/XLSX araçları | Markdown/CSV | Resmi yazı, toplantı tutanağı, aksiyon listesi ve transmittal formu için. |

## İş Akışı

1. İletişim tipini belirle: RFI, submittal, transmittal, toplantı, saha talimatı, müşteri güncellemesi, taşeron takip, gecikme/variasyon taslağı veya ödeme/hakediş takip.
2. Taraf ve kanal seç: müşteri, taşeron, tedarikçi, iç ekip; resmi e-posta, kısa mesaj, tutanak, issue veya CRM kaydı.
3. Gerçekleri ayır: doğrulanmış veri, varsayım, talep, risk, karar, bekleyen cevap ve ekler ayrı tutulur.
4. Referansları bağla: proje, sözleşme/şartname maddesi, çizim revizyonu, RFI/submittal no, önceki yazışma, toplantı kararı.
5. Mesajı hazırla: konu, kısa özet, arka plan, talep/aksiyon, termin, ekler, sorumlu ve kapanış.
6. Tonu düzelt: net, kayıt altına alınabilir, suçlayıcı olmayan, ölçülü ve aksiyon odaklı dil kullan.
7. Risk kontrolü yap: hukuki/sözleşmesel iddia, gecikme/variasyon, ödeme, kusur kabulü, ceza, fesih veya kesin taahhüt ifadelerini bayrakla.
8. Onay sınırını yaz: gönderim, temsil, sözleşmesel bildirim, finansal/hukuki taahhüt ve üçüncü taraf iletişimi yetkili onay gerektirir.

## Çıktı Formatı

```markdown
## İletişim Paketi Özeti

## Taslak Mesaj

## Ekler ve Referanslar

## Beklenen Aksiyonlar

## Riskli / Onay Gerektiren Noktalar

## Kayıt ve Takip Önerisi
```

Makine çıktısı için `references/cikti-semalari.md` içindeki JSON şemalarını kullan.

## Kalite Kapısı

- Mesaj gönderilecek taraf, proje, konu, talep, termin ve beklenen aksiyon net olmalıdır.
- Gerçek bilgi ile yorum/öneri ayrılmalıdır.
- Sözleşmesel, hukuki, finansal veya sorumluluk doğurabilecek ifadeler yetkili onaya ayrılmalıdır.
- Taşerona giden iş talimatı çizim revizyonu, mahal, kapsam, tarih ve güvenlik/kalite koşulu olmadan eksik sayılır.
- Müşteriye giden durum özeti problem saklamaz; fakat suçlayıcı ve kanıtsız ifade kullanmaz.
- RFI ve submittal iletişiminde kayıt numarası, revizyon, beklenen cevap tarihi ve ekler belirtilmelidir.
- Toplantı tutanağı karar, aksiyon, sorumlu, termin ve açık madde ayrımı yapmalıdır.

## Referanslar

- Açık kaynak araştırması: `references/acik-kaynak-arastirma.md`
- Araç seçim matrisi: `references/arac-secim-matrisi.md`
- İletişim iş akışı: `references/iletisim-is-akisi.md`
- Mesaj şablonları: `references/mesaj-sablonlari.md`
- RFI, submittal ve transmittal kuralları: `references/rfi-submittal-transmittal-kurallari.md`
- Toplantı, aksiyon ve takip kuralları: `references/toplanti-aksiyon-ve-takip-kurallari.md`
- Çıktı şemaları: `references/cikti-semalari.md`

## Yardımcı Scriptler

- `scripts/check_communication_tools.py`: iletişim, CRM, doküman ve tablo araçlarının durumunu raporlar.
- `scripts/plan_communication_route.py`: iş tipine göre kanal, çıktı, QA ve onay rotası üretir.
- `scripts/draft_construction_message.py`: yapılandırılmış girdiden mesaj/e-posta/tutanak taslağı üretir.
- `scripts/validate_communication_pack.py`: iletişim paketinde eksik alan, riskli ifade ve onay ihtiyacını kontrol eder.
