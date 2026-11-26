# Brezilya (PT-BR) — durum ve sıradaki işler (26 Kasım 2026)

## Kanal
- YouTube: **Gabinete: Simulador Político** · @gabinetejogo · kanal ID `UCmgZd4PBjlv733HF0ohC4zg` (Kabine TR kanalıyla aynı Google hesabında; Claude, Chrome üzerinden yükler).
- Açıklama, link, anahtar kelimeler girildi. Kit: claude.ai projesindeki `claude/KABINE_BREZILYA_YT_KIT.md`.
- **Açık iş (Umut):** YouTube telefon doğrulaması (Studio → Ayarlar → Kanal → Özellik uygunluğu). Bu yapılmadan açıklamadaki App Store linki tıklanmıyor.
- TikTok BR yok (TR kayıtlı hesap Brezilya'ya ulaşmıyor); Instagram BR belki ileride.

## Planlanan Shorts (yayın saati TR 01:00 = Brezilya 19:00)
| Tarih | Video | Kaynak |
|---|---|---|
| 27 Kas | O papagaio da prefeitura sumiu… e agora? 🦜 | `make_br.py kart` |
| 28 Kas | Dá pra fugir da imprensa? 🕶️ | `make_br.py dodge` |
| 29 Kas | De zé-ninguém a Presidente em 15 segundos 🏆 (fragman A) | `make_br.py trA` |

Her Short: çocuklara özel değil, yapay zeka "Hayır", kategori Oyun, PT etiketler, açıklama şablonu kitte.

## Reklam videoları (Meta, Brezilya)
- `gabinete_br_reklam_A.mp4` (kanca "DE ZÉ-NINGUÉM A PRESIDENTE") ve `_B.mp4` ("VOCÊ DURARIA 1 SEMANA?"); Umut'un PC'sinde `Desktop/kabinegame-sosyalmedya/`.
- 15 sn, 128 BPM sentetik müzik (`music_synth.py`, telifsiz), AI anlatım yok. Üç bağımsız denetçi turundan geçti; A daha güçlü bulundu.
- Karar: "18 MINIJOGOS" kalıyor. **Meta testi Android çıkınca (1–2 hafta) başlar**, sadece iOS + Android hedefli, A ve B ayrı reklam setlerinde aynı bütçe. Ölçüt: 3 sn kalma ≥%25, tıklama ≥%0,8; kurulum maliyeti yön göstergesi.
- Reklam metnine "jogo de simulação totalmente fictício" yaz (siyasi reklam sınıfına düşmesin). Reddedilirse seçim sahnesiz kurgu çıkar.

## Üretim hattı (PT)
1. Oyunu derle: kabine repo `python3 game/build.py` → `game/dist/app/index.html` → buraya `game/kabine.html`, `fonts/` klasörünü de `game/fonts/` altına kopyala (harness artık yan dosyaları da servis ediyor).
2. Kayıt: `cd rec && KLANG=pt python3 rec2.py dodge cards rally bus` · mini oyunlar `KLANG=pt python3 sess5.py konvoy dinner tele rally ...` · seçim gecesi `KLANG=pt python3 sess3.py 1`.
3. Grafik: `cd rec/edit && python3 -I gfx_pt.py` · kurgu: `python3 make_br.py kart dodge trA trB` → `cikti/br/`.
4. Chrome dosya yükleme sınırı 3,8 MB → yüklemeden önce `crf 28–29` ile küçült, Umut'un klasörüne yazıp oradan yükle.
5. Her video: taze bağımsız denetçi (EVET/HAYIR + 5 sorun) → #1 düzelt → yeni denetçi.

## Sıradaki işler
1. 48 saat sonra 3 Short'un analizi (izlemeye devam oranı, kanca tipi karşılaştırması).
2. Haftalık BR paketi: tek anlık absürt Shorts (otobüs/vovó, miting gafı, konvoy, devlet yemeği). Bot rastgele oynuyor; zayıf mini oyunlar (pazar, delegeler) için akıllı bot ya da Umut'un telefon ekran kaydı.
3. Umut 6–7 mini oyunu telefonda iyi oynayıp ekran kaydı atarsa → fragmanın "büyük stüdyo" v2'si.
4. Android çıkınca: Meta A/B testi (yukarıdaki kurallarla), açıklama/kanal linkine Google Play eklenir.
5. 1.2 yayında olunca: App Store pt-BR önizleme videosu (886x1920, 15–30 sn, fiyat/"grátis" yazısı olmadan).
