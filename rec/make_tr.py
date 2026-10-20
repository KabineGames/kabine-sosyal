import sys, json
sys.path.insert(0, '.')
from build import build
OUT = str(__import__('pathlib').Path(__file__).resolve().parents[1] / 'cikti' / 'v1')
T, B = 240, 1190
reels = {}
reels['kabine_r1_tanitim_TR'] = (
 [dict(src='sess1_1.mp4', a=0.42, b=3.82, ov=[('hook', 0, None)], label='hook: zürafa kartı'),
  dict(src='sess1_1.mp4', a=3.82, b=5.9, ov=[('b', 0, None)], label='B seçildi'),
  dict(src='sess2.mp4', a=1.5, b=4.6, ov=[('rally', 0, None)], label='miting'),
  dict(src='sess2.mp4', a=4.6, b=6.2, ov=[('prompter', 0, None)], label='prompter dondu'),
  dict(src='sess2.mp4', a=7.45, b=8.75, ov=[('saved', 0, None)], label='kurtardı'),
  dict(src='sess2.mp4', a=18.56, b=21.1, ov=[('paper', 0.85, None)], label='gazete'),
  dict(src='sess3_1.mp4', a=0.6, b=3.8, ov=[('night', 0, None)], label='seçim gecesi'),
  dict(src='sess3_1.mp4', a=7.0, b=10.3, ov=[('win', 1.85, None)], label='kazandı'),
  dict(still='promo_tr.jpg', dur=1.8, ov=[('promo', 0, None)], label='terfi'),
  dict(card='end', dur=2.6, label='kapanış')],
 {'hook': dict(text='15 MİNİ OYUN\n1 SEÇİM GECESİ\n0 ZÜRAFA', y=T),
  'b': dict(text='ZÜRAFAYA\nHAYIR DEDİM', y=T),
  'rally': dict(text='MEYDANI\nCOŞTURDUM', y=T),
  'prompter': dict(text='SONRA PROMPTER\nDONDU', y=T, tcls='w'),
  'saved': dict(text='KURTARDIM', y=T),
  'paper': dict(text='MANŞET OLDUM', y=B),
  'night': dict(text='SEÇİM GECESİ', y=T, tcls='w'),
  'win': dict(text='%50,4 İLE\nKAZANDIM', y=T),
  'promo': dict(text='BELEDİYE\nBAŞKANI OLDUM', y=T),
  'end': dict(kind='end', line='0 ZÜRAFA. 1 MAKAM.', cta='ANDROID TESTİNE KATIL', note='Link profilde · @kabinegame')})
reels['kabine_r2_zurafa_TR'] = (
 [dict(src='sess1_0.mp4', a=0.42, b=3.74, ov=[('hook', 0, None)], label='hook'),
  dict(freeze='sess1_0.mp4', at=3.7, dur=2.4, ov=[('pick', 0, None), ('n3', 0, 0.8), ('n2', 0.8, 1.6), ('n1', 1.6, 2.4)], label='geri sayım'),
  dict(src='sess1_0.mp4', a=3.74, b=7.4, ov=[('a', 0, None)], label='A sonucu'),
  dict(src='sess1_1.mp4', a=3.82, b=7.5, ov=[('b', 0, None)], label='B sonucu'),
  dict(card='end', dur=2.6, label='kapanış')],
 {'hook': dict(text='2 ZÜRAFA MI,\n“OLMAZ” MI?', y=T),
  'pick': dict(tag='SEN SEÇ', text='A MI, B Mİ?', y=T, tcls='w'),
  'n3': dict(kind='big', text='3', y=470), 'n2': dict(kind='big', text='2', y=470), 'n1': dict(kind='big', text='1', y=470),
  'a': dict(tag='A', text='İKİ ZÜRAFA\nVAAT ET', y=T),
  'b': dict(tag='B', text='GERÇEKÇİ OL', y=T),
  'end': dict(kind='end', line='SEN HANGİSİNİ\nSEÇERDİN?', cta='YORUMA A YA DA B YAZ', note='@kabinegame')})
reels['kabine_r3_prompter_TR'] = (
 [dict(src='sess2.mp4', a=3.4, b=5.45, ov=[('hook', 0, None)], label='hook'),
  dict(freeze='sess2.mp4', at=5.45, dur=3.0, ov=[('q', 0, None), ('n3', 0, 1.0), ('n2', 1.0, 2.0), ('n1', 2.0, 3.0)], label='donma + geri sayım'),
  dict(src='sess2.mp4', a=5.45, b=8.9, label='çözüm'),
  dict(src='sess2.mp4', a=10.3, b=11.6, label='tekrar coşku'),
  dict(src='sess2.mp4', a=13.33, b=15.6, label='10/10'),
  dict(src='sess2.mp4', a=18.56, b=21.6, ov=[('paper', 0.85, None)], label='gazete'),
  dict(card='end', dur=2.6, label='kapanış')],
 {'hook': dict(text='PROMPTER DONDU.\n5 SANİYEN VAR.', y=T),
  'q': dict(tag='SIRAYI BUL', text='DOĞRU CÜMLE?', sub='İpucu: “asfaltı yedik!” değil', y=T, tcls='w'),
  'n3': dict(kind='big', text='3', y=560), 'n2': dict(kind='big', text='2', y=560), 'n1': dict(kind='big', text='1', y=560),
  'paper': dict(text='ERTESİ GÜN\nMANŞETTE', y=B),
  'end': dict(kind='end', line='SEN KAÇ SANİYEDE\nKURARDIN?', cta='SÜRENİ YORUMA YAZ', note='@kabinegame')})
reels['kabine_r4_secim_TR'] = (
 [dict(freeze='sess3_1.mp4', at=0.6, dur=1.3, ov=[('hook', 0, None)], label='ilk sandık'),
  dict(src='sess3_1.mp4', a=0.6, b=8.85, ov=[('hook', 0, 1.4), ('mid', 5.0, None)], label='sayım'),
  dict(src='sess3_1.mp4', a=8.85, b=11.6, ov=[('win', 0.2, None)], label='kazandı'),
  dict(still='promo_tr.jpg', dur=1.8, ov=[('promo', 0, None)], label='terfi'),
  dict(card='end', dur=2.8, label='kapanış')],
 {'hook': dict(text='İLK SANDIKTA %40.\nDAHA BİTMEDİ.', y=T),
  'mid': dict(text='SON MAHALLELER\nAÇILIYOR', y=T, tcls='w'),
  'win': dict(text='%50,4.\nKIL PAYI.', y=T),
  'promo': dict(text='YENİ MAKAM:\nBELEDİYE BAŞKANI', y=T, tcls='sm'),
  'end': dict(kind='end', line='SEÇİM GECESİ\nSENİ BEKLİYOR', cta='ANDROID’DE İLK\nOYNAYANLARDAN OL', note='Katılım linki profilde · @kabinegame')})
only = sys.argv[1:]
for name, (segs, cards) in reels.items():
    if only and not any(o in name for o in only): continue
    f, total, tl = build(name, segs, cards, OUT)
    print(name, round(total, 1), 's')
