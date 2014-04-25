import json

s = json.dumps(json.load(open('test.json', 'r')), sort_keys=True, indent=4, separators=(',', ': '))


f = open('test.json', 'w')
f.write(s)