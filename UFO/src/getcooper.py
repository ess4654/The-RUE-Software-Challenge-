import json, urllib.request, urllib.parse

API = 'https://commons.wikimedia.org/w/api.php'
UA = 'UfologyBookBuild/1.0 (educational book figure sourcing)'

def api(params):
    url = API + '?' + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={'User-Agent': UA})
    return json.load(urllib.request.urlopen(req, timeout=60))

res = api({
    'action': 'query', 'generator': 'search',
    'gsrsearch': 'Gordon Cooper astronaut', 'gsrnamespace': '6',
    'gsrlimit': '30', 'prop': 'imageinfo', 'iiprop': 'url|extmetadata',
    'format': 'json',
})
for p in res.get('query', {}).get('pages', {}).values():
    ii = p['imageinfo'][0]
    em = ii.get('extmetadata', {})
    lic = em.get('LicenseShortName', {}).get('value', '?')
    print(p['title'], '||', lic, '||', ii['url'])
