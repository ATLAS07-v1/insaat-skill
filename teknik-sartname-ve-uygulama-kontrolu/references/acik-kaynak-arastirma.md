# Açık Kaynak Araştırması

Bu skill için açık kaynak ve açık standart referansları, şartname maddesini makine-okunur kontrol listesine çevirmek ve uygulama kanıtını izlenebilir biçimde eşlemek için seçildi.

## Çekirdek Referanslar

| Referans | Kullanım | Hibrit yaklaşımdaki rol |
|---|---|---|
| buildingSMART IDS | BIM bilgi gereksinimlerini XML tabanlı, makine-okunur kurallara çevirmek | IFC model bilgi şartlarını manuel yorumdan çıkarıp IDS/IfcTester kontrolüne bağlar. |
| IfcOpenShell IfcTester | IDS dosyasını IFC modeline karşı doğrulamak, konsol/HTML/JSON/ODS/BCF raporları üretmek | Model parametre, sınıflandırma, property ve quantity kontrolü için doğrulama motoru. |
| IfcOpenShell BIMTester | Gherkin tabanlı model testleri yazmak | "Verilen/Ne zaman/O zaman" tarzı kontrol senaryolarını BIM QA'ya taşır. |
| buildingSMART BCF API | BIM uygunsuzluklarını konu, yorum, dosya ve viewpoint olarak paylaşmak | Uygunsuzluk ve eksik kanıt bulgularını takip edilebilir issue yapısına taşır. |
| OpenProject BCF API | Açık kaynak proje/issue yönetiminde BCF v2.1 uyumlu konu yönetimi | Saha/BIM bulgularının ekip takibine bağlanması için opsiyonel hedef. |
| WBDG UFGS | Kamuya açık teknik şartname kütüphanesi ve bölüm yapısı | Şartname bölüm/madde disiplinini anlamak için referans yapı; içerik kopyalanmaz. |
| pdfplumber / pypdf / PyMuPDF | PDF metin ve tablo çıkarımı | Teknik şartname PDF'lerinden madde adaylarını çıkarmak. |
| python-docx | DOCX şartname, tutanak ve tablo okuma | Word kaynaklarında başlık, paragraf ve tablo izini korumak. |
| Camelot | PDF tablo çıkarımı | Malzeme/test/tolerans tabloları için ikincil araç. |
| JSON Schema / Great Expectations | Veri kalite ve şema doğrulama | Çıktıların tekrar kullanılabilir, kontrol edilebilir JSON haline gelmesi. |
| Cucumber Gherkin | İnsan-okunur çalıştırılabilir şart senaryosu | Uygulama kontrollerini davranış testi formatına çevirmek için örüntü. |

## Hibrit Çalışma

1. Kaynak doküman metni deterministik araçlarla çıkarılır; sayfa, madde ve revizyon izi korunur.
2. Madde adayları zorunluluk kelimeleri, tolerans ifadeleri, test/rapor/sertifika/numune gereksinimleri ve uygulama emirleriyle sınıflandırılır.
3. Her madde kontrol listesine çevrilir: kontrol konusu, kabul kriteri, kanıt türü, sorumlu taraf ve uygunsuzluk eşiği.
4. BIM bilgi gereksinimi olan maddeler IDS veya BIMTester senaryosuna dönüştürülür.
5. Saha/test/submittal kanıtları madde id veya konu etiketi üzerinden eşleştirilir.
6. Eksik, çelişkili, tolerans dışı veya revizyon dışı kanıtlar takip aksiyonuna çevrilir.
7. BIM tabanlı uygunsuzluklar BCF topic taslağına veya OpenProject BCF iş akışına aktarılabilir.

## Kaynak Linkleri

- buildingSMART IDS: https://github.com/buildingSMART/IDS
- buildingSMART IDS tanımı: https://www.buildingsmart.org/what-is-information-delivery-specification-ids/
- IfcTester dokümantasyonu: https://docs.ifcopenshell.org/ifctester.html
- BIMTester dokümantasyonu: https://docs.ifcopenshell.org/bimtester.html
- buildingSMART BCF API: https://github.com/buildingSMART/BCF-API
- OpenProject API / BCF: https://www.openproject.org/docs/api/
- WBDG UFGS: https://www.wbdg.org/dod/ufgs
- pdfplumber: https://github.com/jsvine/pdfplumber
- pypdf: https://github.com/py-pdf/pypdf
- python-docx: https://github.com/python-openxml/python-docx
- Camelot: https://github.com/atlanhq/camelot
- Great Expectations: https://github.com/great-expectations/great_expectations
- Gherkin: https://github.com/cucumber/gherkin
