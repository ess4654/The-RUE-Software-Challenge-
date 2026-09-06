import re,sys,collections,subprocess
xml=subprocess.run(["pdftotext","-bbox-layout","main.pdf","-"],capture_output=True,text=True).stdout
pages=re.split(r'<page ',xml)[1:]
ignore=set([53,55,68,69,70,71,72,73,74,75]+list(range(194,201))+list(range(348,362)))
for i,p in enumerate(pages,1):
    if i in ignore: continue
    xs=[round(float(m)) for m in re.findall(r'<line xMin="([\d.]+)"',p)]
    if len(xs)<8: continue
    modal,cnt=collections.Counter(xs).most_common(1)[0]
    base=94 if i%2==1 else 104
    if modal-base>60 and cnt>0.5*len(xs):
        print(i,"folio",i-18,"modal",modal,"lines",cnt,"/",len(xs))
