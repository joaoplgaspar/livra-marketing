# Pauta A — Releitura conta na meta. Nível A (identidade completa do Livra).
# Filosofia: Segunda Margem (filosofia-a-segunda-margem.md).
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import *
from PIL import Image

OUT = os.path.join(HERE, '..', 'a-releitura')
INK, INK2, INK3 = '#16110d', '#221a14', '#3a2e25'
PAPER, PAPER2 = '#f4ecdc', '#eadfca'
BRAND, BRAND_D = '#e0552f', '#b53f20'
MARKER = '#f4d44d'
def mix(a, b, t):
    A, B = hexc(a), hexc(b)
    return '#%02x%02x%02x' % tuple(int(A[i] * (1 - t) + B[i] * t) for i in range(3))
MUTED_D = mix(INK, PAPER, .66)
MUTED_L = mix(PAPER, INK, .66)

XB = 'Bricolage-ExtraBold.ttf'; MD = 'Bricolage-Medium.ttf'; SB = 'Bricolage-SemiBold.ttf'
FI = 'Fraunces-Italic-Display.ttf'; FT = 'Fraunces-Italic-Text.ttf'; HAND = 'ReenieBeanie.ttf'
X0, MW = 96, 888
LOGO_DARK = Image.open(r'E:/Projetos/lura/redesign-livra/logo/final/png/livra-assinatura-escuro.png')
LOGO_LIGHT = Image.open(r'E:/Projetos/lura/redesign-livra/logo/final/png/livra-assinatura-claro.png')

def ribbon(s, x, w, length, color=BRAND, shade=BRAND_D):
    # fita de marcador pendurada da borda superior, com corte em V
    s.rect(x, 0, x + w, length, fill=color)
    s.poly([(x, length - 1), (x + w, length - 1), (x + w, length + w * 0.55), (x + w / 2, length + 2), (x, length + w * 0.55)], fill=color)
    s.rect(x + w - 8, 0, x + w, length, fill=shade)
    s.reg('~ribbon', x, 0, x + w, length + w * 0.55)

def h(size, fill, font=XB, tr=-.028, **kw):
    return Style(font, size, fill, track=tr * size, **kw)

def slide1():
    s = Slide(INK, 'a1')
    ribbon(s, 862, 64, 236)
    y, _ = s.text([('Releitura conta na meta.', h(162, PAPER))], X0, 250, 760, lh=.9, label='head')
    y2, _ = s.text([('Sim.', h(300, BRAND, FI, tr=-.02))], X0 - 6, y + 40, MW, label='sim')
    # rodada 2 (29/10): fundador vetou a nota "pode brigar nos comentários"
    return s

def slide2():
    s = Slide(PAPER, 'a2')
    # rodada 2 (29/10): no molde do slide 2 da versão X, que o fundador escolheu (centro, tracking fechado, risco na frase inteira)
    st = h(112, INK, tr=-.05)
    y, _ = s.text([('Todo fim de ano aparece alguém dizendo que ', st),
                   ('reler é trapacear a meta', st.but(deco='strike', deco_color=BRAND)), ('.', st)], X0, 675, 860, lh=.96, label='t', valign='middle', balance=False)
    return s

def slide3():
    s = Slide(INK, 'a3')
    y, _ = s.text([('Meta de leitura não é prova.', h(132, PAPER))], X0, 200, MW, lh=.92, label='t1')
    y2, _ = s.text([('Ninguém vai conferir a sua lista em dezembro.', Style(FT, 64, BRAND, track=-1.5))], X0, y + 70, 700, lh=1.12, label='t2')
    # lista sem conferir: doze linhas de caderno, a última é dezembro
    top = max(y2 + 110, 760)
    gap = (1250 - top) / 12
    for i in range(12):
        yy = top + i * gap
        c = MUTED_D if i < 11 else PAPER
        s.rect(X0, yy, X0 + 24, yy + 24, outline=mix(INK, PAPER, .35) if i < 11 else PAPER, width=3)
        s.line([(X0 + 54, yy + 14), (X0 + 54 + [520, 610, 440, 580, 500, 640, 470, 560, 600, 430, 540, 380][i], yy + 14)],
               mix(INK, PAPER, .22) if i < 11 else mix(INK, PAPER, .5), 4)
    return s

def slide4():
    s = Slide(PAPER, 'a4')
    y, _ = s.text([('Reler não é ler o mesmo livro.', h(112, INK))], X0, 190, MW, lh=.94, label='t1')
    num = Style(FI, 210, BRAND, track=-6)
    body = Style(SB, 54, INK, track=-1.2)
    # linha 15
    yA = y + 120
    s.text([('Aos 15', num)], X0 - 4, yA, MW, label='n15', bind_short=False)
    s.text([('você leu pelo romance.', body)], X0, yA + 250, MW, label='b15')
    s.line([(X0, yA + 372), (X0 + MW, yA + 372)], mix(PAPER, INK, .18), 2)
    yB = yA + 420
    s.text([('Aos 30', num)], X0 - 4, yB, MW, label='n30', bind_short=False)
    s.text([('percebe que era ', body), ('sobre a mãe', body.but(deco='mark', deco_color=MARKER)), ('.', body)], X0, yB + 250, MW, label='b30')
    return s

def slide5():
    s = Slide(INK, 'a5')
    y, _ = s.text([('A segunda leitura pega o que a primeira deixou passar:', h(96, PAPER))], X0, 240, MW, lh=.98, label='t1')
    it = Style(FI, 82, PAPER, track=-2)
    y2, _ = s.text([('a pista no capítulo', it), (' 2', it.but(deco='circle', deco_color=MARKER, padl=10, padr=22)), (',', it)], X0, y + 190, MW, label='l1', balance=False)
    y3, _ = s.text([('a frase que você não sublinhou', it.but(deco='underline', deco_color=BRAND)), ('.', it)], X0, y2 + 80, 760, lh=1.12, label='l2')
    return s

def slide6():
    s = Slide(BRAND, 'a6')
    st = h(118, '#ffffff')
    it = Style(FI, 122, INK, track=-3)
    y, _ = s.text([('Manda pra quem relê o mesmo livro todo dezembro e ', st),
                   ('ainda pede desculpa', it), ('.', it)], X0, 675, MW, lh=.98, label='t', valign='middle')
    return s

def slide7():
    s = Slide(INK, 'a7')
    st = Style(FI, 128, PAPER, track=-4)
    y, _ = s.text([('Se reler não contasse, ninguém teria ', st), ('livro preferido', st.but(fill=INK, deco='mark', deco_color=MARKER)), ('.', st)],
                  X0, 675, MW, lh=1.04, label='t', valign='middle')
    ribbon(s, 862, 64, 150)
    return s

def slide8():
    s = Slide(PAPER, 'a8')
    y, _ = s.text([('E na sua meta, releitura conta?', h(112, INK))], X0, 150, MW, lh=.94, label='q')
    it = Style(FI, 76, BRAND_D, track=-1.5)
    y2, _ = s.text([('Sim, não ou\n', Style(SB, 62, INK, track=-1.2)), ('“só se eu chorar de novo”', it), ('.', it.but(fill=INK))], X0, y + 60, MW, lh=1.3, label='opts', balance=False)
    # ponte
    yb = 810
    s.line([(X0, yb), (X0 + MW, yb)], mix(PAPER, INK, .2), 2)
    y3, _ = s.text([('No Livra, releitura tem botão próprio e entra no seu contador de leituras quando você termina.', Style(MD, 41, MUTED_L, track=-.4))],
                   X0, yb + 44, MW, lh=1.28, label='ponte', balance=True)
    s.paste(LOGO_LIGHT, X0, 1250 - 84, h=84, label='logo')
    return s

if __name__ == '__main__':
    allp = []
    for i, fn in enumerate([slide1, slide2, slide3, slide4, slide5, slide6, slide7, slide8], 1):
        allp += fn().save(os.path.join(OUT, f'{i:02d}.png'))
    print('problemas:', len(allp))
