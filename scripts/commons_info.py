import sys,json,subprocess,urllib.parse,re
sys.stdout.reconfigure(encoding='utf-8')
titles='|'.join(sys.argv[1:])
u="https://commons.wikimedia.org/w/api.php?"+urllib.parse.urlencode({'action':'query','prop':'imageinfo','iiprop':'url|extmetadata|size','iiurlwidth':1600,'titles':titles,'format':'json'})
d=json.loads(subprocess.run(['curl','-s','-A','hillen-familie-research/1.0 (peotjmsa@gmail.com)',u],capture_output=True).stdout)
for p in d['query']['pages'].values():
    ii=p.get('imageinfo',[{}])[0]; m=ii.get('extmetadata',{})
    g=lambda k: re.sub('<[^>]+>','',m.get(k,{}).get('value',''))[:160]
    print(p['title'],'|',ii.get('width'),'x',ii.get('height'),'|',g('LicenseShortName'),'|',g('Artist'),'|',g('ImageDescription'),'|',g('DateTimeOriginal'),'\n   ',ii.get('thumburl'),'\n   ',ii.get('descriptionurl'))
