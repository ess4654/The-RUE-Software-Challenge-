import re, glob, os, sys
os.chdir('/nfs/104328877/temp/ufology')
BAD = ('\\figplace', '\\pullquote', '\\begin', '\\end', '\\item', '\\section', '\\subsection', '\\chapter', '\\gap', '\\needspace')
files = sys.argv[1:] or sorted(glob.glob('ch*.tex'))
for f in files:
    lines = open(f).read().split('\n')
    print('#####', f)
    cur = 'PRE'
    i = 0
    n = len(lines)
    while i < n:
        ln = lines[i]
        m = re.match(r'\\(sub)?section\*?\{([^}]*)', ln)
        if m:
            cur = ('SUB ' if m.group(1) else 'SEC ') + m.group(2)
            print('  --', cur, f'(L{i+1})')
            i += 1
            continue
        if ln.strip() == '' or ln.lstrip().startswith('%'):
            i += 1
            continue
        start = i
        while i < n and lines[i].strip() != '':
            i += 1
        length = i - start
        first = lines[start].lstrip()
        if any(first.startswith(b) for b in BAD):
            print(f'     [skip L{start+1} len{length}] {first[:50]}')
            continue
        flag = 'OK ' if length >= 7 else '   '
        print(f'     {flag}L{start+1} len{length} :: {lines[start][:95]}')
