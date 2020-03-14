import tools
import json

infos = set([p["info"] for p in tools.mapping_list])
s = {}
for info in infos:
    s[info] = False
with open("DB.json", 'w', encoding='utf8') as f:
    json.dump(s, f, ensure_ascii=False)
