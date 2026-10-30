# Motor de composição em PIL para os carrosséis do caminho 2 (canvas-design + theme-factory).
# Desenha em 2x e reduz para 1080x1350. Registra caixas de texto/imagem e acusa
# vazamento de margem e colisão antes de salvar.
import math, os, random
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np

S = 2
W, H = 1080, 1350
HERE = os.path.dirname(os.path.abspath(__file__))
FONTS = os.path.join(HERE, 'fonts')
CANVAS_FONTS = r'C:\ClaudeAccounts\Livra\.claude\skills\canvas-design\canvas-fonts'
MARGIN_X = 80
MARGIN_Y = 60

_fc = {}
def font(name, size):
    key = (name, size)
    if key not in _fc:
        p = name
        for base in (os.path.join(FONTS, 'static'), FONTS, CANVAS_FONTS):
            if os.path.exists(os.path.join(base, name)):
                p = os.path.join(base, name); break
        _fc[key] = ImageFont.truetype(p, int(round(size * S)))
    return _fc[key]

def hexc(h, a=255):
    h = h.lstrip('#')
    return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16), a)

class Style:
    def __init__(self, fontname, size, fill, track=0.0, deco=None, deco_color=None, upper=False):
        self.fontname, self.size, self.fill = fontname, size, fill
        self.track = track  # em unidades de 1080 (px), pode ser negativo
        self.deco, self.deco_color, self.upper = deco, deco_color, upper
    @property
    def f(self): return font(self.fontname, self.size)
    def but(self, **kw):
        s = Style(self.fontname, self.size, self.fill, self.track, self.deco, self.deco_color, self.upper)
        for k, v in kw.items(): setattr(s, k, v)
        return s
    padl = 0
    padr = 0

def text_w(s, st):
    s = s.replace('\u00a0', ' ')
    if not s: return 0
    return st.f.getlength(s) / S + (len(s) - 1) * st.track

SHORT = {'a','o','e','é','de','da','do','no','na','em','um','os','as','ou','se','só','à','ao','pra','que','um','uma','nos','nas','dos','das','sua','seu','não','sim,','não,'}

def _tokens(segments):
    """segments: list[(text, Style)] -> tokens [(word, style, gid)] e quebras forçadas ('\n')."""
    toks = []
    for gid, (text, st) in enumerate(segments):
        if st.upper: text = text.upper()
        parts = text.split('\n')
        for pi, part in enumerate(parts):
            if pi > 0: toks.append(('\n', st, gid, False))
            words = part.split(' ')
            for wi, w in enumerate(words):
                if w == '':
                    continue
                # gruda em palavra anterior se não houve espaço antes (pontuação colada entre segmentos)
                glue = (wi == 0 and not part.startswith(' ') and toks and toks[-1][0] != '\n' and pi == 0
                        and gid > 0 and not segments[gid - 1][0].endswith((' ', '\n')))
                toks.append((w, st, gid, glue))
    # amarra palavras curtas à seguinte (sem viúva de "a", "de"...)
    out = []
    for t in toks:
        out.append(list(t))
    return out

def layout(segments, maxw, lh=1.1, balance=True, bind_short=True):
    toks = _tokens(segments)
    # unidades: cada unidade = lista de tokens que não podem quebrar entre si
    units = []
    for t in toks:
        w, st, gid, glue = t
        if w == '\n':
            units.append('\n'); continue
        if glue and units and units[-1] != '\n':
            units[-1].append((w, st, gid, True))
        else:
            units.append([(w, st, gid, False)])
    if bind_short:
        merged = []
        i = 0
        while i < len(units):
            u = units[i]
            if u != '\n' and i + 1 < len(units) and units[i + 1] != '\n' and \
               u[-1][0].lower().strip('"“(') in SHORT and len(u) == 1:
                nxt = units[i + 1]
                merged.append(u + [(nxt[0][0], nxt[0][1], nxt[0][2], False)] + nxt[1:])
                # marca separação por espaço com flag False (espaço) já é o default
                i += 2
                continue
            merged.append(u); i += 1
        units = merged

    def unit_w(u):
        x = 0
        for k, (w, st, gid, glue) in enumerate(u):
            if k > 0 and not glue: x += text_w(' ', st)
            x += text_w(w, st)
        return x

    def wrap(width):
        lines, cur, curw = [], [], 0
        for u in units:
            if u == '\n':
                lines.append(cur); cur, curw = [], 0; continue
            uw = unit_w(u)
            sp = text_w(' ', u[0][1]) if cur else 0
            if cur and curw + sp + uw > width:
                lines.append(cur); cur, curw = [u], uw
            else:
                cur.append(u); curw += sp + uw
        lines.append(cur)
        return lines

    lines = wrap(maxw)
    if balance:
        n = len(lines)
        def cost(ls, width):
            ws = [unit_w_line(l, unit_w) for l in ls]
            mx = max(ws)
            c = sum((mx - w) ** 2 for w in ws[:-1])
            if len(ws) > 1 and ws[-1] < mx * 0.4: c += (mx * 0.4 - ws[-1]) ** 2 * 3
            if len(ws) > 1 and ws[0] < mx * 0.55: c += (mx * 0.55 - ws[0]) ** 2 * 3
            return c + (maxw - width) * 2  # leve preferência por linhas largas
        best, bc = lines, cost(lines, maxw)
        wdt = maxw - 8
        while wdt > maxw * 0.5:
            l2 = wrap(wdt)
            if len(l2) == n:
                c = cost(l2, wdt)
                if c < bc: best, bc = l2, c
            elif len(l2) > n:
                break
            wdt -= 8
        lines = best
    # posiciona
    out = []
    y = 0
    for li, line in enumerate(lines):
        maxsize = max([u[0][1].size for u in line] or [segments[0][1].size])
        asc = max([u[0][1].f.getmetrics()[0] / S for u in line] or [segments[0][1].f.getmetrics()[0] / S])
        if li == 0:
            y = asc
        else:
            y += maxsize * lh
        x = 0
        items = []
        pg = None
        for ui, u in enumerate(line):
            if ui > 0: x += text_w(' ', u[0][1])
            for k, (w, st, gid, glue) in enumerate(u):
                if k > 0 and not glue: x += text_w(' ', st)
                if pg is not None and pg[0] != gid:
                    x += getattr(pg[1], 'padr', 0) + getattr(st, 'padl', 0)
                pg = (gid, st)
                ww = text_w(w, st)
                items.append((x, w, st, gid, ww))
                x += ww
        out.append({'y': y, 'w': x, 'items': items, 'size': maxsize})
    return out

def unit_w_line(line, unit_w):
    x = 0
    for i, u in enumerate(line):
        if i > 0: x += text_w(' ', u[0][1])
        x += unit_w(u)
    return x

class Slide:
    def __init__(self, bg, name):
        self.bg = bg
        self.name = name
        self.im = Image.new('RGBA', (W * S, H * S), hexc(bg) if isinstance(bg, str) else bg)
        self.d = ImageDraw.Draw(self.im)
        self.boxes = []  # (label, x0, y0, x1, y1)
        self.rng = random.Random(hash(name) & 0xffff)

    # ---- registro ----
    def reg(self, label, x0, y0, x1, y1):
        self.boxes.append((label, x0, y0, x1, y1))

    def check(self):
        probs = []
        for (lb, x0, y0, x1, y1) in self.boxes:
            if lb.startswith('~'): continue
            if x0 < MARGIN_X - 0.5 or x1 > W - MARGIN_X + 0.5 or y0 < MARGIN_Y or y1 > H - MARGIN_Y:
                probs.append(f'MARGEM {lb}: ({x0:.0f},{y0:.0f})-({x1:.0f},{y1:.0f})')
        bx = [b for b in self.boxes if not b[0].startswith('~')]
        for i in range(len(bx)):
            for j in range(i + 1, len(bx)):
                a, b = bx[i], bx[j]
                if a[0].split('#')[0] == b[0].split('#')[0]:
                    continue  # linhas do mesmo bloco
                if a[1] < b[3] - 1 and b[1] < a[3] - 1 and a[2] < b[4] - 1 and b[2] < a[4] - 1:
                    probs.append(f'COLISAO {a[0]} x {b[0]}')
        return probs

    # ---- desenho básico ----
    def P(self, *xy):
        return [v * S for v in xy]

    def rect(self, x0, y0, x1, y1, fill=None, outline=None, width=1, label=None):
        self.d.rectangle(self.P(x0, y0, x1 - 1 / S, y1 - 1 / S), fill=hexc(fill) if isinstance(fill, str) else fill,
                         outline=hexc(outline) if isinstance(outline, str) else outline, width=int(width * S))
        if label: self.reg(label, x0, y0, x1, y1)

    def line(self, pts, fill, width, label=None):
        c = hexc(fill) if isinstance(fill, str) else fill
        self.d.line([v * S for p in pts for v in p], fill=c, width=max(1, int(round(width * S))))
        if label:
            xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
            self.reg(label, min(xs), min(ys), max(xs), max(ys))

    def poly(self, pts, fill=None, outline=None, width=1):
        self.d.polygon([v * S for p in pts for v in p], fill=hexc(fill) if isinstance(fill, str) else fill,
                       outline=hexc(outline) if isinstance(outline, str) else outline, width=int(width * S))

    def ellipse(self, x0, y0, x1, y1, fill=None, outline=None, width=1):
        self.d.ellipse(self.P(x0, y0, x1, y1), fill=hexc(fill) if isinstance(fill, str) else fill,
                       outline=hexc(outline) if isinstance(outline, str) else outline, width=int(width * S))

    # traço à mão: linha com tremor leve e pontas arredondadas
    def hand_stroke(self, pts, color, width, jitter=1.2, seed=0):
        rng = random.Random(seed)
        dense = []
        for (a, b) in zip(pts, pts[1:]):
            n = max(2, int(math.dist(a, b) / 18))
            for k in range(n):
                t = k / n
                dense.append((a[0] + (b[0] - a[0]) * t + rng.uniform(-jitter, jitter) * 0.4,
                              a[1] + (b[1] - a[1]) * t + rng.uniform(-jitter, jitter)))
        dense.append(pts[-1])
        c = hexc(color) if isinstance(color, str) else color
        wpx = width * S
        for (a, b) in zip(dense, dense[1:]):
            self.d.line([a[0] * S, a[1] * S, b[0] * S, b[1] * S], fill=c, width=int(wpx))
        for p in dense:
            r = wpx / 2
            self.d.ellipse([p[0] * S - r, p[1] * S - r, p[0] * S + r, p[1] * S + r], fill=c)

    def marker_band(self, x0, y0, x1, y1, color, angle=-1.2, seed=0):
        """marca-texto: faixa levemente torta, cantos irregulares."""
        rng = random.Random(seed)
        cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
        pts = [(x0 + rng.uniform(-3, 2), y0 + rng.uniform(-2, 3)), (x1 + rng.uniform(-2, 4), y0 + rng.uniform(-3, 2)),
               (x1 + rng.uniform(-4, 2), y1 + rng.uniform(-2, 3)), (x0 + rng.uniform(-2, 3), y1 + rng.uniform(-3, 2))]
        a = math.radians(angle)
        rp = [(cx + (px - cx) * math.cos(a) - (py - cy) * math.sin(a), cy + (px - cx) * math.sin(a) + (py - cy) * math.cos(a)) for px, py in pts]
        self.poly(rp, fill=color)

    # ---- texto ----
    def draw_word(self, x, ybase, w, st):
        w = w.replace('\u00a0', ' ')
        f = st.f
        c = hexc(st.fill) if isinstance(st.fill, str) else st.fill
        if abs(st.track) < 0.01:
            self.d.text((x * S, ybase * S), w, font=f, fill=c, anchor='ls')
            return
        for i, ch in enumerate(w):
            xi = x + f.getlength(w[:i]) / S + i * st.track
            self.d.text((xi * S, ybase * S), ch, font=f, fill=c, anchor='ls')

    def text(self, segments, x, y, maxw, lh=1.1, align='left', label='txt', balance=True, valign='top', bind_short=True):
        """y = topo da caixa (topo do ascendente da 1ª linha). Retorna (y_fim, linhas)."""
        if isinstance(segments, tuple): segments = [segments]
        lines = layout(segments, maxw, lh, balance, bind_short)
        # caixa
        last = lines[-1]
        desc = max(it[2].f.getmetrics()[1] / S for it in last['items']) if last['items'] else 0
        total_h = last['y'] + desc * 0.6
        if valign == 'bottom': y = y - total_h
        elif valign == 'middle': y = y - total_h / 2
        # decorações por grupo, por linha
        under, over = [], []
        for li, ln in enumerate(lines):
            ox = x if align == 'left' else (x + (maxw - ln['w']) / 2 if align == 'center' else x + maxw - ln['w'])
            ln['ox'] = ox
            groups = {}
            for (ix, w, st, gid, ww) in ln['items']:
                if st.deco:
                    g = groups.setdefault(gid, [ix, ix + ww, st])
                    g[0] = min(g[0], ix); g[1] = max(g[1], ix + ww)
            for gid, (gx0, gx1, st) in groups.items():
                yb = y + ln['y']
                asc = st.f.getmetrics()[0] / S
                if st.deco == 'mark':
                    under.append(('mark', ox + gx0, ox + gx1, yb, st, li * 10 + gid))
                else:
                    over.append((st.deco, ox + gx0, ox + gx1, yb, st, li * 10 + gid))
        for (k, x0, x1, yb, st, sd) in under:
            sz = st.size
            self.marker_band(x0 - sz * 0.06, yb - sz * 0.62, x1 + sz * 0.06, yb + sz * 0.1, st.deco_color, seed=sd)
        for li, ln in enumerate(lines):
            yb = y + ln['y']
            xs = []
            for (ix, w, st, gid, ww) in ln['items']:
                self.draw_word(ln['ox'] + ix, yb, w, st)
            asc = max(it[2].f.getmetrics()[0] / S for it in ln['items']) if ln['items'] else 0
            capish = max(it[2].size for it in ln['items']) * 0.74 if ln['items'] else 0
            self.reg(f'{label}#{li}', ln['ox'], yb - capish, ln['ox'] + ln['w'], yb + ln['size'] * 0.2)
        for (k, x0, x1, yb, st, sd) in over:
            sz = st.size
            if k == 'strike':
                ym = yb - sz * 0.3
                self.hand_stroke([(x0 - sz * 0.05, ym + sz * 0.04), (x1 + sz * 0.05, ym - sz * 0.05)], st.deco_color, max(4, sz * 0.075), seed=sd)
            elif k == 'underline':
                yu = yb + sz * 0.13
                self.hand_stroke([(x0 - 4, yu + 2), ((x0 + x1) / 2, yu - 1), (x1 + 6, yu + 3)], st.deco_color, max(3, sz * 0.06), seed=sd)
            elif k == 'circle':
                self.hand_ellipse(x0 - sz * 0.14, yb - sz * 0.9, x1 + sz * 0.16, yb + sz * 0.3, st.deco_color, max(3, sz * 0.05), seed=sd)
        return y + total_h, lines

    def hand_ellipse(self, x0, y0, x1, y1, color, width, seed=0):
        rng = random.Random(seed)
        cx, cy, rx, ry = (x0 + x1) / 2, (y0 + y1) / 2, (x1 - x0) / 2, (y1 - y0) / 2
        pts = []
        start = -0.5
        for k in range(0, 76):
            t = start + k / 72 * 2 * math.pi * 1.04
            grow = 1 + 0.035 * (k / 76)
            pts.append((cx + rx * grow * math.cos(t) + rng.uniform(-0.6, 0.6), cy + ry * grow * math.sin(t) * (1 - 0.02 * k / 76) + rng.uniform(-0.6, 0.6)))
        self.hand_stroke(pts, color, width, jitter=0.3, seed=seed)

    def rotated_text(self, txt, st, cx, cy, angle, label='hand'):
        f = st.f
        tw = int(f.getlength(txt)) + 40 * S
        asc, desc = f.getmetrics()
        th = asc + desc + 40 * S
        layer = Image.new('RGBA', (tw, th), (0, 0, 0, 0))
        ImageDraw.Draw(layer).text((20 * S, 20 * S + asc), txt, font=f, fill=hexc(st.fill), anchor='ls')
        layer = layer.crop(layer.getbbox())
        r = layer.rotate(angle, resample=Image.BICUBIC, expand=True)
        px, py = int(cx * S - r.width / 2), int(cy * S - r.height / 2)
        self.im.alpha_composite(r, (px, py))
        self.reg(label, px / S, py / S, (px + r.width) / S, (py + r.height) / S)
        return (px / S, py / S, (px + r.width) / S, (py + r.height) / S)

    def paste(self, img, x, y, w=None, h=None, label='img'):
        if w and h: im = img.resize((int(w * S), int(h * S)), Image.LANCZOS)
        elif w: im = img.resize((int(w * S), int(img.height * w * S / img.width)), Image.LANCZOS)
        elif h: im = img.resize((int(img.width * h * S / img.height), int(h * S)), Image.LANCZOS)
        else: im = img
        im = im.convert('RGBA')
        self.im.alpha_composite(im, (int(x * S), int(y * S)))
        self.reg(label, x, y, x + im.width / S, y + im.height / S)
        return (x, y, x + im.width / S, y + im.height / S)

    def shadow(self, x0, y0, x1, y1, color=(0, 0, 0, 120), blur=24, off=(0, 14)):
        layer = Image.new('RGBA', self.im.size, (0, 0, 0, 0))
        ImageDraw.Draw(layer).rectangle([(x0 + off[0]) * S, (y0 + off[1]) * S, (x1 + off[0]) * S, (y1 + off[1]) * S], fill=color)
        layer = layer.filter(ImageFilter.GaussianBlur(blur * S))
        self.im.alpha_composite(layer)

    def save(self, path, grain=6.0):
        probs = self.check()
        im = self.im.convert('RGB').resize((W, H), Image.LANCZOS)
        if grain:
            a = np.asarray(im).astype(np.float32)
            rng = np.random.default_rng(abs(hash(self.name)) % (2 ** 32))
            n = rng.normal(0, grain, (H, W, 1))
            a = np.clip(a + n, 0, 255).astype(np.uint8)
            im = Image.fromarray(a)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        im.save(path, optimize=True)
        print(os.path.basename(os.path.dirname(path)) + '/' + os.path.basename(path), 'OK' if not probs else probs)
        return probs
