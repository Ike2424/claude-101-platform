# Asset · Código "heredado" para demo de explicar código ajeno
# Usar en: M6 · Escena 3 (segunda demo de programación)
#
# Es un script de Python que parece más complicado de lo que es.
# Sin comentarios, con nombres poco descriptivos, y un par de
# decisiones de diseño cuestionables.

import json
from collections import defaultdict
from datetime import datetime, timedelta


def f(d, w=7):
    o = defaultdict(list)
    n = datetime.now()
    for x in d:
        try:
            t = datetime.fromisoformat(x['ts'])
        except (KeyError, ValueError):
            continue
        if n - t > timedelta(days=w):
            continue
        k = x.get('u') or 'anon'
        o[k].append(x.get('v', 0))
    r = {}
    for k, vs in o.items():
        if len(vs) < 3:
            continue
        m = sum(vs) / len(vs)
        s = (sum((v - m) ** 2 for v in vs) / len(vs)) ** 0.5
        if s > m * 0.5:
            r[k] = {'avg': round(m, 2), 'std': round(s, 2), 'n': len(vs)}
    return r


if __name__ == '__main__':
    with open('events.json') as fh:
        events = json.load(fh)
    print(json.dumps(f(events), indent=2))
