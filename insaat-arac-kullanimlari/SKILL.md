---
name: insaat-arac-kullanimlari
description: İnşaat operasyonunda PDF, Excel, CSV, CAD/DWG/DXF, IFC/BIM, görsel, klasör ve arşiv girdilerini incelemek, doğru açık kaynak araca yönlendirmek, kanıtlı veri çıkarmak ve sonraki inşaat skill'lerine temiz veri hazırlamak için kullanılır.
---

# İnşaat Araç Kullanımları

## Ne Zaman Kullanılır

- Kullanıcı inşaat dosyası, keşif, metraj, teklif, hakediş, teknik doküman, çizim, fotoğraf veya klasör verdiğinde.
- Girdi formatı karışık olduğunda ve önce hangi araçla işleneceğine karar verilmesi gerektiğinde.
- Başka bir skill çalışmadan önce kaynak belge, tablo, çizim veya görselden temiz veri çıkarılacağı zaman.
- Dosya dönüşümü, veri çıkarımı, kaynak/kanıt haritası veya okunabilir çıktı paketi gerektiğinde.

Bu skill proje yönetmez, fiyat kararı vermez, teknik onay imzalamaz. Sadece dosyayı işler, kanıtı çıkarır, kalite bayraklarını yazar ve işi uygun sonraki skill'e hazırlar.

## Girdi

- Dosya veya klasör yolu.
- Dosya türü biliniyorsa beklenen kullanım amacı.
- Varsa proje adı, tarih, revizyon, mahal, iş kalemi ve hedef çıktı.
- Kullanıcının izin verdiği araçlar veya kısıtlar.

## Hibrit Araç Stratejisi

Önce düşük maliyetli ve deterministik araçları kullan. Yetmezse daha güçlü ama daha pahalı veya daha bağımlı araca geç.

| Girdi | İlk tercih | İkinci tercih | Ne üretir |
|---|---|---|---|
| PDF / DOCX / PPTX / XLSX | MarkItDown | Docling, PyMuPDF, pdfplumber | Markdown, tablo, sayfa kanıtı |
| PDF tablo | pdfplumber | PyMuPDF, Docling | Metraj/teklif/hakediş tablosu |
| Taranmış PDF / görsel | Docling OCR | PyMuPDF render + OCR, OpenCV ön işleme | OCR metni, görsel kalite notu |
| CSV / Excel | pandas | openpyxl/xlwings | Normalize tablo |
| DXF | ezdxf | FreeCAD | Layer, block, ölçü, entity özeti |
| DWG | LibreDWG / FreeCAD dönüşümü | AutoCAD varsa kullanıcı onaylı dış araç | DXF'e dönüşüm, QA notu |
| IFC | IfcOpenShell | FreeCAD / Bonsai | Eleman, mahal, tip, metraj özeti |
| JPG / PNG / TIFF | OpenCV | Görsel model yorumu | Görsel kalite, kırpma, kanıt notu |
| ZIP / klasör | Güvenli envanter | Dosya türüne göre alt araç | Dosya haritası |

## İş Akışı

1. Dosya envanteri çıkar: ad, uzantı, boyut, hash, kategori, risk bayrağı.
2. Hassas veya tehlikeli içerik kontrolü yap: parola, makro, çalıştırılabilir dosya, arşiv içeriği, kişisel veri.
3. Dosyayı kategoriye ayır: belge, tablo, CAD, BIM, görsel, arşiv, bilinmeyen.
4. Araç rotası seç: hızlı çıkarım, hassas tablo çıkarımı, çizim okuma, model okuma veya görsel ön işleme.
5. Kaynak kanıtını koru: dosya adı, sayfa, sheet, satır, layer, entity, mahal veya görsel referansı.
6. Normalize çıktı üret: Markdown, JSON, CSV veya tablo.
7. Kalite bayraklarını yaz: okunamayan alan, belirsiz ölçü, eksik başlık, ölçek/birim şüphesi, OCR güveni.
8. Sonraki skill öner: metraj, teknik şartname, teklif, hakediş, risk, tasarım veya iletişim.

## Çıktı Formatı

Kısa işlerde Markdown tablo yeterlidir. Karmaşık işlerde şu bölümleri kullan:

```markdown
## Dosya Envanteri

## Araç Rotası

## Çıkarılan Veri

## Kanıt Haritası

## Kalite Bayrakları

## Eksik Veri / Sorular

## Sonraki Skill Önerisi
```

Makine tarafından kullanılacak çıktılarda `references/cikti-semalari.md` içindeki JSON şemalarını uygula.

## Kalite Kapısı

- Ölçek, birim, para birimi veya revizyon belirsizse açıkça bayrakla.
- DWG dönüşümünde tam doğruluk iddiası yapma; dönüşüm sonrası QA iste.
- OCR çıktısını kesin veri gibi kullanma; kritik sayılar için görsel veya kaynak kontrolü iste.
- Excel formül hücresinde görünen değer ile formül ayrımını koru.
- PDF tablosunda satır kayması, birleşik hücre veya bölünmüş tablo varsa belirt.
- Makro, script veya çalıştırılabilir dosyayı kullanıcı onayı olmadan çalıştırma.

## Onay Sınırı

- Sözleşme, ödeme, fiyat, iş güvenliği, resmi teknik uygunluk ve hukuki bağlayıcı kararlar insan onayı gerektirir.
- Ticari veya teknik açıdan kritik ölçü/miktar sadece tek OCR ya da tek dönüşüm sonucuna dayanarak kesinleştirilmez.

## Referanslar

- Açık kaynak araştırması: `references/acik-kaynak-arastirma.md`
- Hibrit iş akışı: `references/hibrit-is-akisi.md`
- Çıktı şemaları: `references/cikti-semalari.md`
- Kalite kapıları: `references/kalite-kapilari.md`

## Scriptler

- `scripts/inspect_construction_inputs.py`: dosya/klasör envanteri ve araç rotası önerisi üretir.
- `scripts/extract_document_skeleton.py`: PDF/Office için opsiyonel MarkItDown, Docling, PyMuPDF ve pdfplumber akış iskeleti.
- `scripts/extract_table_skeleton.py`: CSV/XLSX için opsiyonel pandas/openpyxl akış iskeleti.
