a, b, c = open('a').readlines(), open('b').readlines(), open('c').readlines()
d = {}
for x in range(226):
    a[x] = a[x].strip()
    b[x] = b[x].strip()
    c[x] = c[x].strip()

    d[a[x]] = {
        "name": b[x],
        "bic": c[x],
    }

import json
print json.dumps(d, indent=2)
#import pprint
#pprint.pprint(d)
