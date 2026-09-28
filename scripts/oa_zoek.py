import sys,json,subprocess,urllib.parse
sys.stdout.reconfigure(encoding='utf-8')
for q in sys.argv[1:]:
    u="https://api.openarch.nl/1.0/records/search.json?"+urllib.parse.urlencode({'name':q,'lang':'nl','number_show':100})
    d=json.loads(subprocess.run(['curl','-s',u],capture_output=True).stdout.decode('utf-8','replace'))
    print('#####',q,'TOTAL',d['response']['number_found'])
    for r in d['response'].get('docs',[]):
        e=r.get('eventdate') or {}
        print(f"{e.get('year','')}-{e.get('month','')}-{e.get('day','')} | {r.get('eventtype')} | {r.get('personname')} ({r.get('relationtype')}) | {','.join(r.get('eventplace') or [])} | {r.get('url','').split('/')[-1]}")
