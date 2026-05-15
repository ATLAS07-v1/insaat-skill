# Açık Kaynak Araştırması

Bu skill, temel metraj/malzeme hesaplarında deterministik formül ve stdlib scriptleri kullanır. İleri mühendislik hesaplarında ise açık kaynak hesap motorlarına yönlendirir ve sonucun uzman onayı gerektirdiğini açıkça yazar.

## Ana Referanslar

| Kaynak | Rol | Skill'e Alınan İlke |
|---|---|---|
| https://github.com/hgrecco/pint | Birim dönüşümü ve boyutsal kontrol | Karışık birimli hesaplarda boyutsal hata riskini azaltır. |
| https://github.com/sympy/sympy | Sembolik matematik | Formül türetme, denklem çözme ve hesap açıklığı. |
| https://github.com/IfcOpenShell/IfcOpenShell | IFC okuma/geometri/quantity | BIM modelinden quantity alma ama model QA şartı. |
| https://docs.ifcopenshell.org/ifc5d.html | Ifc5D maliyet/quantity araçları | 5D ve quantity ilişkili veri işleme rotası. |
| https://github.com/datadrivenconstruction/QuantityTakeoff-Python | Revit/IFC kaynaklı quantity takeoff örneği | Filtreli gruplama ve volume toplama yaklaşımı. |
| https://github.com/JWock82/Pynite | 3D elastik yapısal analiz | Basit 3D FEA için açık kaynak rota; proje onayı değildir. |
| https://github.com/anastruct/anaStruct | 2D frame/truss analizi | Kiriş/çerçeve/truss ön analiz rotası. |
| https://hpgavin.github.io/frame3dd/ | 2D/3D frame/truss statik/dinamik analiz | CSV/text tabanlı açık kaynak frame analiz alternatifi. |
| https://github.com/OpenSees/OpenSees | Nonlinear/deprem/geoteknik simülasyon | Uzman modelleme ve doğrulama gereken ileri analiz. |
| https://github.com/zhuminjie/OpenSeesPy | OpenSees Python arayüzü | Python ile ileri OpenSees modeli; lisans/saha kullanımı kontrol edilir. |
| https://github.com/robbievanleeuwen/section-properties | Kesit özellikleri | Karma kesit alan, atalet, gerilme görselleştirme. |
| https://github.com/robbievanleeuwen/concrete-properties | Betonarme kesit özellikleri | Brüt, çatlamış, ultimate ve moment-eğrilik analizleri için açık kaynak rota. |
| https://github.com/fib-international/structuralcodes | Tasarım kodu yardımcıları | Kod tabanlı hesaplarda sürüm ve yönetmelik açık yazılır. |

## Hibrit Sonuç

1. Günlük metraj ve malzeme hesabı bu skill içinde deterministic script ile yapılır.
2. Birim dönüşümü ve formül kontrolünde Pint/SymPy tercih edilir.
3. BIM kaynaklı quantity verileri IfcOpenShell/Ifc5D hattına yönlendirilir.
4. Taşıyıcı sistem hesapları yalnız ön analiz/rota olarak ele alınır.
5. Kesin proje hesabı veya mevzuat uygunluğu için uzman onayı zorunlu bayraklanır.
