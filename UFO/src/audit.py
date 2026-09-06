import sys, re, fitz
doc = fitz.open(sys.argv[1])
LIMIT = 792 - 1.05 * 72          # 716.4 bottom of text block
FOOTTOP = 730.0                  # footer/folio ornament zone starts here
bad = []
for i, pg in enumerate(doc):
    hits = []
    def add(kind, y0, y1, label=''):
        if y0 >= FOOTTOP:            # pure footer ornament / folio
            return
        if y1 > LIMIT + 6:
            hits.append((kind, round(y1, 1), label))
    for b in pg.get_text('blocks'):
        t = b[4].strip()
        if not t:
            continue
        add('txt', b[1], b[3], t[:45].replace('\n', ' '))
    for d in pg.get_drawings():
        r = d['rect']
        if 4 < r.height < 700:
            add('draw', r.y0, r.y1)
    for im in pg.get_image_info():
        r = fitz.Rect(im['bbox'])
        if r.height < 700:
            add('img', r.y0, r.y1)
    if hits:
        bad.append((i + 1, hits))
print('pages with content past text block:', len(bad))
for p, hits in bad:
    mx = max(h[1] for h in hits)
    print(' pdf', p, 'folio', p - 18, 'maxbottom', mx, hits[:4])
