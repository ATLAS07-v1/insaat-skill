# Araç Seçim Matrisi

## İş Tipine Göre Rota

| İş tipi | Veri | Ana araç | Destek araç | Çıktı |
|---|---|---|---|---|
| Saha İSG denetimi | checklist, fotoğraf, aksiyon | `audit_compliance_checklist.py` | Frictionless, Markdown | Uygunluk matrisi, uygunsuzluk, aksiyon planı |
| Risk değerlendirme | risk register | `score_risk_register.py` | spreadsheet | Risk skoru, artık risk, öncelik listesi |
| Method statement / JSA kontrolü | method statement, faaliyet listesi | checklist audit | resmi kaynak/prosedür | Eksik kontrol, gerekli izin ve kanıt listesi |
| Çalışma izni denetimi | permit, ekipman kontrolü, eğitim | checklist audit | PDF extractor, OCR | Geçerli/geçersiz izin ve eksik ekler |
| BIM uygunluk denetimi | IFC + IDS | IfcOpenShell IfcTester | BCF reporter | IDS pass/fail raporu, BCF issue |
| Uygunsuzluk aksiyon takibi | bulgu, sorumlu, termin | OpenProject / BCF | Markdown tablo | Work package/issue özeti |
| Denetim veri kalite kontrolü | CSV/JSON/XLSX | Frictionless / GX | `audit_compliance_checklist.py` | Şema hatası, eksik kolon, hatalı enum |
| Compliance-as-code tasarımı | kontrol kataloğu | OSCAL yaklaşımı | OpenSCAP yaklaşımı | Kontrol, kanıt, değerlendirme veri modeli |

## Araç Seçim Kuralları

- IFC modeli ve IDS gereksinimi varsa önce IfcTester kullan; metin tabanlı yorumla yetinme.
- BCF veya OpenProject kullanılıyorsa her bulguya model viewpoint, sorumlu, termin ve durum bağla.
- Sadece PDF/fotoğraf varsa önce kanıt envanteri çıkar; görselden kesin mevzuat uygunluğu iddia etme.
- CSV/JSON veri varsa önce şema ve zorunlu alan kontrolü yap; veri bozuksa analiz sonucunu sınırlı raporla.
- Yerel mevzuat isteniyorsa güncel resmi kaynak doğrulanmadan kanuni hüküm üretme.
- Kritik İSG bulgularında "öneri" dili kullan; yetkili saha/İSG onayı gerektiğini belirt.

## Minimum Kurulum

- Python stdlib: JSON/CSV parsing, risk skorlama ve basit checklist denetimi için yeterlidir.
- pandas/xlsxwriter: büyük tabloları işlemek ve XLSX rapor üretmek için kullanışlıdır.
- pypdf/pdfplumber/OCR: PDF ve tarama kaynaklardan veri çıkarımı için opsiyoneldir.
- ifcopenshell/ifctester: IFC/IDS denetimi için gerekir.
- frictionless/great_expectations/jsonschema: veri kalite ve şema kontrollerini güçlendirir.
- OpenProject/BCF: aksiyon ve BIM issue takibi için kullanılır.
