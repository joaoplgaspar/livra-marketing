import sys, os, glob
from PIL import Image
d = sys.argv[1]; out = sys.argv[2]; cols = int(sys.argv[3]) if len(sys.argv) > 3 else 4
fs = sorted(glob.glob(os.path.join(d, '[0-9][0-9].png')))
w, h = 360, 450
rows = (len(fs) + cols - 1) // cols
im = Image.new('RGB', (cols * (w + 12) + 12, rows * (h + 12) + 12), (90, 90, 90))
for i, f in enumerate(fs):
    im.paste(Image.open(f).resize((w, h), Image.LANCZOS), (12 + (i % cols) * (w + 12), 12 + (i // cols) * (h + 12)))
im.save(out)
