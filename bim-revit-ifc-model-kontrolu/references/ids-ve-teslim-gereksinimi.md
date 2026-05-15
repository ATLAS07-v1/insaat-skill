# IDS ve Teslim Gereksinimi

IDS, model tesliminde hangi elemanda hangi property/classification/quantity bilgisinin bulunması gerektiğini makine okunur şekilde ifade eder.

## Ne Zaman Kullanılır?

- Müşteri BIM teslim şartnamesi varsa.
- Model kalite kontrolü sadece "eleman var mı" değil, "gereken bilgi var mı" seviyesine çıkacaksa.
- Teslim öncesi IFC doğrulama raporu isteniyorsa.

## Araç

- IfcTester, IfcOpenShell ekosisteminde IDS dosyalarını okuyup IFC modelini doğrulamak için kullanılır.

## Basit Akış

1. IDS dosyası veya teslim gereksinimi alınır.
2. Gereksinimler entity/property/classification seviyesine ayrılır.
3. IFC model IfcTester ile doğrulanır.
4. Hatalar eleman GlobalId, sınıf, property ve gereksinim adıyla raporlanır.

## Çıktı

- Uyumlu eleman sayısı.
- Eksik property listesi.
- Yanlış değer listesi.
- Classification eksikleri.
- Teslim riski.
