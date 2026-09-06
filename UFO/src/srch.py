import json, urllib.request, urllib.parse, sys

API = 'https://commons.wikimedia.org/w/api.php'
UA = 'UfologyBookBuild/1.0 (educational book figure sourcing)'

def api(params):
    url = API + '?' + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={'User-Agent': UA})
    return json.load(urllib.request.urlopen(req, timeout=90))

queries = sys.argv[1:]
for q in queries:
    print('=' * 8, q)
    try:
        res = api({
            'action': 'query', 'generator': 'search',
            'gsrsearch': q, 'gsrnamespace': '6',
            'gsrlimit': '14', 'prop': 'imageinfo',
            'iiprop': 'url|extmetadata|size', 'format': 'json',
        })
    except Exception as e:
        print('ERR', e); continue
    pages = res.get('query', {}).get('pages', {})
    for p in pages.values():
        ii = p['imageinfo'][0]
        em = ii.get('extmetadata', {})
        lic = em.get('LicenseShortName', {}).get('value', '?')
        print('%-58s | %-22s | %sx%s | %s' % (p['title'][:58], lic[:22], ii.get('width'), ii.get('height'), ii['url']))
