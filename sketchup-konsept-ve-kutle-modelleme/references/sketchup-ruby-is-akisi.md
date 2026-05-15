# SketchUp Ruby İş Akışı

## Temel Kurallar

- `Sketchup` modülü yalnız SketchUp desktop içinde kullanılabilir.
- Model giriş noktası `Sketchup.active_model` olmalıdır.
- Değişiklikler `model.start_operation` ve `model.commit_operation` ile gruplanmalıdır.
- Ham geometri doğrudan ana entities içinde bırakılmamalı; group/component kullanılmalıdır.
- Her ana grup anlamlı ad, tag/layer ve material almalıdır.
- Ölçüler mümkünse metrik kabul edilmeli ve script içinde açık yazılmalıdır.

## Ruby Script Sırası

1. Modeli ve entities koleksiyonunu al.
2. Birim/rendering/template varsayımlarını yaz.
3. Tag/layer ve material setlerini oluştur.
4. Arsa düzlemi, yapı oturumu ve kat kütlelerini group olarak üret.
5. Giriş, pencere/cephe işaretleri ve çekme mesafesi gibi konsept elemanları ekle.
6. Page/scene listesi oluştur.
7. QA attribute veya rapor notu ekle.
8. Çıktı yolu verilmişse yeni dosyaya kaydet.

## Komut Notu

SketchUp desktop için pratik otomasyon komutu:

```powershell
"C:\Program Files\SketchUp\SketchUp 2024\SketchUp.exe" -RubyStartup "C:\path\to\script.rb"
```

Bu komut sürüm, lisans, işletim sistemi ve yol karakterlerine göre doğrulanmalıdır.
