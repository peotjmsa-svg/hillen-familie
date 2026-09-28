for id in "$@"; do a=${id%%:*}; i=${id#*:}; echo "=== $id"; curl -s "https://api.openarch.nl/1.0/records/show.json?archive=$a&identifier=$i&lang=nl" | python -c "
import sys,re;sys.stdout.reconfigure(encoding='utf-8');t=sys.stdin.read();t=re.sub(r'a2a_','',t)
out=[]
for m in re.finditer(r'\"(PersonNameFirstName|PersonNamePrefixLastName|PersonNameLastName|RelationType|Profession|Place|Year|Month|Day|PersonAgeYears|PersonAgeLiteral|EventType|Value)\":\"([^\"]*)\"',t):
  if 'http' in m.group(2) or 'A2A' in m.group(2): continue
  out.append(m.group(1).replace('PersonName','')+'='+m.group(2))
print(' | '.join(out))
"; done
