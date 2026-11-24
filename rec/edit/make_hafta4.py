"""Hafta 4 videoları (3 reklam EN+PT, 3 organik EN+TR).
Kullanım: python3 make_hafta4.py <a1|a2|a3|o1|o2|o3> <en|pt|tr>   (reklamlar: en/pt, organikler: en/tr)
Kayıtlar: rec/rec4.py (KLANG=en|pt|tr) -> rec/v2/h4_*_<dil>/.  Çıktı: cikti/v2/hafta4/<id>_<dil>.mp4 (+ sheets/<id>_<dil>.png).
Reklamlarda ekranda seçim/oy/kampanya/parti/aday/miting/başkan kelimeleri yok; bayraklar kamera kadrajıyla dışarıda kalır.
Reklamlara oyunun chiptune altlığı (chiptune.py, 120 BPM) kısık gömülür; kesmeler ve yazı vuruşları 0,5 sn'lik vuruşlara oturur."""
import sys, pathlib, subprocess, shutil
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import numpy as np
from scipy.io import wavfile
import make_hafta3 as H3
from engine import render, W, H
import gfx, chiptune

ED = pathlib.Path(__file__).resolve().parent
REC = ED.parent
OUT = REC.parent / 'cikti' / 'v2' / 'hafta4'
SHEETS = OUT / 'sheets'
BPM, BEAT = 120, 0.5
TOP, BOT = 515, 1345
ADS = ('a1', 'a2', 'a3')

# ---------------------------------------------------------------- yazılar
STRIP = {'en': 'CABINET NEWS · @KABINEGAME', 'pt': 'CABINET NOTÍCIAS · @KABINEGAME', 'tr': 'KABİNE HABER · @KABINEGAME'}
BUG = {'en': ('CABINET NEWS', 'LIVE'), 'pt': ('CABINET NOTÍCIAS', 'AO VIVO'), 'tr': ('KABİNE HABER', 'CANLI')}
BRK = {'en': 'BREAKING', 'pt': 'URGENTE', 'tr': 'SON DAKİKA'}
NEXT = {'en': 'NEXT DAY', 'pt': 'NO DIA SEGUINTE', 'tr': 'ERTESİ GÜN'}
WHITE, GOLD, RED = '#ffffff', '#f5b83d', '#e43b34'

TEXT = {
    # A1 Muhabirden Kaç (reklam)
    'a1_hook': {'en': 'I RAN INTO THEM.', 'pt': 'CORRI PRA CIMA DELES.'},
    'a1_rep': {'en': '◀◀ REPLAY', 'pt': '◀◀ DE NOVO'},
    'a1_why': {'en': 'ON PURPOSE.', 'pt': 'DE PROPÓSITO.'},
    'a1_res': {'en': 'SAID “NO COMMENT”\nTO 3 CAMERAS', 'pt': 'TEMPESTADE DE\nMICROFONES'},
    'a1_take2': {'en': 'TAKE 2: ZERO CONTACT', 'pt': 'TENTATIVA 2: SEM ENCOSTAR'},
    'a1_q': {'en': 'YOUR TURN?', 'pt': 'SUA VEZ?'},
    # A2 çöp grevi (reklam)
    'a2_hook': {'en': 'CITY BURIED IN TRASH', 'pt': 'CIDADE AFOGADA NO LIXO'},
    'a2_ab': {'en': 'A OR B?', 'pt': 'A OU B?'},
    'a2_b': {'en': 'SEAGULLS MOVED\nINTO CITY HALL', 'pt': 'GAIVOTAS TOMARAM\nA PREFEITURA'},
    'a2_rew': {'en': '◀◀ WHAT IF A?', 'pt': '◀◀ E SE FOSSE A?'},
    'a2_a': {'en': 'STREETS SPARKLING,\nBUDGET TOOK A HIT', 'pt': 'RUAS BRILHANDO,\nO CAIXA SENTIU'},
    'a2_q': {'en': 'WHAT WOULD YOU PICK?', 'pt': 'O QUE VOCÊ ESCOLHERIA?'},
    # A3 Kadrajda Kal (reklam)
    'a3_hook': {'en': 'DON’T LEAVE THE PHOTO.', 'pt': 'NÃO SAI DA FOTO.'},
    'a3_out': {'en': 'OUT!', 'pt': 'FORA!'},
    'a3_res': {'en': 'BODYGUARD PULLED\nME OUT OF THE SHOT', 'pt': 'SÓ A MINHA ORELHA\nSAIU NA FOTO'},
    'a3_take2': {'en': 'TAKE 2: NOD ON CUE', 'pt': 'TENTATIVA 2: CONCORDA NA HORA'},
    'a3_nod': {'en': 'NOD! +8', 'pt': 'CONCORDOU! +8'},
    'a3_good': {'en': 'STAR OF THE\nEVENING NEWS', 'pt': 'ESTRELA DO\nJORNAL DA NOITE'},
    'a3_q': {'en': 'COULD YOU STAY IN?', 'pt': 'VOCÊ FICARIA NA FOTO?'},
    # O1 seçim gecesi
    'o1_hook': {'en': 'LAST REGION. DEAD TIE.', 'tr': 'SON BÖLGE. BAŞA BAŞ.'},
    'o1_rew': {'en': '◀◀ 6 HOURS\nEARLIER', 'tr': '◀◀ 6 SAAT\nÖNCE'},
    'o1_c1': {'en': 'EARLY LEAD', 'tr': 'ERKEN ÖNDEYİZ'},
    'o1_c2': {'en': 'THE GAP IS SHRINKING', 'tr': 'FARK ERİYOR'},
    'o1_lt1': {'en': 'TOO CLOSE\nTO CALL', 'tr': 'KİMSE\nKESTİREMİYOR'},
    'o1_left': {'en': '1 LEFT', 'tr': '1 KALDI'},
    'o1_lt2': {'en': 'BY A HAIR!\nNEW MAYOR', 'tr': 'KIL PAYI!\nYENİ BAŞKAN'},
    'o1_pct': {'en': '50.6%', 'tr': '%50,6'},
    'o1_q': {'en': 'COULD YOU WIN BY A HAIR?', 'tr': 'SEN KIL PAYI KAZANIR MIYDIN?'},
    # O2 miting
    'o2_hook': {'en': 'WORST TIMING. ON PURPOSE.', 'tr': 'EN KÖTÜ AN. BİLEREK.'},
    'o2_lt1': {'en': 'PROMPTER FROZE!\nPURE IMPROV', 'tr': 'PROMPTER DONDU!\nADAY DOĞAÇLAMADA'},
    'o2_res': {'en': 'RALLY SURVIVED.\nBARELY.', 'tr': 'MİTİNG BİTTİ.\nZAR ZOR.'},
    'o2_rew': {'en': '◀◀ TAKE 2', 'tr': '◀◀ 2. DENEME'},
    'o2_take2': {'en': 'NOW: PERFECT TIMING', 'tr': 'ŞİMDİ: TAM ZAMANINDA'},
    'o2_lt2': {'en': 'CROWD GOES\nWILD', 'tr': 'MEYDAN\nYIKILDI'},
    'o2_q': {'en': 'CAN YOU TIME IT?', 'tr': 'SEN ZAMANLAYABİLİR MİSİN?'},
    # O3 skandal zinciri
    'o3_hook': {'en': 'SCANDAL LEAKED. I FLIPPED IT.', 'tr': 'SKANDAL SIZDI. TERS ÇEVİRDİM.'},
    'o3_rew': {'en': '◀◀ 1 WEEK\nEARLIER', 'tr': '◀◀ 1 HAFTA\nÖNCE'},
    'o3_c1': {'en': 'AN INFLUENCER WANTS A COLLAB', 'tr': 'FENOMEN ORTAK VİDEO İSTİYOR'},
    'o3_lt1': {'en': 'OLD POSTS LEAKED.\nI’M IN THE VIDEO.', 'tr': 'ESKİ POSTLAR ÇIKTI.\nBEN DE VİDEODAYIM.'},
    'o3_c2': {'en': 'THEN THE TAPE LEAKED', 'tr': 'SONRA SES KAYDI SIZDI'},
    'o3_c3': {'en': 'COUNTERATTACK: TREND WAR', 'tr': 'KARŞI SALDIRI: ETİKET SAVAŞI'},
    'o3_win': {'en': 'TREND IS MINE', 'tr': 'GÜNDEM BENİM'},
    'o3_lt2': {'en': 'THE CONVERSATION\nMOVED ON', 'tr': 'GÜNDEM DEĞİŞTİ,\nSKANDAL SÖNÜYOR'},
    'o3_end': {'en': 'MADE BY 1 PERSON · 15 MINI-GAMES', 'tr': '1 KİŞİ YAPTI · 15 MİNİ OYUN'},
    # ortak
    'end_free': {'en': 'FREE ON IPHONE', 'pt': 'GRÁTIS NO IPHONE'},
}
# tür, ek ayarlar (yazı TEXT'ten)
KIND = {
    'a1_hook': ('cap', dict(size=112, color=WHITE)), 'a1_rep': ('rew', {}), 'a1_why': ('stamp', dict(size=150, color=GOLD)),
    'a1_res': ('lt', dict(tag=NEXT)), 'a1_take2': ('cap', dict(size=86, color=GOLD)), 'a1_q': ('tagl', dict(size=150)),
    'a2_hook': ('cap', dict(size=100, color=WHITE)), 'a2_ab': ('cap', dict(size=130, color=GOLD)), 'a2_b': ('lt', dict(tag=BRK)),
    'a2_rew': ('rew', {}), 'a2_a': ('lt', dict(tag=BRK)), 'a2_q': ('tagl', dict(size=96)),
    'a3_hook': ('cap', dict(size=112, color=WHITE)), 'a3_out': ('stamp', dict(size=230, color=RED)), 'a3_res': ('lt', dict(tag=NEXT)),
    'a3_take2': ('cap', dict(size=86, color=GOLD)), 'a3_good': ('lt', dict(tag=NEXT)), 'a3_nod': ('stamp', dict(size=130, color=GOLD)), 'a3_q': ('tagl', dict(size=104)),
    'o1_hook': ('cap', dict(size=104, color=WHITE)), 'o1_rew': ('rew', {}), 'o1_c1': ('cap', dict(size=110, color=GOLD)),
    'o1_c2': ('cap', dict(size=96, color=GOLD)), 'o1_lt1': ('lt', dict(tag='LIVE')), 'o1_left': ('stamp', dict(size=200, color=GOLD)),
    'o1_lt2': ('lt', dict(tag=BRK)), 'o1_pct': ('stamp', dict(size=230, color=GOLD)), 'o1_q': ('tagl', dict(size=84)),
    'o2_hook': ('cap', dict(size=100, color=WHITE)), 'o2_lt1': ('lt', dict(tag=BRK)), 'o2_res': ('lt', dict(tag=NEXT)), 'o2_rew': ('rew', {}),
    'o2_take2': ('cap', dict(size=96, color=GOLD)), 'o2_lt2': ('lt', dict(tag=BRK)), 'o2_q': ('tagl', dict(size=90)),
    'o3_hook': ('cap', dict(size=94, color=WHITE)), 'o3_rew': ('rew', {}), 'o3_c1': ('cap', dict(size=80, color=WHITE)),
    'o3_lt1': ('lt', dict(tag=BRK)), 'o3_c2': ('cap', dict(size=92, color=GOLD)), 'o3_c3': ('cap', dict(size=84, color=GOLD)),
    'o3_win': ('stamp', dict(size=150, color=GOLD)), 'o3_lt2': ('lt', dict(tag=BRK)), 'o3_end': ('cap', dict(size=72, color=GOLD)),
    'end_free': ('pill', {}),
}
TR_LIVE = {'tr': 'CANLI', 'en': 'LIVE', 'pt': 'AO VIVO'}


def specs(lang):
    sp = {'bug': ('bug', dict(name=BUG[lang][0], live=BUG[lang][1])),
          'end_bg': ('endbg', {}), 'end_icon': ('icon', {}), 'end_handle': ('handle', dict(text='@kabinegame')),
          'end_logo': ('logo', dict(text='KABİNE') if lang == 'tr' else dict(text='CABINET', latin=True)),
          'b_a': ('badge', dict(text='A')), 'b_b': ('badge', dict(text='B')), 'b_c': ('badge', dict(text='C')),
          's_4': ('stamp', dict(text='4/10' if lang == 'en' else '3/10', size=200, color=RED)),
          's_10': ('stamp', dict(text='10/10', size=200, color=GOLD)), 's_9': ('stamp', dict(text='9/10', size=200, color=GOLD)),
          's_q': ('stamp', dict(text='?!', size=260, color=GOLD))}
    for k, d in TEXT.items():
        if lang not in d: continue
        kind, kw = KIND[k]; kw = dict(kw); t = d[lang]
        if kind == 'lt':
            tag = kw.pop('tag'); tag = tag[lang] if isinstance(tag, dict) else ({'LIVE': TR_LIVE[lang]}.get(tag, tag))
            sp[k] = ('lt', dict(tag=tag, head=t, strip=STRIP[lang]))
        elif kind == 'tagl':
            sp[k] = ('tagl', dict(text=t)); sp[k + '_sz'] = kw.get('size')
        else:
            kw['text'] = t; sp[k] = (kind, kw)
    return {k: v for k, v in sp.items() if not k.endswith('_sz')}


# ---------------------------------------------------------------- yardımcılar
def V(n, lang): return str(REC / 'v2' / f'h4_{n}_{lang}')
def g(n): return H3.g(n)
def size(n): return H3.size(n)
def lt(n, u0, u1, y=TOP, sc=0.88): return H3.lt(n, u0, u1, y, sc)
def lt_cover(n, u1, y=1195, sc=0.88):
    """Sonuç ekranında çip satırını (bar adları) ilk kareden örten sabit alt bant."""
    d = H3.lt(n, 0.0, u1, y, sc); d['anim'] = 'none'
    return [dict(img=g('topband'), u0=0.0, u1=u1, x=W / 2, y=122, anim='none', out='cut'), d]
# alt yarıda (y>900) yazılar sağdaki 230 px'lik platform düğmelerinden uzak durur: LX merkez, en fazla LW genişlik
LX, LW = 455, 790
def cap(n, u0, u1, y=430, rot=-2, sc=1.0, x=W / 2, maxw=960): d = H3.cap(n, u0, u1, y, rot); d['scale'] = min(sc, maxw / size(n)[0]); d['x'] = x; return d
def words(n, u0, u1, y=430, rot=-2, step=0.09, x=W / 2, maxw=960):
    return dict(img=g(n), u0=u0, u1=u1, x=x, y=y, anim='words', step=step, rot=rot, scale=min(1.0, maxw / size(n)[0]))
def stamp(n, u0, u1, x=W / 2, y=640, rot=-6, sc=1.0, maxw=940): return H3.stamp(n, u0, u1, x, y, rot, min(sc, maxw / size(n)[0]))
def rew(n, u0, u1, y=430, x=W / 2, maxw=940): return dict(img=g(n), u0=u0, u1=u1, x=x, y=y, anim='pop', out='cut', scale=min(1.0, maxw / size(n)[0]))
def badge(n, u0, u1, y, anim='pop', sc=0.6): return dict(img=g(n), u0=u0, u1=u1, x=780, y=y, anim=anim, out='cut', rot=-8, scale=sc)
def question(n, u0, u1, y=430, x=W / 2, maxw=940): return dict(img=g(n), u0=u0, u1=u1, x=x, y=y, anim='slam', out='cut', scale=min(1.0, maxw / size(n)[0]))


def thru(a, b, d=0.22, x=W / 2, y=H / 2):
    """Kesmesiz içinden geçiş: a sonunda hedefe dalar, b içeriden açılır."""
    a['zoom_out'] = (d, x, y); b['zoom_in'] = d


def ad_end(lang, dur=1.8):
    cx = W / 2
    ov = [dict(img=g('end_icon'), u0=0.0, u1=9, x=cx, y=560, anim='drop', scale=0.5),
          dict(img=g('end_logo'), u0=0.0, u1=9, x=cx, y=830, anim='slam', scale=0.78),
          dict(img=g('end_free'), u0=0.5, u1=9, x=cx, y=1040, anim='pop', rot=-3, pulse=True, scale=min(1.25, 900 / size('end_free')[0])),
          dict(img=g('end_handle'), u0=0.5, u1=9, x=cx, y=1180, anim='fade')]
    return dict(card=g('end_bg'), dur=dur, ov=ov, fx=[('flash', 0.0, 0.1, 0.5)],
                sfx=[('impact', 0.0, 0.7), ('sting', 0.02, 0.5), ('pop2', 0.5, 0.6), ('ding', 0.52, 0.4)])


GAME_CAM = (1.5, 540, 1030)    # Kadrajda Kal: köşe bayrakları kadraj dışında
RES_CAM = (1.0, 540, 960)      # sonuç ekranı tam kadraj; üstteki sahne bayrağını 'topband' (haber bandı) örter


# ---------------------------------------------------------------- A1: Muhabirden Kaç (reklam)
def a1(lang):
    # zamanlar kayıttaki karelerden ölçüldü (olay günlüğü kareden ~0,3 sn önde)
    T = {'en': dict(hit=9.78, hit_y=640, res=25.7, car=41.25, shades=40.9),
         'pt': dict(hit=8.15, hit_y=1081, res=25.8, car=36.75, shades=36.55)}[lang]
    s = V('dodge', lang); h = T['hit']; sh = []
    sh.append(dict(src=s, dur=2.0, time=[(0, h - 1.0), (1.0, h), (1.05, h + 0.06), (2.0, h + 0.13)],
        cam=[(0, 1.2, 540, T['hit_y'] + 300), (1.0, 1.45, 540, T['hit_y']), (2.0, 1.48, 540, T['hit_y'])],
        fx=[('flash', 1.0, 0.12, 0.8), ('shake', 1.0, 26, 0.45), ('chroma', 1.0, 1.3, 5)],
        ov=[words('a1_hook', 0.0, 2.0, step=0.08)],
        sfx=[('tap', 0.2, 0.5), ('tap', 0.5, 0.5), ('tap', 0.8, 0.5), ('camera', 1.0), ('camera', 1.1), ('error', 1.02, 0.7), ('impact', 1.0, 0.8)]))
    sh.append(dict(src=s, dur=2.5, time=[(0, h - 0.48), (2.5, h + 0.32)],
        cam=[(0, 1.5, 540, T['hit_y']), (2.5, 1.55, 540, T['hit_y'])],
        fx=[('vhs', 0.0, 0.3, 0.8), ('flash', 1.5, 0.12, 0.7), ('shake', 1.5, 20, 0.35)],
        ov=[rew('a1_rep', 0.0, 1.5), stamp('a1_why', 1.5, 2.5, y=430, rot=-5, sc=0.9)],
        sfx=[('rewind', 0.0, 0.6), ('camera', 1.5), ('error', 1.52, 0.6), ('trombone', 1.6, 0.5)]))
    sh.append(dict(src=s, dur=3.0, time=[(0, T['res']), (3.0, T['res'] + 2.8)], cam=[(0, *RES_CAM), (3.0, *RES_CAM)],
        fx=[('flash', 0.0, 0.1, 0.4)], ov=lt_cover('a1_res', 3.0),
        sfx=[('boo', 0.0, 0.5), ('impact', 0.02, 0.6), ('paper', 0.5, 0.6)]))
    c = T['car']
    sh.append(dict(src=s, dur=4.5, time=[(0, c - 4.0), (4.5, c + 0.5)], cam=[(0, 1.12, 540, 1000), (3.5, 1.14, 540, 900), (4.5, 1.2, 540, 700)],
        fx=[('flash', 0.0, 0.1, 0.4), ('punch', T['shades'] - c + 4.0, 0.06, 0.25), ('flash', 4.0, 0.12, 0.6)],
        ov=[cap('a1_take2', 0.0, 2.0, y=430, sc=0.95)],
        sfx=[('swoosh', 0.0, 0.5)] + [('tap', x, 0.35) for x in (0.6, 1.4, 2.2, 2.9)] + [('perfect', T['shades'] - c + 4.0, 0.7), ('win', 4.0), ('cheer', 4.05, 0.6)]))
    sh.append(dict(src=s, dur=1.5, time=[(0, c + 0.5), (1.5, c + 0.75)], cam=[(0, 1.2, 540, 700), (1.5, 1.24, 540, 690)],
        ov=[question('a1_q', 0.0, 1.5)], sfx=[('pop2', 0.0, 0.6), ('applause', 0.0, 0.5)]))
    thru(sh[0], sh[1], 0.2, 540, T['hit_y']); thru(sh[2], sh[3], 0.22); thru(sh[3], sh[4], 0.15, 540, 700)
    sh.append(ad_end(lang))
    return sh


# ---------------------------------------------------------------- A2: çöp grevi kartı (reklam)
def a2(lang):
    T = {'en': dict(clickB=3.21, clickA=3.20), 'pt': dict(clickB=3.45, clickA=3.28)}[lang]
    sB, sA = V('strike', lang), V('strikeA', lang); cb, ca = T['clickB'], T['clickA']; sh = []
    CAM = [(0, 1.0, 540, 840), (1, 1.03, 540, 850)]
    pill = dict(img=g('brk'), u0=0.0, u1=3.0, x=W / 2, y=330, anim='slam', out='cut', rot=-2, scale=0.9)
    sh.append(dict(src=sB, dur=3.0, time=[(0, cb - 2.4), (3.0, cb - 0.9)], cam=[(0, 1.0, 540, 840), (3.0, 1.03, 540, 850)],
        fx=[('flash', 0.0, 0.1, 0.5), ('tint', 0.0, 0.5, (40, 40, 200), 0.12)],
        ov=[pill, words('a2_hook', 0.05, 3.0, y=455, step=0.09)],
        sfx=[('impact', 0.0, 0.8), ('sting', 0.02, 0.5), ('swoosh', 0.5, 0.4)]))
    sh.append(dict(src=sB, dur=2.5, time=[(0, cb - 0.9), (2.5, cb)], cam=[(0, 1.03, 540, 850), (2.5, 1.05, 540, 860)],
        fx=[('punch', 2.45, 0.04, 0.2)],
        ov=[cap('a2_ab', 0.0, 2.5, y=430, rot=-3), badge('b_a', 0.5, 2.5, 1150), badge('b_b', 1.0, 2.5, 1290)],
        sfx=[('pop2', 0.0, 0.5), ('tick', 0.5), ('tick', 1.0), ('tick', 1.5), ('tick', 2.0), ('select', 2.45)]))
    sh.append(dict(src=sB, dur=3.5, time=[(0, cb), (3.5, cb + 3.6)], cam=[(0, 1.05, 540, 860), (3.5, 1.0, 540, 840)],
        fx=[('flash', 0.0, 0.12, 0.6), ('shake', 0.0, 14, 0.3)],
        ov=[stamp('b_b', 0.0, 0.5, x=W - 150, y=1290, rot=-8, sc=0.8), lt('a2_b', 0.5, 3.5, TOP)],
        sfx=[('impact', 0.0, 0.7), ('ding', 0.5, 0.5), ('trombone', 0.6, 0.6), ('boo', 1.0, 0.3)]))
    sh.append(dict(src=sA, dur=3.0, time=[(0, ca - 0.5), (1.0, ca), (3.0, ca + 2.6)], cam=[(0, 1.0, 540, 840), (3.0, 1.03, 540, 850)],
        fx=[('vhs', 0.0, 0.35, 0.9), ('flash', 1.0, 0.1, 0.5)],
        ov=[rew('a2_rew', 0.0, 1.0, y=430), stamp('b_a', 1.0, 1.5, x=W - 150, y=1150, rot=-8, sc=0.8), lt('a2_a', 1.5, 3.0, TOP)],
        sfx=[('rewind', 0.0, 0.6), ('select', 1.0), ('ding', 1.5, 0.5), ('applause', 1.6, 0.5), ('coin', 1.8, 0.5)]))
    sh.append(dict(src=sB, dur=2.0, time=[(0, cb + 3.6), (2.0, cb + 4.1)], cam=[(0, 1.0, 540, 840), (2.0, 1.02, 540, 845)],
        ov=[question('a2_q', 0.0, 2.0), badge('b_a', 0.5, 2.0, 1150, sc=0.5), badge('b_b', 0.5, 2.0, 1290, sc=0.5)],
        sfx=[('pop2', 0.0, 0.6), ('pop2', 0.5, 0.4)]))
    thru(sh[0], sh[1], 0.15, 540, 1200); thru(sh[3], sh[4], 0.15, 540, 900)
    sh.append(ad_end(lang))
    return sh


# ---------------------------------------------------------------- A3: Kadrajda Kal (reklam)
def a3(lang):
    T = {'en': dict(sec=9.15, res1=23.5, n1=31.9, nods=(1.1, 4.0), res2=49.6, n2=44.1, nod2=1.3),
         'pt': dict(sec=9.27, res1=23.6, n1=31.75, nods=(1.6, 4.05), res2=49.6, n2=44.9, nod2=1.3)}[lang]
    s = V('frame', lang); sh = []; z, x, y = GAME_CAM
    t0 = T['sec'] - 3.5
    sh.append(dict(src=s, dur=4.5, time=[(0, t0), (4.5, t0 + 4.5)], cam=[(0, z, x, y), (4.5, z + 0.05, x, y)],
        fx=[('flash', 1.1, 0.08, 0.4), ('shake', 1.1, 12, 0.25), ('flash', 3.5, 0.12, 0.8), ('shake', 3.5, 26, 0.45)],
        ov=[words('a3_hook', 0.0, 2.5, y=430, step=0.08), stamp('a3_out', 3.5, 4.5, y=560, rot=-8, sc=0.8)],
        sfx=[('drum', 0.5, 0.5), ('thud', 1.1, 0.8), ('error', 3.5, 0.7), ('impact', 3.5, 0.8), ('trombone', 3.6, 0.5)]))
    sh.append(dict(src=s, dur=2.5, time=[(0, T['res1']), (2.5, T['res1'] + 2.3)], cam=[(0, *RES_CAM), (2.5, *RES_CAM)],
        fx=[('flash', 0.0, 0.1, 0.4)], ov=lt_cover('a3_res', 2.5),
        sfx=[('boo', 0.0, 0.5), ('paper', 0.4, 0.6)]))
    n1 = T['n1']
    sh.append(dict(src=s, dur=5.0, time=[(0, n1), (5.0, n1 + 5.0)], cam=[(0, z, x, y), (5.0, z + 0.04, x, y)],
        fx=[('flash', 0.0, 0.1, 0.4)] + [('punch', u, 0.04, 0.2) for u in T['nods']],
        ov=[cap('a3_take2', 0.0, 2.0, y=430, sc=0.95)] + [stamp('a3_nod', u, u + 0.9, x=W / 2, y=700, rot=-6, sc=0.75) for u in T['nods']],
        sfx=[('swoosh', 0.0, 0.5)] + [x for u in T['nods'] for x in (('drum', u - 0.5, 0.4), ('good', u, 0.7))]))
    sh.append(dict(src=s, dur=2.0, time=[(0, T['res2']), (2.0, T['res2'] + 1.8)], cam=[(0, *RES_CAM), (2.0, *RES_CAM)],
        fx=[('flash', 0.0, 0.12, 0.6)], ov=lt_cover('a3_good', 2.0),
        sfx=[('win', 0.0), ('cheer', 0.05, 0.6)]))
    n2 = T['n2']
    sh.append(dict(src=s, dur=2.5, time=[(0, n2), (2.5, n2 + 2.5)], cam=[(0, z, x, y), (2.5, z + 0.03, x, y)],
        ov=[question('a3_q', 0.0, 2.5), stamp('a3_nod', T['nod2'], 2.5, x=W / 2, y=700, rot=-6, sc=0.75)],
        sfx=[('pop2', 0.0, 0.6), ('drum', T['nod2'] - 0.5, 0.4), ('good', T['nod2'], 0.6)]))
    thru(sh[0], sh[1], 0.2, 540, 1000); thru(sh[1], sh[2], 0.2); thru(sh[2], sh[3], 0.2, 540, 1000); thru(sh[3], sh[4], 0.2)
    sh.append(ad_end(lang))
    return sh


# ---------------------------------------------------------------- O1: seçim gecesi (organik)
def o1(lang):
    T = {'en': dict(left=6.95, last=7.8, verdict=8.95), 'tr': dict(left=7.0, last=8.05, verdict=9.1)}[lang]  # karelerden ölçüldü
    s = V('night', lang); sh = []; L, Lt, Vd = T['left'], T['last'], T['verdict']
    CAM = (1.0, 540, 960); Y = 1340   # yazılar yorum kutusunun üstünde: harita, yüzdeler ve çubuk açık kalır
    sh.append(dict(src=s, dur=3.5, time=[(0, L + 0.05), (3.5, L + 0.6)], cam=[(0, *CAM), (3.5, 1.05, 540, 900)],
        fx=[('flash', 0.0, 0.1, 0.4)], ov=[words('o1_hook', 0.0, 3.5, y=Y, step=0.1, rot=-1, x=LX, maxw=LW)],
        sfx=[('heart', 0.2, 0.9), ('heart', 0.7, 0.9), ('heart', 1.4, 1.0), ('heart', 1.9, 1.0), ('heart', 2.6, 1.0), ('heart', 3.1, 1.0)]))
    sh.append(dict(src=s, dur=1.2, time=[(0, L + 0.6), (1.2, 0.45)], cam=[(0, 1.05, 540, 900), (1.2, *CAM)],
        fx=[('vhs', 0.0, 1.2, 0.9)], ov=[rew('o1_rew', 0.0, 1.2, y=Y, x=LX, maxw=LW)], sfx=[('rewind', 0.0, 0.8), ('rewind', 0.55, 0.6)]))
    sh.append(dict(src=s, dur=3.5, time=[(0, 0.45), (3.5, 2.2)], cam=[(0, *CAM), (3.5, 1.03, 540, 940)],
        fx=[('flash', 0.0, 0.1, 0.4)], ov=[cap('o1_c1', 0.3, 3.5, y=Y, rot=-1, x=LX, maxw=LW)], sfx=[('tick', x, 0.5) for x in (0.3, 0.9, 1.5, 2.1, 2.7, 3.3)]))
    sh.append(dict(src=s, dur=3.0, time=[(0, 2.2), (3.0, 4.6)], cam=[(0, 1.03, 540, 940), (3.0, 1.05, 540, 930)],
        ov=[cap('o1_c2', 0.2, 3.0, y=Y, rot=-1, x=LX, maxw=LW)], sfx=[('tick', x, 0.5) for x in (0.2, 0.8, 1.4, 2.0)] + [('heart', 2.5, 0.8)]))
    sh.append(dict(src=s, dur=3.0, time=[(0, 4.6), (3.0, L)], cam=[(0, 1.05, 540, 930), (3.0, 1.06, 540, 920)],
        fx=[('tint', 0.0, 3.0, (40, 40, 200), 0.08)], ov=[lt('o1_lt1', 0.3, 3.0, y=1295, sc=0.72)],
        sfx=[('heart', x, 0.9) for x in (0.4, 0.9, 1.4, 1.9, 2.4)]))
    sh.append(dict(src=s, dur=4.5, time=[(0, L), (4.5, Lt - 0.02)], cam=[(0, 1.06, 540, 920), (4.5, 1.14, 540, 860)],
        fx=[('chroma', 3.8, 4.5, 4)], ov=[stamp('o1_left', 0.3, 4.5, x=LX, y=Y, rot=-4, sc=0.75, maxw=LW)],
        sfx=[('heart', x, 1.0) for x in (0.3, 0.95, 1.55, 2.1, 2.6, 3.05, 3.45, 3.8, 4.1, 4.35)]))
    vu = round((Vd - Lt) / 0.62, 2)
    sh.append(dict(src=s, dur=3.5, time=[(0, Lt), (3.5, Lt + 3.5 * 0.62)], cam=[(0, 1.14, 540, 860), (vu, *CAM), (3.5, *CAM)],
        fx=[('flash', 0.0, 0.12, 0.6), ('shake', vu, 24, 0.4), ('flash', vu, 0.14, 0.9)],
        ov=[stamp('o1_pct', vu, 3.5, x=LX, y=Y, sc=0.75, maxw=LW), lt('o1_lt2', vu + 0.35, 3.5, y=560)],
        sfx=[('impact', 0.0, 0.6), ('heart', 0.5, 1.0), ('win', vu), ('impact', vu + 0.02, 0.8), ('cheer', vu + 0.1, 0.9), ('fanfare', vu + 0.2, 0.6)]))
    t1 = Lt + 3.5 * 0.62
    sh.append(dict(src=s, dur=3.0, time=[(0, t1), (3.0, t1 + 2.4)], cam=[(0, *CAM), (3.0, *CAM)],
        ov=[question('o1_q', 0.0, 3.0, y=Y, x=LX, maxw=LW)], sfx=[('applause', 0.0, 0.6), ('pop2', 0.0, 0.5)]))
    thru(sh[0], sh[1], 0.15, 540, 400)
    return sh


# ---------------------------------------------------------------- O2: miting (organik)
def o2(lang):
    T = {'en': dict(gaffe=5.2, prompter=9.35, gaffe2=12.7, res1=17.6, h1=26.6, res2=33.4),
         'tr': dict(gaffe=5.2, prompter=8.1, gaffe2=11.35, res1=16.0, h1=25.25, res2=31.8)}[lang]
    s = V('rally', lang); sh = []; gf = T['gaffe']
    RC, TY = (1.04, 540, 1000), 375   # yazılar sahnenin boş üst gökyüzünde (pankart/kalabalık açık kalır)
    sh.append(dict(src=s, dur=4.0, time=[(0, gf - 2.0), (2.0, gf), (2.15, gf + 0.08), (4.0, gf + 1.0)], cam=[(0, *RC), (4.0, 1.07, 540, 990)],
        fx=[('flash', 2.0, 0.12, 0.8), ('shake', 2.0, 26, 0.45), ('punch', 2.0, 0.06, 0.3), ('tint', 2.0, 3.0, (40, 40, 200), 0.15)],
        ov=[words('o2_hook', 0.0, 2.6, y=TY, step=0.1), stamp('s_q', 2.6, 4.0, x=W - 200, y=720, rot=10, sc=0.6)],
        sfx=[('drum', 0.5, 0.5), ('drum', 1.0, 0.5), ('drum', 1.5, 0.5), ('gaffe', 2.0), ('impact', 2.02, 0.7), ('boo', 2.2, 0.6)]))
    p = T['prompter']
    sh.append(dict(src=s, dur=4.5, time=[(0, p - 0.3), (4.5, T['gaffe2'] + 0.8)], cam=[(0, 1.07, 540, 990), (4.5, *RC)],
        fx=[('flash', 0.3, 0.1, 0.5), ('shake', T['gaffe2'] - p + 0.3, 20, 0.35)],
        ov=[lt('o2_lt1', 0.4, 3.0, y=1180), stamp('s_q', 3.0, 4.5, x=W - 200, y=720, rot=-6, sc=0.7)],
        sfx=[('error', 0.3, 0.6), ('type', 1.2, 0.4), ('type', 2.0, 0.4), ('gaffe', T['gaffe2'] - p + 0.3), ('trombone', T['gaffe2'] - p + 0.4, 0.6)]))
    sh.append(dict(src=s, dur=2.5, time=[(0, T['res1']), (2.5, T['res1'] + 2.3)], cam=[(0, *RES_CAM), (2.5, *RES_CAM)],
        fx=[('flash', 0.0, 0.1, 0.4)], ov=lt_cover('o2_res', 2.5), sfx=[('paper', 0.3, 0.6)]))
    h1 = T['h1']
    sh.append(dict(src=s, dur=1.0, time=[(0, T['gaffe2'] + 0.8), (1.0, gf - 1.0)], cam=[(0, *RC), (1.0, *RC)],
        fx=[('vhs', 0.0, 1.0, 0.9)], ov=[rew('o2_rew', 0.0, 1.0, y=TY)], sfx=[('rewind', 0.0, 0.8)]))
    sh.append(dict(src=s, dur=5.0, time=[(0, h1 - 1.3), (5.0, h1 + 3.7)], cam=[(0, *RC), (5.0, 1.07, 540, 990)],
        fx=[('flash', 1.3, 0.1, 0.5), ('punch', 1.3, 0.05, 0.2)], ov=[cap('o2_take2', 0.0, 2.6, y=TY)],
        sfx=[('perfect', 1.3, 0.7), ('cheer', 1.35, 0.5), ('applause', 2.5, 0.6), ('cheer', 3.6, 0.6)]))
    sh.append(dict(src=s, dur=3.0, time=[(0, h1 + 3.7), (3.0, T['res2'] - 0.4)], cam=[(0, 1.07, 540, 990), (3.0, 1.1, 540, 1000)],
        fx=[('flash', 0.0, 0.1, 0.4)], ov=[lt('o2_lt2', 0.3, 3.0, y=1180)],
        sfx=[('cheer', 0.2, 0.9), ('applause', 0.5, 0.8), ('fanfare', 0.4, 0.4)]))
    sh.append(dict(src=s, dur=2.5, time=[(0, T['res2']), (2.5, T['res2'] + 2.3)], cam=[(0, *RES_CAM), (2.5, *RES_CAM)],
        fx=[('flash', 0.0, 0.12, 0.6)], ov=[dict(img=g('topband'), u0=0.0, u1=2.5, x=W / 2, y=122, anim='none', out='cut')], sfx=[('win', 0.0), ('applause', 0.1, 0.7)]))
    sh.append(dict(src=s, dur=3.0, time=[(0, h1 + 2.0), (3.0, h1 + 4.2)], cam=[(0, *RC), (3.0, 1.07, 540, 990)],
        ov=[question('o2_q', 0.0, 3.0, y=TY)], sfx=[('cheer', 0.0, 0.6), ('pop2', 0.0, 0.5)]))
    thru(sh[0], sh[1], 0.2, 540, 900); thru(sh[4], sh[5], 0.2, 540, 900)
    return sh



# ---------------------------------------------------------------- O3: skandal zinciri (organik)
def o3(lang):
    T = {'en': dict(card2=8.1, click2=10.9, click1=3.3, win=29.1, toast=30.0), 'tr': dict(card2=8.1, click2=10.95, click1=3.35, win=29.07, toast=29.97)}[lang]  # olay + ~0,2 sn kare gecikmesi
    s = V('scandal', lang); sh = []; c2, k2, k1 = T['card2'], T['click2'], T['click1']
    CAM = (1.0, 540, 840)
    sh.append(dict(src=s, dur=3.5, time=[(0, c2 + 0.15), (3.5, k2 - 0.2)], cam=[(0, *CAM), (3.5, 1.04, 540, 850)],
        fx=[('flash', 0.0, 0.1, 0.5), ('tint', 0.0, 3.5, (40, 40, 200), 0.1)], ov=[words('o3_hook', 0.0, 3.5, y=430, step=0.09)],
        sfx=[('impact', 0.0, 0.7), ('sting', 0.05, 0.5), ('heart', 1.2, 0.7), ('heart', 1.8, 0.7), ('heart', 2.4, 0.8)]))
    sh.append(dict(src=s, dur=1.0, time=[(0, k2 - 0.2), (1.0, 0.7)], cam=[(0, 1.04, 540, 850), (1.0, *CAM)],
        fx=[('vhs', 0.0, 1.0, 0.9)], ov=[rew('o3_rew', 0.0, 1.0)], sfx=[('rewind', 0.0, 0.8)]))
    sh.append(dict(src=s, dur=3.0, time=[(0, 0.7), (3.0, k1 + 0.05)], cam=[(0, *CAM), (3.0, 1.04, 540, 850)],
        ov=[cap('o3_c1', 0.0, 3.0, y=430, sc=0.95), badge('b_a', 2.4, 3.0, 1150)], sfx=[('pop2', 0.0, 0.6), ('ring', 0.3, 0.4), ('select', 2.9)]))
    sh.append(dict(src=s, dur=3.5, time=[(0, k1 + 0.05), (3.5, k1 + 3.6)], cam=[(0, 1.04, 540, 850), (3.5, *CAM)],
        fx=[('flash', 0.3, 0.1, 0.5), ('shake', 0.3, 12, 0.3)], ov=[lt('o3_lt1', 0.4, 3.5, TOP)],
        sfx=[('error', 0.3, 0.6), ('trombone', 0.5, 0.5)]))
    sh.append(dict(src=s, dur=3.0, time=[(0, c2), (3.0, k2 + 0.02)], cam=[(0, *CAM), (3.0, 1.04, 540, 860)],
        fx=[('flash', 0.0, 0.12, 0.6), ('tint', 0.0, 3.0, (40, 40, 200), 0.08)],
        ov=[cap('o3_c2', 0.0, 3.0, y=430), badge('b_c', 2.2, 3.0, 1355)], sfx=[('impact', 0.0, 0.7), ('heart', 1.0, 0.7), ('select', 2.9)]))
    sh.append(dict(src=s, dur=6.0, time=[(0, 12.9), (6.0, 20.1)], cam=[(0, 1.0, 540, 960), (6.0, 1.05, 540, 980)],
        fx=[('flash', 0.0, 0.1, 0.5)], ov=[cap('o3_c3', 0.0, 2.6, y=430)],
        sfx=[('swoosh', 0.0, 0.5)] + [('tap', x, 0.35) for x in (1.0, 1.6, 2.5, 3.1, 3.9, 4.6, 5.4)]))
    w = T['win']
    sh.append(dict(src=s, dur=3.0, time=[(0, w - 2.0), (3.0, w + 1.0)], cam=[(0, 1.05, 540, 980), (3.0, 1.1, 540, 960)],
        fx=[('flash', 2.0, 0.12, 0.7), ('punch', 2.0, 0.06, 0.25)], ov=[stamp('o3_win', 2.0, 3.0, y=560, sc=0.8)],
        sfx=[('tap', 0.6, 0.35), ('tap', 1.4, 0.35), ('win', 2.0), ('cheer', 2.05, 0.6)]))
    sh.append(dict(src=s, dur=3.0, time=[(0, T['toast'] + 0.3), (3.0, T['toast'] + 3.2)], cam=[(0, *CAM), (3.0, 1.03, 540, 850)],
        fx=[('flash', 0.0, 0.1, 0.5)], ov=[lt('o3_lt2', 0.3, 3.0, TOP)], sfx=[('ding', 0.3, 0.6), ('applause', 0.5, 0.6)]))
    sh.append(dict(src=s, dur=2.5, time=[(0, 21.6), (2.5, 24.6)], cam=[(0, 1.0, 540, 960), (2.5, 1.04, 540, 960)],
        ov=[cap('o3_end', 0.0, 2.5, y=430, sc=0.95)], sfx=[('pop2', 0.0, 0.6), ('tap', 0.8, 0.35), ('tap', 1.6, 0.35)]))
    thru(sh[4], sh[5], 0.2, 540, 1355); thru(sh[6], sh[7], 0.2, 540, 900)
    return sh


VIDS = dict(a1=a1, a2=a2, a3=a3, o1=o1, o2=o2, o3=o3)


def beat_snap(sh):
    """Reklamlarda kesmeler 0,5 sn'lik müzik vuruşlarına oturmalı (kontrol)."""
    t = 0.0
    for s in sh:
        assert abs(round(t / BEAT) * BEAT - t) < 1e-6, f'kesme vuruş dışında: {t}'
        t += s['dur']


def build(vid, lang):
    H3.G = ED / 'gfx' / f'h4_{lang}'
    sp = specs(lang)
    sp['brk'] = ('pill', dict(text='● ' + BRK[lang]))
    gfx.render(sp, H3.G)
    band = np.zeros((245, W, 4), np.uint8); band[:, :, :3] = (32, 16, 11); band[:228, :, 3] = 255
    band[228:, :, 3] = np.linspace(255, 0, 17).astype(np.uint8)[:, None]
    import cv2; cv2.imwrite(str(H3.G / 'topband.png'), band)
    # tek satırlık yazılar (cap) iki satıra kırılmasın: sığana kadar küçült
    todo = {k: v for k, v in sp.items() if v[0] in ('cap', 'stamp') and '\n' not in v[1].get('text', '\n')}
    for _ in range(5):
        tall = {}
        for k, (kind, kw) in todo.items():
            if size(k)[1] > kw.get('size', 190) * 1.45 + 70:
                kw = dict(kw, size=int(kw.get('size', 190) * 0.9)); tall[k] = (kind, kw)
        if not tall: break
        gfx.render(tall, H3.G); todo = tall
    for k, (kind, kw) in sp.items():
        if kind == 'lt': assert size(k)[1] < 480, f'alt bant 3 satıra kırıldı: {k}'
    sh = VIDS[vid](lang)
    if vid in ADS: beat_snap(sh)
    total = sum(s['dur'] for s in sh)
    bw, _ = size('bug')
    end_bug = total - (sh[-1]['dur'] if 'card' in sh[-1] else 0)
    glob = [dict(img=g('bug'), u0=0.0, u1=end_bug, x=30 + bw / 2, y=262, anim='fade', out='cut')]
    OUT.mkdir(parents=True, exist_ok=True); SHEETS.mkdir(parents=True, exist_ok=True)
    raw = OUT / f'_{vid}_{lang}_raw.mp4'
    render(sh, raw, glob_ov=glob)
    final = OUT / f'{vid}_{lang}.mp4'
    crf = 21
    while True:
        cmd = ['ffmpeg', '-y', '-loglevel', 'error', '-i', str(raw)]
        if vid in ADS:  # oyunun chiptune altlığı, kısık
            mus = OUT / f'_{vid}_{lang}_music.wav'
            wavfile.write(str(mus), chiptune.SR, (chiptune.song(total, BPM, seed=4) * 32767).astype(np.int16))
            cmd += ['-i', str(mus), '-filter_complex', '[1:a]volume=0.22[m];[0:a][m]amix=inputs=2:duration=first:normalize=0,alimiter=limit=0.95[a]', '-map', '0:v', '-map', '[a]']
        cmd += ['-c:v', 'libx264', '-preset', 'veryfast', '-crf', str(crf), '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '128k', '-movflags', '+faststart', str(final)]
        subprocess.run(cmd, check=True)
        if final.stat().st_size < 9.5e6 or crf >= 30: break
        crf += 2
    for f in OUT.glob(f'_{vid}_{lang}_*'): f.unlink()
    raw.unlink(missing_ok=True)
    sheet = SHEETS / f'{vid}_{lang}.png'
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', str(final), '-vf', f'fps=16/{total:.2f},scale=200:356,tile=8x2', '-frames:v', '1', str(sheet)], check=True)
    print(final, round(total, 2), 's', round(final.stat().st_size / 1e6, 2), 'MB crf', crf, flush=True)


if __name__ == '__main__':
    build(sys.argv[1], sys.argv[2])
