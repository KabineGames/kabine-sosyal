# Kabine sosyal medya — çalışma talimatı

Bu repo, Umut'un mobil oyunu **Kabine: Başkanlık Simülatörü** (Instagram/TikTok/YouTube: @kabinegame) için sosyal medya videolarını ve metinlerini üreten araçları tutar. Paylaşımı Umut yapar; Claude hazırlar.

## Çalışma şekli
- Umut'la **Türkçe** konuş. Önemli kararlarda (hangi video önce, yaratıcı yön) kendi görüşünü söyle ve onun fikrini sor; küçük ayrıntılarda soru sorma.
- Umut gündüz şantiyede, sadece telefonu var: teslimatlar telefonda açılmalı (mp4, png, kısa kopyala-yapıştır metinler).
- `kabine-sosyal-medya` becerisi yüklüyse onun kırmızı çizgilerine uy. Özet: her şey kurgusal; gerçek siyasetçi, parti, slogan, renk eşleşmesi, güncel olay ya da onlara gönderme yok (örn. "otobüsten çay atma" kullanılmaz). Sahte yorum/sayı yok, bot yöntemi yok, hesaba giriş yok.
- Plan: günde 1 video. Müzik Umut tarafından platformda eklenir (trend ses); videolara sadece efekt sesleri gömülür. Hesap "İçerik üreticisi" türünde olmalı (İşletme hesabında ünlü müzikler kapanıyor).
- İçerik takvimi: https://claude.ai/artifact/5GgKG2i1p4ZYyMVfKuj7Pq (`posts` ve `setup` koleksiyonları; ArtifactData ile güncelle, yeni takvim açma).

## Kurulum (her yeni oturumda)
1. `bash tools/setup.sh`
2. Oyunu al: Artifact aracıyla `read` → https://claude.ai/artifact/WdwvebzHNYc8eboHZivxNi ; dönen tam HTML dosyasını `game/kabine.html` olarak kopyala. (Oyun kodu bu repoya commit edilmez.)
3. Ağ notu: npm ve fonts.googleapis.com bu ortamda kapalı olabilir; yazı tipleri git ile google/fonts deposundan gelir. Kayıt sırasında harness tüm dış istekleri engeller, yazı tiplerini yerelden verir.

## Kurgu hattı ("KABİNE HABER" stili)
- `rec/harness.py` — oyunu Playwright/Chromium'da 1080×1920 açar, CDP screencast ile kare kaydeder (kalp atışı animasyonu sayesinde durağan ekranlarda da kare akar). Bekleme için `time.sleep` değil `page.wait_for_timeout` kullan.
- `rec/setup_js.py` — yeni kariyer (Sabri Asfaltoğlu, Demlik Partisi, rakip Necmi Kaldırım). `KLANG=en` İngilizce.
- `rec/bots.py` — miting botu (mükemmel/ıska planı), prompter'ı zorla tetikleme.
- `rec/rec2.py [cards|rally|bus|dodge]` — kriz kartları, miting+gaf, otobüs turu, Muhabirden Kaç kayıtları → `rec/v2/<isim>/` (kareler + `marks.json` + `events.json` olay zamanları). `rec/sess3.py` seçim gecesi kayıtları.
- `rec/grab_sfx.py` — oyunun kendi ses efektlerini OfflineAudioContext ile `rec/sfx/*.wav` olarak çıkarır (repoda hazır).
- `rec/edit/engine.py` — kurgu motoru: shot listesi (zaman eğrisi, kamera zoom/pan, sarsıntı, flaş, renk, VHS geri sarma, kayan geçiş) + animasyonlu katmanlar (slam/pop/slide/drop) + ses miksajı → mp4.
- `rec/edit/gfx.py` + `gfx_specs.py` — alt bant (SON DAKİKA), gün etiketi, damga, logo kartları (Anton + Bungee + Pixelify). `python3 -I gfx_specs.py tr` ile `rec/edit/gfx/tr/` üretilir.
- `rec/edit/make_tanitim.py tr` ve `make_zurafa.py tr` — örnek kurgular (zaman kodları `tanitim_tr.json`). Çıktı `cikti/v2/`.
- `rec/edit/sheet.py <kaynak> <çıktı.png> <zamanlar…>` — kayıttan kesin zamanlı kareler (zoom noktası bulmak için).
- Kontrol: render sonrası ffmpeg ile kare şeridi çıkarıp bak; yazıların okunur kaldığından ve Instagram arayüzünün kapattığı alanlara (üst 220 px, alt 480 px, sağ 230 px) taşmadığından emin ol.

## Yerleşim kuralları
- Üst bant: sol üstte "KABİNE HABER • CANLI", sağ üstte gün etiketi (y≈262).
- Alt bant: kart sahnelerinde üstte (y≈548), miting/seçim sahnelerinde altta (y≈1345). Kart sahnelerinde kamera merkezi (540, 840) ve zoom ≤1.05 (kart yazıları kesilmesin).
- Her alt bant en az ~0,9 sn tam görünür kalmalı.

Durum ve yapılacaklar: `icerik/DURUM.md`.
