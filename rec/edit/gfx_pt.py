"""Brezilya (PT-BR) kanal grafikleri: python3 -I gfx_pt.py -> gfx/pt/"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from gfx import render
OUT = pathlib.Path(__file__).parent / 'gfx' / 'pt'
S = 'PLANTÃO GABINETE · @GABINETEJOGO'
def lt(tag, head): return ('lt', dict(tag=tag, head=head, strip=S))
PT = {
    'bug': ('bug', dict(name='PLANTÃO GABINETE', live='AO VIVO')),
    'end_bg': ('endbg', {}), 'end_icon': ('icon', {}),
    'end_logo': ('logo', dict(text='GABINETE', latin=True)), 'end_sub': ('sub', dict(text='SIMULADOR POLÍTICO')),
    'end_handle': ('handle', dict(text='@gabinetejogo')), 'end_store': ('pill', dict(text='GRÁTIS NA APP STORE')),
    'b_a': ('badge', dict(text='A')), 'b_b': ('badge', dict(text='B')),
    # fuga da imprensa
    'h_dodge': ('cap', dict(text='DÁ PRA FUGIR DA IMPRENSA?', size=84, color='#ffffff')),
    'st_yorum': ('stamp', dict(text='COMENTA?', size=170, color='#f5b83d')),
    'lt_yak1': lt('URGENTE', 'PREFEITO É PEGO\nNA PORTA'),
    'lt_gozluk': lt('NOVA TÁTICA', 'ÓCULOS ESCUROS:\nINVISÍVEL'),
    'lt_araba': lt('URGENTE', 'PREFEITO CHEGA\nAO CARRO'),
    'end_dodge': ('tagl', dict(text='VOCÊ\nESCAPARIA?')),
    # cartas de crise
    'h_kart': ('cap', dict(text='O PAPAGAIO SUMIU. E AGORA?', size=82, color='#ffffff')),
    'c_papagan': ('cap', dict(text='O PAPAGAIO MASCOTE SUMIU', size=78, color='#ffffff')),
    'c_cesme': ('cap', dict(text='CHAFARIZ INAUGURADO 4 VEZES', size=74, color='#ffffff')),
    'c_anne': ('cap', dict(text='SUA MÃE LIGOU', size=110, color='#ffffff')),
    'lt_papagan': lt('URGENTE', 'PAPAGAIO NOVO\nENTREGOU TUDO'),
    'lt_cesme': lt('URGENTE', 'QUARTA INAUGURAÇÃO,\nMESMA FITA'),
    'lt_anne': lt('URGENTE', 'MÃE NÃO ACREDITOU,\nMANDOU TORTA'),
    'end_kart': ('tagl', dict(text='QUAL VOCÊ\nESCOLHERIA?')), 'end_ab': ('pill', dict(text='COMENTA: A OU B')),
    # trailer
    'hA': ('cap', dict(text='DE ZÉ-NINGUÉM\nA PRESIDENTE', size=118, color='#ffffff')),
    'hB': ('cap', dict(text='VOCÊ DURARIA\n1 SEMANA?', size=124, color='#ffffff')),
    'lad1': ('pill', dict(text='CARGO: VEREADOR')), 'lad2': ('pill', dict(text='CARGO: PREFEITO')),
    'lad3': ('pill', dict(text='CARGO: GOVERNADOR')), 'lad4': ('pill', dict(text='CARGO: PRESIDENTE')),
    'v_konvoy': ('cap', dict(text='LEVE A COMITIVA', size=96, color='#f5b83d')),
    'v_stack': ('cap', dict(text='ERGA A OBRA', size=104, color='#f5b83d')),
    'v_dodge': ('cap', dict(text='FUJA DA IMPRENSA', size=96, color='#f5b83d')),
    'v_delegate': ('cap', dict(text='CONQUISTE DELEGADOS', size=88, color='#f5b83d')),
    'v_frame': ('cap', dict(text='POSE PRA FOTO', size=100, color='#f5b83d')),
    'v_trend': ('cap', dict(text='VENÇA NAS REDES', size=96, color='#f5b83d')),
    'v_summit': ('cap', dict(text='APERTE A MÃO CERTA', size=90, color='#f5b83d')),
    'v_debate': ('cap', dict(text='VENÇA O DEBATE', size=98, color='#f5b83d')),
    'v_bus': ('cap', dict(text='AGITE A GALERA', size=98, color='#f5b83d')),
    'v_more': ('stamp', dict(text='18\nMINIJOGOS', size=170, color='#e43b34', stroke=16)),
    'st_pres': ('stamp', dict(text='PRESIDENTE!', size=165, color='#f5b83d', stroke=14)),
    'end_tr': ('tagl', dict(text='ATÉ ONDE\nVOCÊ CHEGA?')), 'end_18': ('pill', dict(text='18 MINIJOGOS')),
}
if __name__ == '__main__':
    print(len(render(PT, OUT)))
