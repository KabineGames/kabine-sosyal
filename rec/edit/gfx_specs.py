"""All overlay graphics for the week-2 style edits (TR + EN)."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from gfx import render

OUT = pathlib.Path(__file__).parent / 'gfx'

TR = {
    'bug': ('bug', dict(name='KABİNE HABER', live='CANLI')),
    'gaf': ('stamp', dict(text='GAF!', size=300)),
    'q_asfalt': ('quote', dict(text='“ASFALTI\nYEDİK!”', size=190)),
    'rew_pzt': ('rew', dict(text='◀◀ 3 GÜN ÖNCE')),
    'd_pzt': ('pill', dict(text='PAZARTESİ')), 'd_sal': ('pill', dict(text='SALI')), 'd_car': ('pill', dict(text='ÇARŞAMBA')),
    'd_per': ('pill', dict(text='PERŞEMBE')), 'd_cum': ('pill', dict(text='CUMA')), 'd_cmt': ('pill', dict(text='CUMARTESİ')), 'd_paz': ('pill', dict(text='PAZAR')),
    'lt_kedi': ('lt', dict(head='KEDİ MECLİS\nÜYESİ OLDU')),
    'lt_anne': ('lt', dict(head='ANNE İNANMADI,\nBÖREK YOLLADI')),
    'lt_miting': ('lt', dict(head='MEYDAN\nYIKILDI')),
    'lt_gaf': ('lt', dict(tag='CANLI YAYIN', head='ADAY: “ASFALTI\nYEDİK!”')),
    'lt_otobus': ('lt', dict(head='SİMİT YAĞMURU:\nTEYZE YAKALADI')),
    'lt_saksi': ('lt', dict(tag='SON DAKİKA', head='SAKSI KURBAN\nGİTTİ')),
    'lt_basin': ('lt', dict(head='BASINDAN\nKAÇAMADI')),
    'lt_secim': ('lt', dict(head='KIL PAYI!\nYENİ BAŞKAN')),
    'cap_ohal': ('cap', dict(text='…VE O AN GELDİ', size=120, color='#f5b83d')),
    'cap_live': ('cap', dict(text='CANLI YAYINDA ADAY:', size=104, color='#ffffff')),
    'st_yorum': ('stamp', dict(text='YORUM?', size=170, color='#f5b83d')),
    'st_kazandi': ('stamp', dict(text='%50,4', size=230, color='#f5b83d')),
    'end_bg': ('endbg', {}), 'end_icon': ('icon', {}), 'end_logo': ('logo', dict(text='KABİNE')), 'end_sub': ('sub', dict(text='BAŞKANLIK SİMÜLATÖRÜ')),
    'end_tag': ('tagl', dict(text='BELEDİYEDEN\nBAŞKANLIĞA')), 'end_handle': ('handle', dict(text='@kabinegame')), 'end_soon': ('pill', dict(text='YAKINDA')),
    # zürafa A/B
    'lt_zurafa': ('lt', dict(head='RAKİP HER EVE\nZÜRAFA VAAT ETTİ')),
    'st_senolsan': ('stamp', dict(text='SEN\nOLSAN?', size=190, color='#f5b83d')),
    'b_a': ('badge', dict(text='A')), 'b_b': ('badge', dict(text='B')),
    'n3': ('stamp', dict(text='3', size=420, color='#f5b83d', stroke=16)), 'n2': ('stamp', dict(text='2', size=420, color='#f5b83d', stroke=16)), 'n1': ('stamp', dict(text='1', size=420, color='#f5b83d', stroke=16)),
    'lt_a': ('lt', dict(tag='A SEÇİLDİ', head='İKİ ZÜRAFA!\nHALK ÇILDIRDI')),
    'lt_b': ('lt', dict(tag='B SEÇİLDİ', head='CİDDİ ADAY.\nÇOCUKLAR AĞLADI')),
    'rew_b': ('rew', dict(text='◀◀ YA B\nDESEYDİN?')),
    'end_q': ('tagl', dict(text='SEN HANGİSİNİ\nSEÇERDİN?')),
    'end_ab': ('pill', dict(text='YORUMA A YA DA B YAZ')),
}

EN = {
    'bug': ('bug', dict(name='CABINET NEWS', live='LIVE')),
    'gaf': ('stamp', dict(text='GAFFE!', size=250)),
    'q_asfalt': ('quote', dict(text='“WE ATE\nTHE ASPHALT!”', size=170)),
    'rew_pzt': ('rew', dict(text='◀◀ 3 DAYS EARLIER')),
    'd_pzt': ('pill', dict(text='MONDAY')), 'd_sal': ('pill', dict(text='TUESDAY')), 'd_car': ('pill', dict(text='WEDNESDAY')),
    'd_per': ('pill', dict(text='THURSDAY')), 'd_cum': ('pill', dict(text='FRIDAY')), 'd_cmt': ('pill', dict(text='SATURDAY')), 'd_paz': ('pill', dict(text='SUNDAY')),
    'lt_kedi': ('lt', dict(tag='BREAKING', head='CAT JOINS\nCITY COUNCIL', strip='CABINET NEWS · @KABINEGAME')),
    'lt_anne': ('lt', dict(tag='BREAKING', head='MOM UNCONVINCED,\nSENDS FOOD', strip='CABINET NEWS · @KABINEGAME')),
    'lt_miting': ('lt', dict(tag='BREAKING', head='CROWD GOES\nWILD', strip='CABINET NEWS · @KABINEGAME')),
    'lt_gaf': ('lt', dict(tag='LIVE', head='CANDIDATE: “WE ATE\nTHE ASPHALT!”', strip='CABINET NEWS · @KABINEGAME')),
    'lt_otobus': ('lt', dict(tag='BREAKING', head='BAGEL STORM:\nGRANDMA CATCHES IT', strip='CABINET NEWS · @KABINEGAME')),
    'lt_saksi': ('lt', dict(tag='BREAKING', head='ONE FLOWER POT\nDID NOT SURVIVE', strip='CABINET NEWS · @KABINEGAME')),
    'lt_basin': ('lt', dict(tag='BREAKING', head='PRESS ESCAPE\nFAILED', strip='CABINET NEWS · @KABINEGAME')),
    'lt_secim': ('lt', dict(tag='BREAKING', head='BY A HAIR!\nNEW MAYOR', strip='CABINET NEWS · @KABINEGAME')),
    'cap_ohal': ('cap', dict(text='…AND THEN IT HAPPENED', size=110, color='#f5b83d')),
    'cap_live': ('cap', dict(text='LIVE ON AIR, THE CANDIDATE:', size=92, color='#ffffff')),
    'st_yorum': ('stamp', dict(text='COMMENT?', size=150, color='#f5b83d')),
    'st_kazandi': ('stamp', dict(text='50.4%', size=230, color='#f5b83d')),
    'end_bg': ('endbg', {}), 'end_icon': ('icon', {}), 'end_logo': ('logo', dict(text='CABINET', latin=True)), 'end_sub': ('sub', dict(text='PRESIDENT SIMULATOR')),
    'end_tag': ('tagl', dict(text='FROM CITY COUNCIL\nTO THE TOP')), 'end_handle': ('handle', dict(text='@kabinegame')), 'end_soon': ('pill', dict(text='COMING SOON')),
    'lt_zurafa': ('lt', dict(tag='BREAKING', head='RIVAL PROMISES\nEVERY HOME A GIRAFFE', strip='CABINET NEWS · @KABINEGAME')),
    'st_senolsan': ('stamp', dict(text='YOUR\nMOVE?', size=190, color='#f5b83d')),
    'b_a': ('badge', dict(text='A')), 'b_b': ('badge', dict(text='B')),
    'n3': ('stamp', dict(text='3', size=420, color='#f5b83d', stroke=16)), 'n2': ('stamp', dict(text='2', size=420, color='#f5b83d', stroke=16)), 'n1': ('stamp', dict(text='1', size=420, color='#f5b83d', stroke=16)),
    'lt_a': ('lt', dict(tag='YOU PICKED A', head='TWO GIRAFFES!\nCROWD GOES WILD', strip='CABINET NEWS · @KABINEGAME')),
    'lt_b': ('lt', dict(tag='YOU PICKED B', head='SERIOUS CANDIDATE.\nKIDS CRIED', strip='CABINET NEWS · @KABINEGAME')),
    'rew_b': ('rew', dict(text='◀◀ WHAT IF\nYOU PICKED B?')),
    'end_q': ('tagl', dict(text='WHICH ONE\nWOULD YOU PICK?')),
    'end_ab': ('pill', dict(text='COMMENT A OR B')),
}


def build(lang):
    return render(TR if lang == 'tr' else EN, OUT / lang)


if __name__ == '__main__':
    for l in sys.argv[1:] or ['tr', 'en']:
        print(l, len(build(l)))
