import sys,json,subprocess,urllib.parse
sys.stdout.reconfigure(encoding='utf-8')
for q in sys.argv[1:]:
    u="https://commons.wikimedia.org/w/api.php?"+urllib.parse.urlencode({'action':'query','list':'search','srsearch':q,'srnamespace':6,'srlimit':12,'format':'json'})
    d=json.loads(subprocess.run(['curl','-s','-A','hillen-familie-research/1.0 (peotjmsa@gmail.com)',u],capture_output=True).stdout)
    print('####',q)
    for r in d['query']['search']: print('  ',r['title'])
