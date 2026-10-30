# Pauta B — 4 suspenses nacionais que acabam num fim de semana. Nível B (toque do Livra).
# Filosofia: Arquivo Noturno (filosofia-b-arquivo-noturno.md).
# Tema (theme-factory): Ocean Depths — paleta do tema. Toque do Livra = fontes (Bricolage, Fraunces itálico,
# Reenie Beanie) + assinatura pequena no último slide.
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import *
from PIL import Image

OUT = os.path.join(HERE, '..', 'b-suspense-nacional')
CAPAS = os.path.join(HERE, '..', '..', 'capas')
NAVY, TEAL, SEA, CREAM = '#1a2332', '#2d8b8b', '#a8dadc', '#f1faee'
def mix(a, b, t):
    A, B = hexc(a), hexc(b)
    return '#%02x%02x%02x' % tuple(int(A[i] * (1 - t) + B[i] * t) for i in range(3))
NAVY_L = mix(NAVY, CREAM, .07)
RULE = mix(NAVY, SEA, .28)
CREAM_M = mix(NAVY, CREAM, .8)

XB = 'Bricolage-ExtraBold.ttf'; MD = 'Bricolage-Medium.ttf'; SB = 'Bricolage-SemiBold.ttf'
FI = 'Fraunces-Italic-Display.ttf'; FT = 'Fraunces-Italic-Text.ttf'; HAND = 'ReenieBeanie.ttf'
X0, MW = 96, 888
LOGO = Image.open(r'E:/Projetos/lura/redesign-livra/logo/final/png/livra-assinatura-escuro.png')

BOOKS = [
    ('Borges e os orangotangos eternos', 'Luis Fernando Verissimo', 133, 'borges.jpg',
     'Um cinquentão que vive entre livros vai a um congresso sobre Edgar Allan Poe em Buenos Aires, conhece Jorge Luis Borges e acaba no meio de um crime.'),
    ('O silêncio da chuva', 'Luiz Alfredo Garcia-Roza', 262, 'silencio-da-chuva.jpg',
     'Um executivo aparece morto ao volante do próprio carro, no centro do Rio. Ninguém viu nada. O inspetor Espinosa começa a puxar o fio.'),
    ('Uma mulher no escuro', 'Raphael Montes', 273, 'mulher-no-escuro.jpg',
     'Victoria tinha quatro anos quando a família foi assassinada. Vinte anos depois, o assassino volta. Jabuti 2020 de romance de entretenimento.'),
    ('Dias perfeitos', 'Raphael Montes', 274, 'dias-perfeitos.jpg',
     'Amor obsessivo e paranoico, do mesmo autor que criou Bom dia, Verônica. Sombrio e claustrofóbico.'),
]
def cover(name):
    im = Image.open(os.path.join(CAPAS, name)).convert('RGB')
    # recorte 2:3 exato
    w, h = im.size
    tw = int(h * 2 / 3)
    if w > tw:
        x = (w - tw) // 2; im = im.crop((x, 0, x + tw, h))
    return im

def h(size, fill, font=XB, tr=-.028, **kw):
    return Style(font, size, fill, track=tr * size, **kw)

def place_cover(s, name, x, y, w, label):
    hh = w * 1.5
    s.shadow(x, y, x + w, y + hh, color=(4, 8, 14, 170), blur=22, off=(0, 16))
    s.paste(cover(name), x, y, w, hh, label=label)
    s.rect(x, y, x + w, y + hh, outline=mix(NAVY, CREAM, .35), width=1)
    return y + hh

def ruler(s, x, y, w, pages, scale_max=600, limit=280, bar_h=14, full=False, dim=False, label='~ruler'):
    """régua de páginas: traço fino a cada 10 páginas, traço alto no limite de 280."""
    px = w / scale_max
    for p in range(0, scale_max + 1, 10):
        tall = p % 100 == 0
        s.line([(x + p * px, y + bar_h + 6), (x + p * px, y + bar_h + 6 + (14 if tall else 7))], RULE, 1.5)
    s.rect(x, y, x + w, y + bar_h, fill=mix(NAVY, CREAM, .06))
    if pages:
        s.rect(x, y, x + pages * px, y + bar_h, fill=(SEA if not dim else mix(NAVY, CREAM, .22)))
    s.line([(x + limit * px, y - 18), (x + limit * px, y + bar_h + 30)], CREAM, 3)
    s.reg(label, x, y - 18, x + w, y + bar_h + 30)

def slide1():
    s = Slide(NAVY, 'b1')
    s.text([('4', Style(FI, 430, SEA, track=0))], X0 - 14, -34, 400, label='num', bind_short=False)
    y, _ = s.text([('suspenses nacionais que acabam num fim' + chr(160) + 'de' + chr(160) + 'semana', h(96, CREAM))], X0, 472, MW, lh=.96, label='head')
    s.rotated_text('todos com menos de 280 páginas', Style(HAND, 76, SEA), 532, y + 78, -2.5, label='nota')
    cw, gap = 196, (MW - 4 * 196) / 3
    for i, b in enumerate(BOOKS):
        place_cover(s, b[3], X0 + i * (cw + gap), 1270 - cw * 1.5, cw, f'capa{i}')
    return s

def slide2():
    s = Slide(NAVY, 'b2')
    y, _ = s.text([('Nada de tijolo de 600 páginas.', h(112, CREAM))], X0, 150, MW, lh=.94, label='t1')
    y2, _ = s.text([('Começa sexta à noite, termina domingo antes do jantar.', Style(FI, 66, SEA, track=-1.5))], X0, y + 60, MW, lh=1.14, label='t2')
    # diagrama: o tijolo (600) contra os quatro livros, na mesma régua
    top = 820
    ruler(s, X0, top, MW, 600, dim=True, label='~r0')
    for i, b in enumerate(BOOKS):
        ruler(s, X0, top + 84 * (i + 1), MW, b[2], label=f'~r{i+1}')
    return s

def book_slide(i):
    title, author, pages, img, syn = BOOKS[i]
    s = Slide(NAVY, f'b{i+3}')
    cw = 384
    bottom = place_cover(s, img, X0, 120, cw, 'capa')
    cx = X0 + cw + 52
    cwid = X0 + MW - cx
    s.text([(str(i + 1), Style(FI, 230, SEA, track=0))], cx - 6, 108, cwid, label='num', bind_short=False)
    y, _ = s.text([(title, h(58, CREAM, tr=-.022))], cx, 390, cwid, lh=1.0, label='title')
    y2, _ = s.text([(author, Style(FT, 42, SEA, track=-.6))], cx, y + 34, cwid, lh=1.12, label='author')
    y4, _ = s.text([(syn, Style(MD, 43, CREAM, track=-.3))], X0, bottom + 64, MW, lh=1.3, label='syn', balance=False)
    s.text([(f'{pages} páginas', Style(SB, 40, SEA, track=-.4))], X0, 1236 - 86, MW, label='pages', bind_short=False)
    ruler(s, X0, 1236, MW, pages)
    return s

def slide7():
    s = Slide(NAVY, 'b7')
    st = h(122, CREAM)
    it = Style(FI, 128, SEA, track=-3)
    s.text([('Manda pra quem diz que ', st), ('não tem tempo de ler', it), ('.', it)], X0, 675, MW, lh=.98, label='t', valign='middle')
    return s

def slide8():
    s = Slide(NAVY, 'b8')
    y, _ = s.text([('Qual você' + chr(10) + 'começa na sexta?', h(112, CREAM))], X0, 140, MW, lh=.94, label='q')
    y2, _ = s.text([('Responde com o número.', Style(FI, 68, SEA, track=-1.5))], X0, y + 46, MW, label='r')
    cw, gap = 192, (MW - 4 * 192) / 3
    ytop = y2 + 80
    for i, b in enumerate(BOOKS):
        x = X0 + i * (cw + gap)
        yb = place_cover(s, b[3], x, ytop, cw, f'capa{i}')
        s.text([(str(i + 1), Style(FI, 76, SEA, track=0))], x, yb + 34, cw, align='center', label=f'n{i}', bind_short=False)
    s.text([('Salva pra quando o fim de semana chegar.', Style(SB, 46, CREAM, track=-.6))], X0, 1110, 640, lh=1.15, label='salva')
    s.paste(LOGO, X0 + MW - 150, 1238 - 52, h=52, label='logo')
    return s

if __name__ == '__main__':
    allp = []
    fns = [slide1, slide2] + [lambda i=i: book_slide(i) for i in range(4)] + [slide7, slide8]
    for i, fn in enumerate(fns, 1):
        allp += fn().save(os.path.join(OUT, f'{i:02d}.png'), grain=4.5)
    print('problemas:', len(allp))
