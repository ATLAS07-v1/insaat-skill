# Araç Seçim Matrisi

| İhtiyaç | İlk Tercih | İkinci Tercih | Risk |
|---|---|---|---|
| Alan/hacim/metraj | stdlib hesap script'i | Spreadsheet skill | Ölçü/boşluk/fire eksikleri |
| Donatı yaklaşık kg | stdlib formül | betonarme uzman kontrolü | bindirme, kanca, zayiat, proje detayı |
| Beton/kalıp | stdlib formül | metraj-mahal skill'i | çift sayım ve açıklık düşümü |
| Birim dönüşümü | Pint | stdlib dönüşüm tablosu | cm-mm-m karışması |
| Formül doğrulama | SymPy | manuel ara adım | yanlış denklem kurulumu |
| BIM quantity | IfcOpenShell / Ifc5D | BIM skill'i | quantity set eksikliği |
| 2D kiriş/çerçeve | anaStruct | Frame3DD | model varsayımı ve mesnet/yük hatası |
| 3D elastik frame | PyNite | Frame3DD | sadece elastik/ön analiz |
| Nonlinear/deprem | OpenSeesPy | OpenSees Tcl | ileri uzmanlık gerekir |
| Kesit özellikleri | sectionproperties | el formülü | karma kesit ve birim hatası |
| Betonarme kesit | concreteproperties | structuralcodes | mevzuat ve kullanıcı sorumluluğu |

## Varsayılan Rota

1. Basit metraj ise bu skill scriptleriyle hesapla.
2. Tablo yoğun ise spreadsheet skill'e aktar.
3. Model kaynaklı ise BIM/CAD skill'iyle veri doğrula.
4. Taşıyıcı sistem ise açık kaynak motor rotası + uzman onayı notu ver.
