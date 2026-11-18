# Video kontrol listesi (eleştirmen ajanı — Sonnet'e ver)
Render sonrası `ffmpeg -vf "fps=16/<süre>,scale=200:356,tile=8x2"` ile kare ızgarası çıkar, ajana bu listeyle baktır:
1. **Kanca (ilk 1 sn):** ilk kare boş/siyah/bulanık değil; kanca yazısı 1 sn içinde okunuyor; konu tek bakışta anlaşılıyor.
2. **Yazı süresi:** her yazı/alt bant en az ~0,9 sn tam görünür; iki satırlık yazılar ~1,3 sn.
3. **Çakışma:** yazılar birbirine, sol üst "KABİNE HABER • CANLI" rozetine ve oyunun kendi büyük başlıklarına binmiyor; kenarlardan kesilmiyor (≥60 px pay).
4. **Güvenli alan:** üst 220, alt 480, sağ 230 px'e önemli yazı/CTA girmiyor.
5. **Yazı = görüntü:** her başlık o an ekranda görünen oynanışı anlatıyor; menü/yükleme ekranı yok.
6. **Dil:** EN videoda oyun içi Türkçe yazı yok (tersi de).
7. **Reklam kuralı (reklam videolarında):** bayrak, parti adı, "seçim/parti/oy" yok; CTA (ücretsiz + arama ifadesi) son 2,5 sn boyunca net.
8. **Kırmızı çizgiler:** gerçek siyasetçi/parti/slogan/güncel olay göndermesi yok.
Karar: "Yayına hazır" ya da kare numarasıyla somut düzeltme listesi.
