# Açık Kaynak Araştırması

SketchUp uygulaması kapalı kaynaklıdır. Bu skill, SketchUp ekosistemindeki açık kaynak resmi örnekleri, API yardımcılarını ve dönüşüm/test araçlarını referans alır; SKP üretiminin SketchUp lisansı ve API sınırları içinde yapılacağını varsayar.

## Ana Referanslar

| Kaynak | Rol | Skill'e Alınan İlke |
|---|---|---|
| https://ruby.sketchup.com/ | Resmi Ruby API dokümantasyonu | API yalnız SketchUp içinde çalışır; ana giriş `Sketchup.active_model`. |
| https://github.com/SketchUp/sketchup-ruby-api-tutorials | Resmi örnek extension ve tutorial repo'su | Ruby API ile group, command, menu, model işlemlerinde örnek tabanlı yaklaşım. |
| https://github.com/SketchUp/ruby-api-stubs | IDE autocomplete/stub | Kod yazarken SketchUp API görünürlüğü ve statik geliştirme kolaylığı. |
| https://github.com/SketchUp/sketchup-extension-vscode-project | Resmi VSCode extension template | RuboCop SketchUp, Solargraph, debug task ve proje iskeleti. |
| https://github.com/SketchUp/testup-2 | SketchUp içi test framework | Minitest tabanlı extension testleri ve CI benzeri kontrol. |
| https://github.com/SketchUp/sketchup-live-c-api | Live C API örnekleri | Açık SKP modeli veya importer/exporter senaryolarında C API sınırları. |
| https://github.com/SketchUp/ruby-c-extension-examples | Ruby C extension örnekleri | Performans/SDK gerektiren gelişmiş extension geliştirme. |
| https://github.com/openstudiocoalition/openstudio-sketchup-plugin | OpenStudio SketchUp plug-in | Enerji/analiz odaklı konsept geometri hattı. |
| https://github.com/YulioTech/SketchUp-glTF-Exporter-Ruby | Ruby glTF exporter | Web/3D paylaşım için GLB/glTF export örneği. |

## Hibrit Sonuç

1. Skill, doğrudan SketchUp yerine önce brief ve model organizasyonu üretir.
2. Ölçüler yeterliyse SketchUp Ruby API script'i üretir.
3. Geliştirme ortamı varsa resmi stubs, VSCode template ve TestUp önerilir.
4. SKP dışı formatlarda export kaybı ayrıca QA bayrağına alınır.
5. CAD/BIM girdileri karmaşıksa önce ilgili CAD/BIM skill'i ile temizlenir.

## Dikkat

- SketchUp Ruby API normal sistem Ruby'sinde çalışmaz.
- SketchUp Web Ruby API sunmaz; otomasyon için desktop SketchUp gerekir.
- `-RubyStartup` ile script başlatma pratikte kullanılır, ancak sürüm/yol/Unicode farkları nedeniyle her zaman doğrulanmalıdır.
- Ücretli/proprietary SketchUp ve eklenti lisansları teslim öncesi kontrol edilmelidir.
