# Açık Kaynak Araştırması

Bu skill, inşaat iletişimini tek başına mesaj yazma işi olarak değil; kayıt, aksiyon, müşteri ilişkisi, taşeron takip ve kanıt zinciri olan bir iş akışı olarak ele alır.

## Referans Alınan Açık Kaynak Araçlar

| Kaynak | Kullanım | Neden alındı |
|---|---|---|
| OpenProject | Work package, toplantı gündemi/tutanağı, aksiyon, issue, BIM/BCF iletişimi | İnşaat ve proje yönetiminde iş paketi, toplantı, sorumlu ve termin bağını iyi temsil eder. |
| OpenProject BIM / BCF | Model tabanlı issue ve koordinasyon iletişimi | BIM bulgularında viewpoint, model seçimi ve konu takibi için uygun. |
| ERPNext | CRM, proje, görev, satış/satın alma ve destek kayıtları | Müşteri/taşeron bağlamını proje, satın alma, hakediş ve teklif akışıyla ilişkilendirmek için. |
| Dolibarr | Kişi, müşteri, tedarikçi, teklif, sipariş, agenda ve ERP/CRM kayıtları | Hafif CRM/ERP mantığı ve küçük ekip operasyonları için referans. |
| EspoCRM | Açık kaynak CRM, özel entity/field ve REST API | Müşteri/kişi/hesap iletişim kaydı ve özel inşaat iletişim nesneleri için referans. |
| Chatwoot | Çok kanallı müşteri destek konuşmaları | E-posta, canlı chat ve sosyal kanal taleplerini tek conversation/ticket akışında düşünmek için. |
| Mattermost | Self-hosted ekip iletişimi, kanal, workflow ve playbook yaklaşımı | İç ekip ve saha operasyon mesajlarını kanal/takip mantığıyla hazırlamak için. |

## Hibrit Çalışma Kararı

1. Mesaj taslağı yerel script ve şablonlarla hazırlanır.
2. Takip gerektiren her mesaj issue/work package/task kaydına çevrilebilir yapıdadır.
3. Müşteri ve taşeron bağlamı CRM mantığıyla ayrılır: kişi, kurum, proje, konu, kayıt no, durum.
4. RFI/submittal/transmittal iletişiminde belge revizyonu, ekler, yanıt tarihi ve takip sorumlusu zorunlu kabul edilir.
5. Sözleşmesel veya hukuki sonuç doğurabilecek ifadeler otomatik olarak onay gerektirir.

## Kaynak Linkleri

- OpenProject GitHub: https://github.com/opf/openproject
- OpenProject Meetings: https://www.openproject.org/docs/user-guide/meetings/
- OpenProject BIM Issue Management: https://www.openproject.org/docs/bim-guide/bim-issue-management/
- ERPNext GitHub: https://github.com/frappe/erpnext
- Dolibarr GitHub: https://github.com/Dolibarr/dolibarr
- EspoCRM GitHub: https://github.com/espocrm/espocrm
- Chatwoot GitHub: https://github.com/chatwoot/chatwoot
- Mattermost GitHub: https://github.com/mattermost/mattermost
