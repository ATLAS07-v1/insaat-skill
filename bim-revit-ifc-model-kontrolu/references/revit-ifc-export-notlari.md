# Revit IFC Export Notları

## Temel Yaklaşım

Revit modeli doğrudan açık kaynak parse edilmeye çalışılmaz. Doğru yol:

1. Revit sürümünü belirle.
2. Autodesk `revit-ifc` eklentisinin güncel ve uygun sürümde olduğunu kontrol et.
3. Export ayarlarını kaydet.
4. IFC export al.
5. IFC'yi IfcOpenShell ile analiz et.
6. Görsel QA için Bonsai/FreeCAD/xeokit kullan.

## Export Öncesi Kontrol

- Shared coordinates / project base point / survey point.
- Room/space export ayarı.
- Property set export ayarı.
- Base quantities export ayarı.
- Linked model export ayarı.
- IFC schema seçimi: IFC2x3, IFC4, IFC4 Reference View, Design Transfer View.
- Phase/design option/workset görünürlüğü.
- Classification mapping.

## Revit Otomasyon

Kullanıcı ortamında Revit kuruluysa:

- `pyRevit`: hızlı Python/C#/VB.NET tool ve export otomasyonu.
- `RevitPythonShell`: IronPython ile interaktif Revit API kontrolü.
- Autodesk `revit-ifc`: IFC export davranışı ve kaynak kod referansı.

## Risk Dili

Kötü:

> RVT dosyası açık kaynakla okundu ve model kesin doğru.

Doğru:

> Revit kaynak model için IFC export rotası önerildi. IFC alındıktan sonra model hiyerarşisi, property setler, quantity setler, koordinat ve görsel QA ayrı doğrulanmalıdır.
