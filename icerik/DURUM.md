# Durum (8 Kasım 2026)

## Hesaplar
- Instagram @kabinegame: açıldı. Hesap türü İşletme seçildi → **İçerik üreticisi**ne geçilmesi önerildi (müzik kütüphanesi için).
- TikTok @kabinegame: açılıyor. YouTube kanalı "Kabine: Başkanlık Simülatörü" açıldı, Shorts telefondan yüklenecek (müzik için).
- Yabancı kanal: şimdilik ayrı hesap yok; en iyi giden videoların EN versiyonları hazırlanacak, oyun yayına çıkınca EN TikTok açılması önerildi (karar Umut'ta).
- Testçiler R10 üzerinden bulunacak; tanıtım videolarında test linki çağrısı yok. Test çağrısı karuseli, Google kapalı testi onaylayınca paylaşılacak.

## Paylaşılanlar
| Tarih | Platform | Video | Not |
|---|---|---|---|
| 19 Ekim 13:45 | Instagram | kabine_tanitim_v2_TR.mp4 ("Bir siyasetçinin bir haftası") | Lisanslı müzik; öne çıkarma (reklam) yapılmadı |
| 19 Ekim akşam | TikTok | aynı video | Umut yükleyecekti |
| 20 Ekim | YouTube Shorts | aynı video | telefondan, müzikli |

## Hazır, paylaşılmadı
- kabine_zurafa_v2_TR.mp4 (zürafa A/B, 13 sn) — açıklaması icerik/hafta1/aciklamalar ve takvimde.
- Test çağrısı karuseli (5 slayt TR/EN) — onay bekliyor.

## Sıradaki
1. Günde 1 video, aynı "KABİNE HABER" stilinde: prompter gafı, seçim gecesi, Muhabirden Kaç (dodge_0: 3 yakalanma → güneş gözlüğü → arabaya ulaştı), kriz kartları derlemesi (papağan, çeşme 4. açılış, anne araması), otobüs turu (simit/karanfil/saksı).
2. İlk videonun sonuçlarına göre (izlenme süresi, kaydetme, paylaşım) sıradaki konuyu seç.
3. Takvimi günlük plana göre güncelle; haftalık zamanlanmış görev (cumartesi 08:55) bu repoyu kullanacak şekilde güncellendi.

## 8 Kasım 2026 — App Store çıkışı, paylaşım Claude'da
- Oyun App Store'da (ücretsiz): https://apps.apple.com/tr/app/id6824178071 . Paylaşımı artık Claude, Umut'un Chrome'undan (Claude in Chrome) platformların kendi zamanlayıcılarıyla yapıyor (CLAUDE.md "Paylaşım").
- Zamanlananlar: 8 Kas 20:00 çıkış videosu (TikTok, YT, IG Reel) + IG hikâye 20:05; 9 Kas 20:00 prompter gafı (TikTok, YT, IG).
- YouTube kanalı doğrulandı, kanal profiline "App Store'da indir" linki eklendi.
- Hazır, Umut'a gönderildi: hikâye görseli + 4 öne çıkan kapağı (cikti/v2/story), App Store önizleme videosu 886x1920 18,7 sn (App Store Connect'e Umut yükleyecek).
- ASO önerileri (Umut'un onayı bekliyor): alt başlık "Komik Siyaset ve Seçim Oyunu"; anahtar kelimeler `başkan,belediye,politika,parti,miting,lider,ülke,strateji,piksel,kariyer,kriz,tycoon,yönetim`; tanıtım metni; puanlama penceresi (oyun kodu).
- Yapılacak: IG "Çıktı" öne çıkanı (hikâye yayına girince), Instagram profil linki (Umut, telefondan), haftanın kalan 5 videosu (Muhabirden Kaç, kriz kartları, otobüs/simit, seçim gecesi, zürafa tekrar değil).

## 10 Kasım 2026 — hafta 3 zamanlandı
- 6 video (rec/edit/make_hafta3.py, metinler icerik/hafta3/aciklamalar.md) TikTok, YouTube Shorts ve Instagram Reel'de 10–15 Kasım her gün 20:00'ye planlandı: dodge, kriz kartları, otobüs, seçim gecesi, 8 mini oyun, kedi A/B.
- IG kapak görseli: seçim, mini oyun ve kedi reel'lerinde özel kapak var; dodge, kart, otobüs reel'lerinde Instagram'ın önerdiği kare.
- Reklam rehberi: icerik/reklam/REHBER.md (öne çıkarmadan önce 3–5 gün organik bekle; siyaset temalı reklam reddi riski).
- Sıradaki: 16 Kasım haftası; ilk sonuçlara göre konu seçimi.

## 24 Kasım 2026 — Hafta 4 (dal: hafta4)
- 12 video hazır: `cikti/v2/hafta4/` — reklam a1/a2/a3 (EN+PT: Muhabirden Kaç, çöp grevi kartı, Kadrajda Kal), organik o1/o2/o3 (EN+TR: seçim gecesi son bölge, miting bilerek kötü zamanlama, skandal→Etiket Savaşı). Metinler `icerik/hafta4/aciklamalar.md`.
- Bağımsız değerlendirici turları sonrası düzeltmeler: reklam kapanışındaki arama satırı kaldırıldı (EN'de "President" geçiyordu); dodge ve miting kayıtları uydurma ülke + mor/turkuaz/turuncu bayrakla yeniden alındı (gerçek ABD/Brezilya bayrağı ve Ukrayna'ya benzeyen mavi-sarı kalabalık bayrakları çıktı); kanca kelime arası ≤0,06 sn; A2 sonundaki A/B rozetleri kaldırıldı; açıklamalarda 18 mini oyun.
- Kayıtlar rastgele: dodge ve miting zamanları (make_hafta4.py T) her yeni kayıtta marks.json/events.json'dan yeniden ölçülmeli (kare ≈ olay + 0,2–0,3 sn).
- Organik videolarda bilinçli olarak kapanış kartı yok (CTA açıklamada).
- 24 Kas 15:50 zamanlandı (TR): o1 25 Kas, o2 26 Kas, o3 27 Kas, hepsi 20:00 — Instagram (vidIQ, @kabinegame) + TikTok (Studio, özel kapak 1,2 sn karesi). YouTube Shorts YAPILMADI: yerleşik tarayıcıdaki Google hesabında yalnız Fix My Floor Plan kanalı var; Kabine kanalı Umut'un Chrome'unda (Claude in Chrome bağlı değildi).
- Yeni paylaşım yolu (Chrome yokken): videoyu `yayin` dalına koy (raw.githubusercontent) → vidiq_video_upload(url) → Instagram vidIQ taslak+publish(publishAt). TikTok'ta raw.github fetch engelli ama vidIQ'nun storage.googleapis imzalı URL'si fetch edilir: File → DataTransfer → input[type=file] + change; kapak aynı videodan canvas ile. Saat: `.tiktok-timepicker-left/right` öğelerine JS click (saat ve dakika ayrı açılışta).
- Sıradaki: YouTube'a 3 TR Shorts (Chrome bağlanınca); Brezilya Meta testi için reklam hesabı/bütçe onayı.
