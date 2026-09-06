#!/usr/bin/env python3
# Label every chapter/section, convert hardcoded Chapter~N / Section~N.M refs
# to \ref{}, then reorder the chapter list in main.tex.
import re, os, shutil, sys

D = '/nfs/104328877/temp/ufology'

# printed chapter number (CURRENT build) -> source file
CUR = {1:'ch01',2:'ch02',3:'ch04',4:'ch03',5:'ch05',6:'ch16',7:'ch06',8:'ch07',
       9:'ch08',10:'ch09',11:'ch10',12:'ch11',13:'ch12',14:'ch13',15:'ch14',
       16:'ch15',17:'ch17',18:'ch18',19:'ch19',20:'ch20'}

# author's requested order: new printed number -> source file
NEW = ['ch01','ch02','ch04','ch14','ch12','ch03','ch05','ch16','ch06','ch07',
       'ch08','ch09','ch10','ch11','ch13','ch15','ch17','ch18','ch19','ch20']

CHFILES = ['ch%02d' % i for i in range(1,21)]

def slug(t):
    t = re.sub(r'\\[a-zA-Z]+', ' ', t)
    t = re.sub(r'[^A-Za-z0-9 ]', ' ', t)
    w = [x.lower() for x in t.split()]
    stop = {'the','a','an','of','and','is','to','in','for','on','from','it','its','by'}
    w = [x for x in w if x not in stop] or w
    return ''.join(w)[:24] or 'x'

used = set()
for f in CHFILES:
    for m in re.finditer(r'\\label\{([^}]*)\}', open(os.path.join(D,f+'.tex')).read()):
        used.add(m.group(1))

HEAD = re.compile(r'^\\(chapter|section)\{((?:[^{}]|\{[^{}]*\})*)\}(\\label\{([^}]*)\})?',
                  re.M)

chlab = {}          # file -> chapter label
seclab = {}         # (file, 1-based section index) -> label
edits = {}          # file -> new text

for f in CHFILES:
    p = os.path.join(D, f+'.tex')
    txt = open(p).read()
    out, pos, idx = [], 0, 0
    for m in HEAD.finditer(txt):
        kind, title, lab = m.group(1), m.group(2), m.group(4)
        if lab is None:
            base = ('ch:' if kind == 'chapter' else 'sec:') + slug(title)
            lab, n = base, 2
            while lab in used:
                lab = base + str(n); n += 1
            used.add(lab)
            out.append(txt[pos:m.end()])
            out.append('\\label{%s}' % lab)
            pos = m.end()
        if kind == 'chapter':
            chlab[f] = lab
        else:
            idx += 1
            seclab[(f, idx)] = lab
    out.append(txt[pos:])
    edits[f] = ''.join(out)
    print(f, 'chapter label', chlab[f], '| sections', idx)

# ---- reference rewriting -------------------------------------------------
RE_REF = re.compile(r'\b(Chapters?|Sections?)([~ ])(\d{1,2})(?:\.(\d{1,2}))?\b')
bad = []
count = 0

def fix(text, fname):
    global count
    def rep(m):
        global count
        word, sep, cn, sn = m.group(1), m.group(2), int(m.group(3)), m.group(4)
        if cn not in CUR:
            bad.append((fname, m.group(0), 'chapter out of range')); return m.group(0)
        src = CUR[cn]
        if sn is None:
            if word.startswith('Section'):
                bad.append((fname, m.group(0), 'section without number')); return m.group(0)
            lab = chlab[src]
        else:
            key = (src, int(sn))
            if key not in seclab:
                bad.append((fname, m.group(0), 'no such section')); return m.group(0)
            lab = seclab[key]
        count += 1
        return '%s~\\ref{%s}' % (word, lab)
    return RE_REF.sub(rep, text)

for f in CHFILES:
    edits[f] = fix(edits[f], f)
for f in ['back_glossary','back_author','front_preface','conclusion','back_references']:
    edits[f] = fix(open(os.path.join(D,f+'.tex')).read(), f)

if bad:
    print('UNRESOLVED:')
    for b in bad: print('   ', b)

for f, t in edits.items():
    p = os.path.join(D, f+'.tex')
    if not os.path.exists(p+'.bak'):
        shutil.copy(p, p+'.bak')
    open(p,'w').write(t)
print('refs converted:', count)

# ---- reorder main.tex ---------------------------------------------------
mp = os.path.join(D,'main.tex')
if not os.path.exists(mp+'.bak'):
    shutil.copy(mp, mp+'.bak')
main = open(mp).read()
block = re.compile(r'(\\chapterplate\{pl_ch\d\d\.jpg\}\s*\n\\input\{ch\d\d\}\s*\n'
                   r'(?:\\addtocontents\{toc\}\{\\protect\\newpage\}\s*\n)?)+')
m = block.search(main)
assert m, 'chapter block not found'
new = []
for i, f in enumerate(NEW, 1):
    new.append('\\chapterplate{pl_%s.jpg}\n\\input{%s}\n' % (f, f))
    if i == 2:
        new.append('\\addtocontents{toc}{\\protect\\newpage}\n')
main = main[:m.start()] + ''.join(new) + main[m.end():]
open(mp,'w').write(main)
print('main.tex reordered; block replaced', m.start(), m.end())
