import json,urllib.request,urllib.parse,re,sys
UA={'User-Agent':'UfologyBookBuild/1.0'}
API='https://commons.wikimedia.org/w/api.php'
ts=['File:Bill Lear.jpg','File:Learwilliam.jpg','File:Gates Learjet 23 (10438289895).jpg','File:Arkansas Air '+chr(38)+' Military Museum May 2017 17 (1964 Learjet 23).jpg','File:Warnhinweis und Sicherheitspersonal an der Groom Lake Road 07.2008.jpg','File:Extraterrestrial Highway sign (Route 375, Nevada, USA).jpg']
q=urllib.parse.urlencode({'action':'query','titles':'|'.join(ts),'prop':'imageinfo','iiprop':'url|extmetadata|size','iiurlwidth':'900','format':'json'})
d=json.load(urllib.request.urlopen(urllib.request.Request(API+'?'+q,headers=UA),timeout=60))
for p in d['query']['pages'].values():
    if 'imageinfo' not in p:
        print('MISSING',p['title']); continue
    ii=p['imageinfo'][0]; em=ii.get('extmetadata',{})
    art=re.sub('<[^>]+>','',em.get('Artist',{}).get('value','?')).strip().replace('\n',' ')
    print(p['title'],'|',em.get('LicenseShortName',{}).get('value','?'),'|',art[:70],'|',ii['width'],ii['height'])
    print('   ',ii.get('thumburl'))
