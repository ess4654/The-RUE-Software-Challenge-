import json,urllib.request,urllib.parse,time,re,os,sys
UA={'User-Agent':'UfologyBookBuild/1.0 (book build)'}
API='https://commons.wikimedia.org/w/api.php'
name=sys.argv[1]; t=sys.argv[2]; w=sys.argv[3] if len(sys.argv)>3 else '700'
info=json.load(open('temp_mj12/info.json'))
q=urllib.parse.urlencode({'action':'query','titles':t,'prop':'imageinfo','iiprop':'url|extmetadata|size','iiurlwidth':w,'format':'json'})
data=None
for a in range(6):
    try:
        data=json.load(urllib.request.urlopen(urllib.request.Request(API+'?'+q,headers=UA),timeout=60)); break
    except Exception as e:
        print('api retry',str(e)[:40]); time.sleep(20)
if data is None:
    print('APIFAIL',t); sys.exit(1)
p=list(data['query']['pages'].values())[0]
if 'imageinfo' not in p:
    print('MISSING',t); sys.exit(1)
ii=p['imageinfo'][0]; em=ii.get('extmetadata',{})
url=ii.get('thumburl') or ii['url']
lic=em.get('LicenseShortName',{}).get('value','?')
art=re.sub('<[^>]+>','',em.get('Artist',{}).get('value','?')).strip().replace('\n',' ')
for attempt in range(3):
    try:
        d=urllib.request.urlopen(urllib.request.Request(url,headers=UA),timeout=60).read()
        open('temp_mj12/%s.jpg'%name,'wb').write(d)
        info[name]={'lic':lic,'artist':art,'file':p['title'],'page':ii.get('descriptionurl')}
        json.dump(info,open('temp_mj12/info.json','w'),indent=1)
        print('OK %s %d %s | %s'%(name,len(d),lic,art[:50]))
        break
    except Exception as e:
        print('retry',str(e)[:50]); time.sleep(8)
