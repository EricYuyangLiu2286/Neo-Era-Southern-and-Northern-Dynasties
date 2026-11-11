"""Apply a population plan to common/history/pops with conservation checks. Preview by default.

python scripts/pop_rewrite.py <plan.json>            # print before/after per state, write nothing
python scripts/pop_rewrite.py <plan.json> --write    # write the MOD files (back up first with backup.py)

plan.json is a list of steps:
  {"file": "common/history/pops/14_siberia.txt", "state": "IRKUTSK", "tag": "RUS",
   "replace": {"culture": "russian", "size": 110000},
   "add": [["ce_liaodong", 50000], ["manchu", 45000]]}
"replace" (optional) sets the single pop of that culture to the new size; the people removed must
equal the people added, so the state total stays the same. "add" appends create_pop blocks to the
region_state. Keeps BOM and line endings.
Generalised from WORK/reports/denglai-route/far_north_pops.py (2026-11-10).
"""
import argparse, json, re
from pathlib import Path
from catalog import MOD


def total(block):
    return sum(int(x) for x in re.findall(r'size\s*=\s*(\d+)', block))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('plan', type=Path)
    ap.add_argument('--write', action='store_true')
    ap.add_argument('--mod', type=Path, default=MOD)
    a = ap.parse_args()
    texts = {}
    for step in json.loads(a.plan.read_text('utf-8-sig')):
        f = a.mod / step['file']
        if f not in texts:
            raw = f.read_bytes()
            texts[f] = [raw.decode('utf-8-sig'), raw.startswith(b'\xef\xbb\xbf')]
        t = texts[f][0]
        st, tag = step['state'], step['tag']
        m = re.search(r'\ts:STATE_%s = \{[^\n]*\n\t\tregion_state:%s\s*=\s*\{\r?\n(.*?)\r?\n\t\t\}'
                      % (re.escape(st), re.escape(tag)), t, re.S)
        if not m:
            raise SystemExit(f'not found: STATE_{st} region_state:{tag} in {step["file"]}')
        body = m.group(1)
        before = total(body)
        adds = step.get('add', [])
        rep = step.get('replace')
        if rep:
            rs = re.findall(r'(culture = %s\s*\r?\n\s*size = )(\d+)' % re.escape(rep['culture']), body)
            if len(rs) != 1:
                raise SystemExit(f'{st}: expected one {rep["culture"]} pop, found {len(rs)}')
            delta = int(rs[0][1]) - rep['size']
            if delta != sum(s for _, s in adds):
                raise SystemExit(f'{st}: removed {delta} but adding {sum(s for _, s in adds)}')
            body = body.replace(rs[0][0] + rs[0][1], rs[0][0] + str(rep['size']))
        nl = '\r\n' if '\r\n' in body else '\n'
        for c, s in adds:
            body += nl + '\t\t\tcreate_pop = {' + nl + f'\t\t\t\tculture = {c}' + nl + f'\t\t\t\tsize = {int(s)}' + nl + '\t\t\t}'
        after = total(body)
        if rep and after != before:
            raise SystemExit(f'{st}: total changed {before} -> {after}')
        texts[f][0] = t[:m.start(1)] + body + t[m.end(1):]
        print(f'{st:20s} {tag} {before:>9} -> {after:>9}')
    for f, (t, bom) in texts.items():
        if t.count('{') != t.count('}'):
            raise SystemExit(f'unbalanced braces in {f}')
        if a.write:
            f.write_bytes((b'\xef\xbb\xbf' if bom else b'') + t.encode('utf-8'))
        print(('wrote ' if a.write else 'preview ') + str(f))


if __name__ == '__main__':
    main()
