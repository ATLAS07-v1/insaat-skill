# Dönüşüm ve PDF QA Kuralları

## Dönüşüm Öncesi

- Kaynak dosya yedeği alınır.
- Dosya kilitli mi kontrol edilir.
- Fontlar ve görseller erişilebilir mi kontrol edilir.
- İçindekiler ve çapraz referanslar güncel mi kontrol edilir.
- Kaynakta placeholder var mı kontrol edilir.

## Dönüşüm

- Markdown -> DOCX/PDF için Pandoc.
- DOCX/ODT/XLSX -> PDF için LibreOffice headless.
- Karmaşık DOCX için önce DOCX QA, sonra PDF export.
- PDF birleştirme/onarım için qpdf veya pypdf.

## Dönüşüm Sonrası QA

- Sayfa sayısı beklenen aralıkta mı?
- Başlıklar kesilmiş mi?
- Tablolar sayfadan taşıyor mu?
- Görseller bulanık veya kırpılmış mı?
- Header/footer ve sayfa numarası var mı?
- Kapak, içindekiler, revizyon tablosu, ekler ve onay sayfası doğru sırada mı?
- Linkler ve dosya referansları çalışıyor mu?

## Riskler

- DOCX -> PDF dönüşümünde font ve sayfa kırılması değişebilir.
- Markdown -> DOCX dönüşümünde karmaşık tablo ve resim hizası manuel QA gerektirebilir.
- PDF'den DOCX'e dönüşüm güvenilir yapısal belge üretmez; gerekiyorsa yeniden yapılandırma gerekir.
