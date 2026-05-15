# Metraj Karşılaştırma Kuralları

## Eşleştirme Sırası

1. Aynı mahal kodu + aynı kat.
2. Aynı mahal kodu.
3. Normalize mahal adı + aynı kat.
4. Fuzzy mahal adı + aynı kat.
5. Fuzzy mahal adı.

## Tolerans

- Alan: varsayılan `max(0.1 m2, %1)`.
- Hacim: varsayılan `max(0.05 m3, %1)`.
- Adet: varsayılan `0`.
- Tolerans kullanıcı/şartname tarafından verilirse o değer kullanılır.

## Sapma Tipleri

- `missing_in_source_a`
- `missing_in_source_b`
- `area_delta_over_tolerance`
- `volume_delta_over_tolerance`
- `count_delta`
- `level_mismatch`
- `name_mismatch`
- `low_confidence_match`
- `duplicate_key`

## Raporlama

- Mutlak fark ve yüzde fark birlikte verilir.
- Hangi ölçünün net/brüt olduğu ayrı kolon olarak yazılır.
- Eşleşme güveni düşükse sonuç kesin fark değil, kontrol adayıdır.
