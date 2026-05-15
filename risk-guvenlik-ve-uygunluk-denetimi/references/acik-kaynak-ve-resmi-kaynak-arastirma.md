# Açık Kaynak ve Resmi Kaynak Araştırması

Bu skill hibrit bir denetim yaklaşımı kullanır: resmi İSG kaynakları güvenlik kontrol mantığını, açık kaynak araçlar ise veri doğrulama, BIM uygunluk, kanıt izlenebilirliği ve aksiyon takibini besler.

## Resmi / Otorite Kaynakları

| Kaynak | Kullanım | Not |
|---|---|---|
| OSHA Recommended Practices for Safety and Health Programs in Construction | Program çekirdeği, tehlike tanımlama, önleme/kontrol, eğitim ve sürekli iyileştirme başlıkları | ABD merkezli kaynaktır; yerel mevzuat yerine geçmez. |
| NIOSH Construction Workers | Şantiye çalışanlarına yönelik genel tehlike ve korunma farkındalığı | Eğitim ve saha kontrol dili için referans. |
| HSE Construction | Rol bazlı sorumluluk, saha planı, CDM ve temel güvenlik akışı | Birleşik Krallık bağlamlıdır; workflow disiplini için kullanılır. |
| EU-OSHA | Avrupa iş sağlığı ve güvenliği bilgi kaynağı | Avrupa kaynaklı risk/önleme yaklaşımı için referans. |
| Türkiye ÇSGB Güvenli İnşaat mevzuat sayfası | Türkiye'de yapı işleri ve genel İSG mevzuatı bağlantı haritası | Güncel madde metni için mevzuat.gov.tr veya Resmi Gazete kaynağı ayrıca doğrulanmalıdır. |

## Açık Kaynak / Açık Standart Referansları

| Kaynak | Kullanım | Neden alındı |
|---|---|---|
| IfcOpenShell IfcTester | IFC modelini IDS gereksinimleriyle denetleme, JSON/HTML/ODS/BCF raporu üretme | BIM uygunluk kontrolü için pratik açık kaynak çekirdek. |
| buildingSMART IDS | Model bilgi gereksinimlerini makine okunur şekilde tanımlama | Uygunluk gereksinimini "metin yorumundan" kontrol edilebilir kurala çevirir. |
| buildingSMART BCF API | BIM issue, viewpoint ve model bağlantılı uygunsuzluk paylaşımı | Risk ve uygunsuzlukların model konumu ile takip edilmesini sağlar. |
| OpenProject BIM | Açık kaynak proje/issue takibi, IFC viewer ve BCF issue yönetimi | Saha aksiyonlarını work package, sorumlu, durum ve terminle takip etmeye uygundur. |
| NIST OSCAL | Kontrol bazlı uyumluluk bilgisini JSON/XML/YAML ile makine okunur taşıma | İnşaat mevzuatı değildir; kanıt ve kontrol kataloğu tasarımına örnek alınır. |
| OpenSCAP | Uyumluluk taraması ve raporlama için açık kaynak compliance-as-code örneği | Kanıt zinciri ve otomasyon disiplini için referans. |
| Frictionless | Tablo, kaynak, paket ve şema doğrulama | Denetim checklist'i ve kanıt tablolarında kolon/veri kalite kontrolü. |
| Great Expectations | Veri kalite beklentileri ve test yaklaşımı | Büyük/tekrarlı denetim veri setleri için kalite kapısı. |

## Hibrit Çalışma Kararı

1. Mevzuat ve güvenlik yorumu resmi kaynaklardan ve proje prosedürlerinden gelir.
2. Risk skorlama ve checklist otomasyonu yerel scriptlerle yapılır; resmi karar üretmez.
3. IFC/IDS ve BCF, model tabanlı uygunsuzluk ve kanıt izlenebilirliğinde kullanılır.
4. OSCAL/OpenSCAP yaklaşımı, inşaat dışı olsa da "kontrol -> kanıt -> değerlendirme -> rapor" veri modelini güçlendirir.
5. Frictionless/GX, CSV/JSON/XLSX gibi denetim verilerinin güvenilirliğini kontrol eder.

## Kaynak Linkleri

- OSHA Recommended Practices: https://www.osha.gov/safety-management/download-recommended-practices
- NIOSH Construction Workers: https://www.cdc.gov/niosh/docs/2023-115/default.html
- HSE Construction: https://www.hse.gov.uk/construction/new-health-safety.htm
- EU-OSHA: https://osha.europa.eu/en
- ÇSGB Güvenli İnşaat Mevzuat: https://guvenliinsaat.csgb.gov.tr/mevzuat/
- IfcOpenShell IfcTester: https://docs.ifcopenshell.org/ifctester.html
- buildingSMART IDS: https://github.com/buildingSMART/IDS
- buildingSMART BCF API: https://github.com/buildingSMART/BCF-API
- OpenProject BIM: https://www.openproject.org/bim-project-management/
- NIST OSCAL: https://pages.nist.gov/OSCAL/
- OpenSCAP: https://github.com/OpenSCAP/openscap
- Frictionless validation: https://framework.frictionlessdata.io/docs/guides/validating-data.html
- Great Expectations: https://greatexpectations.io/
