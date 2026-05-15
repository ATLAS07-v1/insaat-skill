# IDS ve BCF Model Kontrol Notları

## IDS Kullanımı

IDS, BIM bilgi gereksinimini insan-okunur ve makine-okunur bir yapıya taşımak için kullanılır. Bu skill içinde IDS, yalnız model içindeki bilgi şartlarını kontrol eder:

- IFC entity türü beklenen eleman mı?
- Zorunlu property/property set var mı?
- Property değeri beklenen değer veya aralıkta mı?
- Classification, material, type veya predefined type bilgisi var mı?
- Quantity veya base quantity alanı doldurulmuş mu?

## IfcTester Akışı

1. Şartname maddesinden model bilgi gereksinimini ayır.
2. Gereksinimi IDS specification, applicability ve requirement alanlarına dönüştür.
3. IFC modelini IfcTester ile doğrula.
4. JSON/HTML/ODS raporu üret.
5. Kritik fail kayıtları BCF topic taslağına dönüştür.

## BIMTester / Gherkin Akışı

BIMTester, model testlerini Gherkin cümleleriyle yazmak için uygundur. Örnek senaryo kalıbı:

```gherkin
Feature: Fire rating model requirements

  Scenario: Fire doors carry required classification
    Given the IFC model contains door elements
    Then every fire door shall have the required fire rating property
```

Bu kalıp kullanıcıya açık test dili verir; teknik uygulama IfcOpenShell/BIMTester tarafında yapılır.

## BCF Topic Taslağı

BCF, uygunsuzlukların model konumu ve ekip takibiyle paylaşılması için kullanılır.

```json
{
  "topic_type": "Issue",
  "topic_status": "Open",
  "title": "SPEC-014 eksik yangın dayanım property",
  "priority": "High",
  "labels": ["IDS", "Specification", "Fire"],
  "reference_links": ["model.ifc", "ids-report.json"],
  "description": "Şartname maddesi SPEC-014 gereği fire rating property zorunlu; IfcTester raporunda eksik görünüyor."
}
```

## Sınırlar

- IDS sonucu model verisinin şartnameye uygunluk göstergesidir; sahadaki imalat kalitesini tek başına doğrulamaz.
- BCF topic, resmi NCR veya kabul tutanağı yerine geçmez; takip ve koordinasyon çıktısıdır.
- Standart metni veya sözleşme önceliği kullanıcı tarafından verilmeden nihai uygunluk yorumu yapılmaz.
