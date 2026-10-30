# Pauta C — Red flags de quem lê. Nível C (sem marca; só "@livraapp" discreto no último slide).
# Filosofia: Código de Sinais (filosofia-c-codigo-de-sinais.md).
# Tema (theme-factory, tema próprio): "Sinal Vermelho" — papel quente, preto de impressão, vermelho de sinalização;
# Instrument Sans Bold + Instrument Serif Italic + Big Shoulders Bold (fontes da canvas-design).
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import *

OUT = os.path.join(HERE, '..', 'c-red-flags')
PAPER, INK, RED = '#f3eee5', '#151313', '#e0281e'
def mix(a, b, t):
    A, B = hexc(a), hexc(b)
    return '#%02x%02x%02x' % tuple(int(A[i] * (1 - t) + B[i] * t) for i in range(3))
GREY = mix(PAPER, INK, .38)
LINE = mix(PAPER, INK, .82)

SANS = 'InstrumentSans-Bold.ttf'; SERIF = 'InstrumentSerif-Italic.ttf'; SIGN = 'BigShoulders-Bold.ttf'; REG = 'InstrumentSans-Regular.ttf'
X0, MW = 96, 888
NL = chr(10)

def b(size, fill=INK, tr=-.03):
    return Style(SANS, size, fill, track=tr * size)
def it(size, fill=RED):
    return Style(SERIF, size, fill, track=-.01 * size)

def flag(s, x, y, pole, fw, fh, filled, color=RED, outline=INK, stroke=4):
    """galhardete: haste em x, topo em y."""
    s.rect(x - stroke / 2, y, x + stroke / 2, y + pole, fill=outline if not filled else INK)
    pts = [(x + stroke / 2, y), (x + fw, y + fh / 2), (x + stroke / 2, y + fh)]
    if filled:
        s.poly(pts, fill=color)
    else:
        s.line(pts + [pts[0]], outline, stroke)
    s.reg('~flag', x - stroke, y, x + fw, y + pole)

def flag_row(s, y, n_filled=None, which=None, pole=200, fw=120, fh=90, base_color=INK, numbers=False, fill=RED):
    gap = (MW - fw) / 4
    for i in range(5):
        x = X0 + 6 + i * gap
        on = (which is not None and i + 1 == which) or (n_filled is not None and i < n_filled)
        flag(s, x, y, pole, fw, fh, on, color=fill, outline=base_color)
        if numbers:
            s.text([(str(i + 1), Style(SIGN, 64, INK if not on else RED, track=0))], x - 30, y + pole + 26, 60, align='center', label=f'num{i}', bind_short=False)
    s.line([(X0, y + pole), (X0 + MW, y + pole)], base_color, 4)

def label(s, n, y=140, color=RED, ink=INK):
    flag(s, X0 + 2, y, 74, 54, 40, True, color=color, outline=ink, stroke=4)
    s.text([(f'Red flag {n}', Style(SIGN, 64, ink, track=1.5, upper=True))], X0 + 84, y + 8, 600, label='label', bind_short=False)

def slide1():
    s = Slide(PAPER, 'c1')
    y, _ = s.text([('Red flags de quem lê', b(150))], X0, 170, MW, lh=.92, label='head')
    s.text([('(a 4ª é você)', it(130))], X0, y + 30, MW, label='sub')
    flag_row(s, 940, which=4, pole=250, fw=150, fh=110)
    return s

def slide2():
    s = Slide(PAPER, 'c2')
    flag_row(s, 150, n_filled=3, pole=170, fw=110, fh=82)
    s.text([('Se você se reconhecer' + NL + 'em 3 ou mais,' + NL, b(88)), ('o problema não é' + NL + 'falta de tempo.', b(88).but(fill=RED))], X0, 1236, MW, lh=1.0, label='t', valign='bottom')
    return s

def slide3():
    s = Slide(PAPER, 'c3')
    label(s, 1)
    y, _ = s.text([('Compra livro novo com 47 na pilha.', b(96))], X0, 300, MW, lh=.98, label='t')
    s.text([('"Esse é diferente."'.replace('"', '“', 1).replace('"', '”'), it(92))], X0, y + 60, MW, lh=1.0, label='aside')
    # a pilha: 47 lombadas + a nova, vermelha, no topo
    rng = random.Random(47)
    base = 1240; hgt = 7; gap = 2.2
    cx = 846
    for k in range(47):
        w = rng.uniform(170, 250); off = rng.uniform(-14, 14)
        yy = base - (k + 1) * (hgt + gap)
        s.rect(cx - w / 2 + off, yy, cx + w / 2 + off, yy + hgt, fill=INK if k % 7 else mix(PAPER, INK, .6))
    yy = base - 47 * (hgt + gap) - 18 - 6
    s.rect(cx - 112, yy, cx + 106, yy + 18, fill=RED)
    s.reg('~stack', cx - 140, yy, cx + 140, base)
    s.reg('stackbox', cx - 140, yy, cx + 140, base)
    return s

def slide4():
    s = Slide(PAPER, 'c4')
    label(s, 2)
    s.text([('Lê o final antes, ', b(96)), ('“só pra ver se vale a pena”', it(104)), ('.', b(96))], X0, 300, MW, lh=1.0, label='t')
    # o livro como fileira de páginas; um salto da primeira para a última
    y0, y1 = 1060, 1230
    n = 44
    step = MW / (n - 1)
    for k in range(n):
        x = X0 + k * step
        last = k == n - 1
        s.rect(x - 2, y0 + (0 if last or k == 0 else 40), x + 2, y1, fill=RED if last else (INK if k == 0 else mix(PAPER, INK, .45)))
    # arco
    pts = []
    for t in range(0, 61):
        u = t / 60
        x = X0 + u * MW
        yy = y0 - 20 - math.sin(u * math.pi) * 150
        pts.append((x, yy))
    s.line(pts, RED, 5)
    s.poly([(X0 + MW, y0 - 6), (X0 + MW - 26, y0 - 40), (X0 + MW + 12, y0 - 38)], fill=RED)
    s.reg('diagram', X0, y0 - 180, X0 + MW, y1)
    return s

def slide5():
    s = Slide(PAPER, 'c5')
    label(s, 3)
    y, _ = s.text([('Fala' + NL, b(92)), ('“só mais um capítulo”', it(104)), (NL + 'à 1h da manhã.', b(92))], X0, 300, MW, lh=1.0, label='t', balance=False)
    s.text([('São 3h.', b(150, RED))], X0, y + 90, 520, label='sao')
    # mostrador: ponteiro fantasma na 1h, ponteiro real nas 3h
    cx, cy, r = 790, 1040, 180
    s.ellipse(cx - r, cy - r, cx + r, cy + r, outline=INK, width=5)
    for k in range(12):
        a = math.radians(k * 30 - 90)
        r0 = r - (30 if k % 3 == 0 else 18)
        s.line([(cx + r0 * math.cos(a), cy + r0 * math.sin(a)), (cx + (r - 8) * math.cos(a), cy + (r - 8) * math.sin(a))], INK, 5 if k % 3 == 0 else 3)
    # arco 1h -> 3h
    arc = [(cx + (r - 48) * math.cos(math.radians(a)), cy + (r - 48) * math.sin(math.radians(a))) for a in range(-60, 1, 2)]
    s.line(arc, RED, 4)
    a1 = math.radians(-60)
    s.line([(cx, cy), (cx + (r - 70) * math.cos(a1), cy + (r - 70) * math.sin(a1))], mix(PAPER, INK, .35), 8)
    s.line([(cx, cy), (cx + (r - 64), cy)], RED, 12)
    s.ellipse(cx - 13, cy - 13, cx + 13, cy + 13, fill=INK)
    s.reg('clock', cx - r, cy - r, cx + r, cy + r)
    return s

def slide6():
    s = Slide(RED, 'c6')
    label(s, 4, color=PAPER, ink=PAPER)
    y, _ = s.text([('Empresta livro e anota mentalmente a data.', b(96, PAPER))], X0, 300, MW, lh=.98, label='t')
    s.text([('E o estado da lombada.', it(112, INK))], X0, y + 70, 560, lh=.98, label='aside')
    # a lombada: um livro de pé, com o vinco que ninguém perdoa
    x0, x1, yt, yb = 760, 900, 760, 1240
    s.rect(x0, yt, x1, yb, outline=PAPER, width=5)
    s.line([(x0 + 16, yt + 70), (x1 - 16, yt + 70)], PAPER, 3)
    s.line([(x0 + 16, yb - 70), (x1 - 16, yb - 70)], PAPER, 3)
    s.line([(x0 + 22, yt + 250), (x1 - 30, yt + 214)], INK, 4)
    s.line([(x0 + 30, yt + 300), (x1 - 22, yt + 282)], INK, 4)
    s.reg('spine', x0, yt, x1, yb)
    return s

def slide7():
    s = Slide(PAPER, 'c7')
    label(s, 5)
    s.text([('Julga a pessoa pela estante antes de dizer oi.', b(104))], X0, 300, MW, lh=.98, label='t')
    # estante
    rng = random.Random(5)
    base = 1210
    x = X0 + 8
    k = 0
    while True:
        w = rng.choice([30, 36, 42, 48, 54, 28])
        hh = rng.uniform(190, 290)
        if x + w > X0 + MW - 8: break
        lean = k == 9
        col = RED if k == 6 else INK
        if lean:
            s.poly([(x, base), (x + w, base), (x + w + 60, base - hh + 10), (x + 60 - 0, base - hh + 10)], outline=col, width=4)
            x += w + 64
        else:
            s.rect(x, base - hh, x + w, base, fill=col if k == 6 else None, outline=col, width=4)
            x += w + 8
        k += 1
    s.rect(X0, base, X0 + MW, base + 14, fill=INK)
    s.reg('shelf', X0, base - 300, X0 + MW, base + 14)
    return s

def slide8():
    s = Slide(PAPER, 'c8')
    y, _ = s.text([('Manda pra pessoa que fez pelo menos 4.', b(104))], X0, 170, MW, lh=.98, label='t')
    s.text([('Ela sabe quem é.', it(120))], X0, y + 50, MW, label='aside')
    flag_row(s, 980, n_filled=4, pole=220, fw=140, fh=104)
    return s

def slide9():
    s = Slide(PAPER, 'c9')
    y, _ = s.text([('Qual é a sua?' + NL + 'Comenta o número.', b(96))], X0, 150, MW, lh=.98, label='t')
    y2, _ = s.text([('Ninguém julga. ', b(96)), ('(Julga sim.)', it(110))], X0, y + 34, MW, lh=1.0, label='t2', balance=False)
    flag_row(s, 830, which=None, n_filled=0, pole=200, fw=120, fh=90, numbers=True)
    s.text([('@livraapp', Style(REG, 34, GREY, track=0))], X0, 1250 - 34, 400, label='handle', bind_short=False)
    return s

if __name__ == '__main__':
    import random
    allp = []
    for i, fn in enumerate([slide1, slide2, slide3, slide4, slide5, slide6, slide7, slide8, slide9], 1):
        allp += fn().save(os.path.join(OUT, f'{i:02d}.png'), grain=4)
    print('problemas:', len(allp))
