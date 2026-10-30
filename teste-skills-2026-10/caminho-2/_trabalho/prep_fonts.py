# Gera instâncias estáticas das fontes variáveis do Livra (PIL sem raqm lida mal com eixos).
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont
import os
D = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fonts')
OUT = os.path.join(D, 'static')
jobs = {
  'Bricolage-ExtraBold.ttf': ('Bricolage.ttf', dict(opsz=96, wght=800, wdth=100)),
  'Bricolage-Bold.ttf': ('Bricolage.ttf', dict(opsz=72, wght=700, wdth=100)),
  'Bricolage-SemiBold.ttf': ('Bricolage.ttf', dict(opsz=36, wght=600, wdth=100)),
  'Bricolage-Medium.ttf': ('Bricolage.ttf', dict(opsz=28, wght=500, wdth=100)),
  'Bricolage-CondBold.ttf': ('Bricolage.ttf', dict(opsz=96, wght=800, wdth=75)),
  'Fraunces-Italic-Display.ttf': ('Fraunces-Italic.ttf', dict(opsz=144, wght=500, SOFT=50, WONK=1)),
  'Fraunces-Italic-Text.ttf': ('Fraunces-Italic.ttf', dict(opsz=48, wght=450, SOFT=50, WONK=1)),
  'Fraunces-Italic-Light.ttf': ('Fraunces-Italic.ttf', dict(opsz=144, wght=300, SOFT=100, WONK=1)),
  'Fraunces-Text.ttf': ('Fraunces.ttf', dict(opsz=36, wght=420, SOFT=50, WONK=0)),
}
for out, (src, loc) in jobs.items():
    f = TTFont(os.path.join(D, src))
    inst = instantiateVariableFont(f, loc)
    inst.save(os.path.join(OUT, out)); print('ok', out)
