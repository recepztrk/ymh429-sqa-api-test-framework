# YMH429 – Yazılım Kalite Güvencesi ve Testi | Proje Önerisi

YMH429 – Yazılım Kalite Güvencesi ve Testi

2025-2026 Güz Dönemi

Proje Önerisi

Teslim tarihi: 07/12/2025 (23:59)

## Proje Başlığı

E-Ticaret Sipariş ve Ödeme Servisleri için REST API Test Otomasyon Çatısı Geliştirilmesi

## Ekip Üyeleri

|  | Öğrenci Numarası | Adı- Soyadı |
| --- | --- | --- |
| 1 | 22290380 | Recep Öztürk |

## Projenin Amacı ve Kısa Açıklaması

Bu projenin amacı, basitleştirilmiş bir e-ticaret sipariş ve ödeme sistemi için tasarlanan REST tabanlı web servisleri üzerinde yeniden kullanılabilir bir API test otomasyon çatısı geliştirmek ve bu çatının etkinliğini incelemektir. Modern e-ticaret uygulamalarında ürün, stok, sipariş ve ödeme işlemlerinin büyük bölümü RESTful API’ler üzerinden yürütülmekte; bu servislerin sistematik olarak test edilmesi yazılım kalite güvencesi açısından kritik önem taşımaktadır.

Proje kapsamında ürün, sipariş, ödeme ve kullanıcı varlıklarını içeren örnek bir E-Ticaret Sipariş & Ödeme REST API’si tanımlanacak; bu API için stok ve sepet tutarı kuralları ile kimlik doğrulama ve yetkilendirme süreçlerini kapsayan fonksiyonel, negatif ve sınır değeri testleri otomatikleştirilecektir. Önerilen test otomasyon çatısı; ortak bir HTTP istemci katmanı, alan bazlı istemci modülleri ve veri odaklı test yapısı içerecek, geliştirilen test paketi uygun bir sürekli entegrasyon aracı ile bütünleştirilerek ders kapsamında “API / Servis Testi Otomasyonu” odak alanına yönelik uygulamalı bir çalışma sunacaktır.

## İlgili Çalışmalar (Literatür Taraması)

[1] A. Golmohammadi, M. Zhang, A. Arcuri, “Testing RESTful APIs: A Survey”

RESTful API testine yönelik çalışmaları derleyerek kara-kutu, model tabanlı, arama tabanlı ve sözleşme tabanlı yaklaşımları sınıflandırmakta; bu proje için genel kavramsal çerçeveyi sağlamaktadır.

[2] G. Martin-Lopez et al., “RESTest: Automated Black-Box Testing of RESTful Web APIs”

OpenAPI/Swagger tanımlarından yararlanarak REST API’ler için otomatik kara-kutu test senaryoları üreten bir araç önermekte; sözleşme tabanlı test tasarımının önemini vurgulamaktadır.

[3] E. Viglianisi et al., “RESTTESTGEN: Automated Black-box Testing of RESTful APIs”

Swagger arayüz tanımlarına dayalı olarak test istekleri ve oracle’lar üreten bir otomatik test aracı sunmakta; bizim çalışmamız ise benzer prensipleri manuel ve hafif bir test çatısında uygulamayı hedeflemektedir.

[4] D. Dimoski, N. Avresky, “Testing RESTful APIs – Use Case: RESTful API for Solving Multidimensional Time-Independent Schrödinger Equation”

Birden fazla REST API test aracını özellikleri ve kullanım kolaylığı açısından karşılaştırmakta; belirli senaryolar için alan-odaklı, kod tabanlı çözümlere duyulan ihtiyacı ortaya koymaktadır.

## Proje Görevleri

1. Literatür taraması ve problem analizi: RESTful API test otomasyonu ve e-ticaret sistemleri üzerine temel çalışmaların incelenerek proje kapsamının, test edilecek işlevlerin ve kalite özelliklerinin netleştirilmesi.
1. Alan modeli ve e-ticaret REST API tasarımı: Ürün, sipariş, ödeme ve kullanıcı varlıklarını içeren alan modelinin, iş kurallarının (stok, sepet tutarı, ödeme koşulları vb.) ve bu kuralları karşılayan REST endpoint’lerinin tanımlanması.
1. Örnek e-ticaret servisinin gerçekleştirilmesi veya seçilmesi: Tasarlanan modele uygun basitleştirilmiş bir sipariş ve ödeme API’sinin geliştirilmesi ya da mevcut bir örnek servisin seçilerek arayüz (OpenAPI/Swagger vb.) dokümantasyonunun çıkarılması.
1. Test otomasyon çatısının mimari tasarımı: Kullanılacak programlama dili ve test çerçevesinin (örn. Python + pytest) belirlenmesi; ortak HTTP istemci katmanı, alan bazlı istemci modülleri (auth, ürün, sipariş, ödeme) ve veri odaklı test yapısının mimarisinin oluşturulması.
1. Test senaryolarının tasarımı (fonksiyonel, negatif, sınır değeri): Kimlik doğrulama, ürün listeleme, stok kuralları, minimum/maksimum sepet tutarı ve ödeme akışlarını kapsayan fonksiyonel; hatalı/eksik girişleri ve yetkisiz erişimi kapsayan negatif; stok ve sepet tutarı eşiklerini hedefleyen sınır değeri testlerinin tanımlanması.
1. Test senaryolarının otomatikleştirilmesi ve çalıştırılması: Tasarlanan senaryoların seçilen test çatısı üzerinde otomatik testler olarak uygulanması, test verilerinin haricî dosyalardan okunması ve API cevapları üzerinde alan/tip kontrollerinin gerçekleştirilmesi.
1. Sürekli entegrasyon ve sonuçların değerlendirilmesi: Geliştirilen test paketinin bir sürekli entegrasyon aracı ile otomatik çalışacak şekilde yapılandırılması, elde edilen test sonuçlarının ve yakalanan hata senaryolarının analiz edilmesi, sistem mimarisi ve test otomasyon çatısının güçlü yönleri ile sınırlılıklarının raporlanması.
