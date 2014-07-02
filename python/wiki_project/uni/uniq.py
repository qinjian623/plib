import json

file_path = "/home/qin/output.wiki.json"
json_text = ""

table = {}
for line in open(file_path):
    if line[0] == '}':
        json_text += line.strip()
        jo = json.loads(json_text)
        title = jo['title']
        if title in table:
            continue
        else:
            print json.dumps(jo, sort_keys=True,
                             indent=4, separators=(',', ': '),
                             ensure_ascii=False).encode("utf-8")
            table[title] = 1
        json_text = ""
    else:
        json_text += line.strip()
