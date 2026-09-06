import json,urllib.request,urllib.parse,time,re,os
UA={'User-Agent':'UfologyBookBuild/1.0 (book build)'}
API='https://commons.wikimedia.org/w/api.php'
titles={
 'uf_mj12_hillenkoetter':'File:Roscoe H. Hillenkoetter (1957).jpg',
 'uf_mj12_forrestal':'File:James Forrestal - SecOfDef.jpg',
 'uf_mj12_bronk':'File:Detlev Wulf Bronk.jpg',
 'uf_mj12_montague':'File:Robert Miller Montague.jpg',
}
info=json.load(open('temp_mj12/info.json'))
q=urllib.parse.urlencode({'action':'query','titles':'|'.join(titles.values()),'prop':'imageinfo','iiprop':'url|extmetadata|size','iiurlwidth':'700','format':'json'})
data=json.load(urllib.request.urlopen(urllib.request.Request(API+'?'+q,headers=UA),timeout=90))
pages={p.get('title'):p for p in data['query']['pages'].values()}
for name,t in titles.items():
    if os.path.exists('temp_mj12/%s.jpg'%name) and os.path.getsize('temp_mj12/%s.jpg'%name)>5000:
        print('have',name); continue
    p=pages.get(t)
    if not p or 'imageinfo' not in p:
        print('MISSING',t); continue
    ii=p['imageinfo'][0]; em=ii.get('extmetadata',{})
    url=ii.get('thumburl') or ii['url']
    lic=em.get('LicenseShortName',{}).get('value','?')
    art=re.sub('<[^>]+>','',em.get('Artist',{}).get('value','?')).strip().replace('\n',' ')
    info[name]={'lic':lic,'artist':art,'file':p['title'],'page':ii.get('descriptionurl')}
    for attempt in range(6):
        try:
            d=urllib.request.urlopen(urllib.request.Request(url,headers=UA),timeout=120).read()
            open('temp_mj12/%s.jpg'%name,'wb').write(d)
            print('OK  %-24s %7d  %-14s %s'%(name,len(d),lic[:14],art[:40]))
            break
        except Exception as e:
            print('retry',name,str(e)[:40]); time.sleep(15)
    time.sleep(10)
json.dump(info,open('temp_mj12/info.json','w'),indent=1)
