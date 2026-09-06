import json,urllib.request,urllib.parse,time,re,os
UA={'User-Agent':'UfologyBookBuild/1.0 (book build)'}
API='https://commons.wikimedia.org/w/api.php'
AMP=chr(38)
titles={
 'uf_mj12_hillenkoetter':'File:Roscoe H. Hillenkoetter (1957).jpg',
 'uf_mj12_twining':'File:Gen Nathan F. Twining, black and white portrait.jpg',
 'uf_mj12_vandenberg':'File:Hoyt S Vandenberg.jpg',
 'uf_mj12_montague':'File:Robert Miller Montague (1899–1958) in the 1920 Howitzer.jpg',
 'uf_mj12_souers':'File:Sidney W. Souers.jpg',
 'uf_mj12_forrestal':'File:James Forrestal - SecOfDef.jpg',
 'uf_mj12_gray':'File:Gordon Gray - Project Gutenberg etext 20587.jpg',
 'uf_mj12_bush':'File:Vannevar Bush, 1938, Harris '+AMP+' Ewing (cropped).jpg',
 'uf_mj12_bronk':'File:Detlev Wulf Bronk.jpg',
 'uf_mj12_hunsaker':'File:Jerome Clarke Hunsaker (cropped).jpg',
 'uf_mj12_menzel':'File:Donald Howard Menzel Portrait.jpg',
 'uf_mj12_berkner':'File:Lloyd Berkner.jpg',
}
os.makedirs('temp_mj12',exist_ok=True)
info={}
q=urllib.parse.urlencode({'action':'query','titles':'|'.join(titles.values()),'prop':'imageinfo','iiprop':'url|extmetadata|size','iiurlwidth':'900','format':'json'})
data=json.load(urllib.request.urlopen(urllib.request.Request(API+'?'+q,headers=UA),timeout=90))
pages={p.get('title'):p for p in data['query']['pages'].values()}
for name,t in titles.items():
    p=pages.get(t)
    if not p or 'imageinfo' not in p:
        print('MISSING',t); continue
    ii=p['imageinfo'][0]; em=ii.get('extmetadata',{})
    url=ii.get('thumburl') or ii['url']
    lic=em.get('LicenseShortName',{}).get('value','?')
    art=re.sub('<[^>]+>','',em.get('Artist',{}).get('value','?')).strip().replace('\n',' ')
    info[name]={'lic':lic,'artist':art,'file':p['title'],'page':ii.get('descriptionurl')}
    for attempt in range(4):
        try:
            d=urllib.request.urlopen(urllib.request.Request(url,headers=UA),timeout=120).read()
            open('temp_mj12/%s.jpg'%name,'wb').write(d)
            print('OK  %-24s %7d  %-14s %s'%(name,len(d),lic[:14],art[:40]))
            break
        except Exception as e:
            print('retry',name,e); time.sleep(6)
    time.sleep(2)
json.dump(info,open('temp_mj12/info.json','w'),indent=1)
