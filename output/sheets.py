import sys, glob
from PIL import Image
fs = sorted(glob.glob('render/s-*.png'))
sel = [int(x) for x in sys.argv[1:]] or list(range(1, len(fs)+1))
for k in range(0, len(sel), 4):
    grp = sel[k:k+4]; ims = [Image.open(fs[i-1]) for i in grp]
    w, h = ims[0].size; sheet = Image.new('RGB', (w*2+10, h*2+10), 'white')
    for j, im in enumerate(ims): sheet.paste(im, ((j % 2)*(w+10), (j//2)*(h+10)))
    sheet.save('render/sheet-%02d.png' % grp[0])
    print('render/sheet-%02d.png' % grp[0], grp)
