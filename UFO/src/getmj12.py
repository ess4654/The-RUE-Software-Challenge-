import json, urllib.request, urllib.parse

API = 'https://commons.wikimedia.org/w/api.php'
UA = 'UfologyBookBuild/1.0 (educational book figure sourcing)'

def api(params):
    url = API + '?' + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={'User-Agent': UA})
    return json.load(urllib.request.urlopen(req, timeout=60))

queries = [
    'Roscoe Hillenkoetter',
    'Nathan Twining',
    'Hoyt Vandenberg',
    'Robert M. Montague general',
    'Sidney Souers',
    'James Forrestal',
    'Gordon Gray politician',
    'Vannevar Bush',
    'Detlev Bronk',
    'Jerome Clarke Hunsaker',
    'Donald Howard Menzel',
    'Lloyd Berkner',
]

for q in queries:
    print('=' * 70)
    print('QUERY:', q)
    try:
        res = api({
            'action': 'query', 'generator': 'search',
            'gsrsearch': q, 'gsrnamespace': '6',
            'gsrlimit': '12', 'prop': 'imageinfo', 'iiprop': 'url|extmetadata|size',
            'format': 'json',
        })
    except Exception as e:
        print('ERR', e)
        continue
    pages = res.get('query', {}).get('pages', {})
    for p in pages.values():
        ii = p['imageinfo'][0]
        em = ii.get('extmetadata', {})
        lic = em.get('LicenseShortName', {}).get('value', '?')
        art = em.get('Artist', {}).get('value', '?')
        import re
        art = re.sub('<[^>]+>', '', art)[:70]
        print('%-62s | %-18s | %5sx%-5s | %s' % (p['title'][:62], lic[:18], ii.get('width'), ii.get('height'), art))
        print('    ', ii['url'])
