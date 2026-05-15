# Araç Seçim Matrisi

| İhtiyaç | Önerilen Araç | Ne Zaman Kullanılır | Risk |
|---|---|---|---|
| Hızlı konsept brief'i | Skill metin akışı | Ölçü eksik veya müşteri fikri erken aşamada | Temsili model riski |
| Ölçülü kütle modeli | SketchUp Ruby API | Arsa/kat/yükseklik ölçüleri net | Script SketchUp içinde çalışmalı |
| Extension geliştirme | VSCode SketchUp template | Kalıcı araç/menü/komut geliştirilecekse | Setup süresi |
| API autocomplete | ruby-api-stubs + Solargraph | Ruby API kodu yazarken | Stub sürüm uyumu |
| Extension testleri | TestUp 2 | Uzun ömürlü extension kodu | SketchUp içi test gerektirir |
| SKP dışı export | SketchUp export / glTF exporter | GLB/gltf/OBJ/FBX gerekiyorsa | Material/scale kaybı |
| Enerji konsepti | OpenStudio SketchUp Plug-in | Enerji modeline gidecek basit geometri | Sürüm uyumu |
| CAD girdisi | CAD skill'i + SketchUp import | DWG/DXF temizliği gerektiğinde | Layer/ölçek karışması |
| Render | Blender skill'i | SketchUp modeli görselleştirilecekse | Export/import QA gerekir |

## Varsayılan Rota

1. Brief ve ölçü kontrolü.
2. SketchUp model organizasyonu.
3. Ruby API script'i veya manuel modelleme adımları.
4. Sahne/export planı.
5. QA bayrakları ve sonraki skill önerisi.
