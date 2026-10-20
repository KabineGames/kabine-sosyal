import sys
sys.path.insert(0, '.')
from build import build
OUT = str(__import__('pathlib').Path(__file__).resolve().parents[1] / 'cikti' / 'v1')
T, B = 240, 1190
LOGO = dict(logo='CABINET', sub='PRESIDENT SIMULATOR', logofont='barlow')
reels = {}
reels['kabine_r1_tanitim_EN'] = (
 [dict(src='sess1_1_en.mp4', a=0.42, b=3.76, ov=[('hook', 0, None)]),
  dict(src='sess1_1_en.mp4', a=3.76, b=5.9, ov=[('b', 0, None)]),
  dict(src='sess2_en.mp4', a=1.5, b=4.7, ov=[('rally', 0, None)]),
  dict(src='sess2_en.mp4', a=4.7, b=6.2, ov=[('prompter', 0, None)]),
  dict(src='sess2_en.mp4', a=7.5, b=8.75, ov=[('saved', 0, None)]),
  dict(src='sess2_en.mp4', a=18.47, b=21.0, ov=[('paper', 0.85, None)]),
  dict(src='sess3_0_en.mp4', a=0.62, b=3.8, ov=[('night', 0, None)]),
  dict(src='sess3_0_en.mp4', a=7.0, b=10.3, ov=[('win', 1.81, None)]),
  dict(still='promo_en.jpg', dur=1.8, ov=[('promo', 0, None)]),
  dict(card='end', dur=2.6)],
 {'hook': dict(text='15 MINI-GAMES\n1 ELECTION NIGHT\n0 GIRAFFES', y=T),
  'b': dict(text='I SAID NO\nTO GIRAFFES', y=T),
  'rally': dict(text='I FIRED UP\nTHE CROWD', y=T),
  'prompter': dict(text='THEN THE\nPROMPTER FROZE', y=T, tcls='w'),
  'saved': dict(text='SAVED IT', y=T),
  'paper': dict(text='FRONT PAGE', y=B),
  'night': dict(text='ELECTION NIGHT', y=T, tcls='w'),
  'win': dict(text='WON WITH\n50.4%', y=T),
  'promo': dict(text='NOW I’M\nTHE MAYOR', y=T),
  'end': dict(kind='end', line='0 GIRAFFES. 1 OFFICE.', cta='JOIN THE ANDROID TEST', note='Link in bio · @kabinegame', **LOGO)})
reels['kabine_r2_zurafa_EN'] = (
 [dict(src='sess1_0_en.mp4', a=0.42, b=3.74, ov=[('hook', 0, None)]),
  dict(freeze='sess1_0_en.mp4', at=3.7, dur=2.4, ov=[('pick', 0, None), ('n3', 0, 0.8), ('n2', 0.8, 1.6), ('n1', 1.6, 2.4)]),
  dict(src='sess1_0_en.mp4', a=3.76, b=7.4, ov=[('a', 0, None)]),
  dict(src='sess1_1_en.mp4', a=3.74, b=7.4, ov=[('b', 0, None)]),
  dict(card='end', dur=2.6)],
 {'hook': dict(text='2 GIRAFFES\nOR A HARD NO?', y=T),
  'pick': dict(tag='YOU PICK', text='A OR B?', y=T, tcls='w'),
  'n3': dict(kind='big', text='3', y=470), 'n2': dict(kind='big', text='2', y=470), 'n1': dict(kind='big', text='1', y=470),
  'a': dict(tag='A', text='PROMISE TWO\nGIRAFFES', y=T),
  'b': dict(tag='B', text='BE REALISTIC', y=T),
  'end': dict(kind='end', line='WHICH ONE\nWOULD YOU PICK?', cta='COMMENT A OR B', note='@kabinegame', **LOGO)})
reels['kabine_r3_prompter_EN'] = (
 [dict(src='sess2_en.mp4', a=3.4, b=5.45, ov=[('hook', 0, None)]),
  dict(freeze='sess2_en.mp4', at=5.45, dur=3.0, ov=[('q', 0, None), ('n3', 0, 1.0), ('n2', 1.0, 2.0), ('n1', 2.0, 3.0)]),
  dict(src='sess2_en.mp4', a=5.45, b=8.9),
  dict(src='sess2_en.mp4', a=9.7, b=11.0),
  dict(src='sess2_en.mp4', a=13.25, b=15.5),
  dict(src='sess2_en.mp4', a=18.47, b=21.5, ov=[('paper', 0.85, None)]),
  dict(card='end', dur=2.6)],
 {'hook': dict(text='PROMPTER FROZE.\n5 SECONDS LEFT.', y=T),
  'q': dict(tag='ORDER IT', text='WHAT’S THE LINE?', sub='Hint: not “we ate the asphalt!”', y=T, tcls='w'),
  'n3': dict(kind='big', text='3', y=560), 'n2': dict(kind='big', text='2', y=560), 'n1': dict(kind='big', text='1', y=560),
  'paper': dict(text='NEXT DAY:\nFRONT PAGE', y=B),
  'end': dict(kind='end', line='HOW FAST WOULD\nYOU SOLVE IT?', cta='COMMENT YOUR TIME', note='@kabinegame', **LOGO)})
reels['kabine_r4_secim_EN'] = (
 [dict(freeze='sess3_0_en.mp4', at=0.62, dur=1.3, ov=[('hook', 0, None)]),
  dict(src='sess3_0_en.mp4', a=0.62, b=8.81, ov=[('hook', 0, 1.4), ('mid', 5.0, None)]),
  dict(src='sess3_0_en.mp4', a=8.81, b=11.6, ov=[('win', 0.2, None)]),
  dict(still='promo_en.jpg', dur=1.8, ov=[('promo', 0, None)]),
  dict(card='end', dur=2.8)],
 {'hook': dict(text='33% AT THE FIRST BOX.\nNOT DONE YET.', y=T),
  'mid': dict(text='LAST DISTRICTS\nREPORTING', y=T, tcls='w'),
  'win': dict(text='50.4%.\nBY A HAIR.', y=T),
  'promo': dict(text='NEW OFFICE:\nMAYOR', y=T),
  'end': dict(kind='end', line='ELECTION NIGHT\nIS WAITING', cta='PLAY FIRST\nON ANDROID', note='Link in bio · @kabinegame', **LOGO)})
only = sys.argv[1:]
for name, (segs, cards) in reels.items():
    if only and not any(o in name for o in only): continue
    f, total, tl = build(name, segs, cards, OUT)
    print(name, round(total, 1), 's')
