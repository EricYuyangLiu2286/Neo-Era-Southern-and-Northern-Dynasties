"""Read actual text-save markets, subject pacts and located building goods fields.

No simulation and no save mutation. Numeric goods IDs remain unmapped. The
market_manager world-market trend channels are deliberately excluded from its
database reader: they also have numeric keys but are not market records.
"""
from pathlib import Path
import argparse
import collections
import hashlib
import json
import re
import sys

sys.path.insert(0, r'C:\Users\Eric Liu\.codex\skills\nesnd-victoria3\scripts')
from pdx import parse, read, effective_files, basekey
from catalog import GAME, WORK


def scalar(body, key, default=None):
    m = re.search(r'^\t' + re.escape(key) + r'=([^\n]+)', body, re.M)
    return m[1].strip('"') if m else default


def sections(text):
    headers = list(re.finditer(r'^([a-z_]+)=\{', text, re.M))
    return {m[1]: text[m.start(): headers[i + 1].start() if i + 1 < len(headers) else len(text)]
            for i, m in enumerate(headers)}


def records(section):
    matches = list(re.finditer(r'^\tdatabase=\{', section, re.M))
    if len(matches) != 1:
        raise ValueError('Expected exactly one immediate database in section')
    database = section[matches[0].end():]
    result = {}
    for m in re.finditer(r'^(\d+)=\{\n(.*?)^\}', database, re.M | re.S):
        if m[1] in result:
            raise ValueError('Duplicate database record ID: ' + m[1])
        result[m[1]] = m[2]
    return result


def record_node(body):
    return parse('record={\n' + body + '}').children[0]


def symbolic_subject_actions(mod):
    effective = {}
    for p in effective_files([GAME, mod], 'common/diplomatic_actions'):
        text, tree = read(p)
        for node in tree.children:
            if node.children is not None:
                effective[basekey(node.key)] = (p, text, node)
    result = {}
    for action, (p, text, node) in effective.items():
        pact = node.get('pact')
        if pact and pact.scalar('subject_type'):
            result[action] = {
                'subject_type': pact.scalar('subject_type'),
                'source': str(p), 'sha256': hashlib.sha256(p.read_bytes()).hexdigest(),
                'line': text[:node.start].count('\n') + 1,
                'direction_basis': 'subject pact targets.first=overlord, targets.second=subject; cross-checked with history',
            }
    return result


def read_snapshot(source, subject_actions):
    raw = source.read_bytes()
    if not raw.startswith(b'SAV'):
        raise ValueError('Only uncompressed native text saves are supported')
    digest = hashlib.sha256(raw).hexdigest()
    text = raw.decode('utf-8-sig')
    sec = sections(text)
    country_bodies = records(sec['country_manager'])
    countries = {}
    for cid, body in country_bodies.items():
        countries[cid] = {
            'country_id': cid, 'tag': scalar(body, 'definition'),
            'dead': scalar(body, 'dead', 'no') == 'yes',
            'raw': {key: scalar(body, key) for key in (
                'market', 'capital', 'market_capital', 'power_bloc_as_core',
                'power_bloc_join_date', 'country_type')},
        }
    by_tag = {}
    for cid, c in countries.items():
        if c['dead']:
            continue
        if c['tag'] in by_tag:
            raise ValueError('Duplicate living country tag: ' + c['tag'])
        by_tag[c['tag']] = cid
    market_bodies = records(sec['market_manager'])
    markets = {}
    for mid, body in market_bodies.items():
        owner = scalar(body, 'owner')
        markets[mid] = {'market_id': mid, 'owner_country_id': owner,
                        'owner_tag': countries.get(owner, {}).get('tag'),
                        'raw_record': body.strip(), 'member_tags': []}
    for c in countries.values():
        if not c['dead'] and c['raw']['market'] is not None:
            mid = c['raw']['market']
            if mid not in markets:
                raise ValueError('Living country references absent market: ' + c['tag'])
            markets[mid]['member_tags'].append(c['tag'])
    for market in markets.values():
        market['member_tags'].sort()

    subject_edges = []
    for pid, body in records(sec['pacts']).items():
        node = record_node(body)
        action = node.scalar('action')
        if node.scalar('dead') == 'yes' or action not in subject_actions:
            continue
        targets = node.get('targets')
        if not targets:
            raise ValueError('Subject pact has no targets')
        first, second = targets.scalar('first'), targets.scalar('second')
        if first not in countries or second not in countries:
            raise ValueError('Subject pact has unresolved country ID')
        subject_edges.append({
            'pact_id': pid, 'action': action,
            'overlord_id': first, 'subject_id': second,
            'overlord': countries[first]['tag'], 'subject': countries[second]['tag'],
            'dead_endpoint': countries[first]['dead'] or countries[second]['dead'],
            'raw_record': body.strip(),
        })
    descendants = {'USM'}
    chains = {'USM': ['USM']}
    while True:
        additions = [(e['subject'], chains[e['overlord']] + [e['subject']])
                     for e in subject_edges if not e['dead_endpoint'] and e['overlord'] in descendants
                     and e['subject'] not in descendants]
        if not additions:
            break
        for tag, chain in additions:
            descendants.add(tag)
            chains[tag] = chain
    selected = descendants | {'MUG', 'FRA', 'HUS', 'QE1', 'CNE', 'MYS', 'JAP', 'USA'}
    usm_market = countries[by_tag['USM']]['raw']['market']
    relevant_markets = {countries[by_tag[tag]]['raw']['market'] for tag in selected if tag in by_tag}
    for mid in relevant_markets:
        selected |= set(markets[mid]['member_tags'])
    states = {}
    for sid, body in records(sec['states']).items():
        cid = scalar(body, 'country')
        if scalar(body, 'dead') == 'yes' or cid not in countries or countries[cid]['dead']:
            continue
        tag = countries[cid]['tag']
        if tag not in selected:
            continue
        states[sid] = {'state_id': sid, 'country_id': cid, 'tag': tag,
                       'region': scalar(body, 'region'),
                       'country_market_id': countries[cid]['raw']['market'],
                       'raw': {key: scalar(body, key) for key in ('incorporation', 'arable_land', 'infrastructure', 'infrastructure_usage')},
                       'population': 0, 'located_buildings': {}}
    for _, body in records(sec['pops']).items():
        state = states.get(scalar(body, 'location'))
        if state:
            state['population'] += int(scalar(body, 'workforce', '0')) + int(scalar(body, 'dependents', '0'))
    goods_rows = []
    for bid, body in records(sec['building_manager']).items():
        if scalar(body, 'dead') == 'yes':
            continue
        state = states.get(scalar(body, 'state'))
        if not state:
            continue
        btype = scalar(body, 'building')
        summary = state['located_buildings'].setdefault(btype, {'levels': 0, 'staffing': 0})
        for key in summary:
            summary[key] += float(scalar(body, key, '0'))
        node = record_node(body)
        fields = {}
        for field in ('input_goods', 'output_goods'):
            value = node.get(field)
            if value is None:
                continue
            good_list = value.get('goods')
            fields[field] = {
                'raw_numeric_ids': {g.key: g.scalar('value') for g in good_list.children or []} if good_list else {},
                'uninterpreted_raw': body[value.start - len('record={\n'):value.end - len('record={\n')],
            }
        if fields:
            goods_rows.append({'building_id': bid, 'state_id': state['state_id'],
                               'region': state['region'], 'physical_country': state['tag'],
                               'country_market_id': state['country_market_id'], 'building_type': btype,
                               'levels': scalar(body, 'levels'), 'staffing': scalar(body, 'staffing'),
                               **fields})
    selected_countries = {}
    selected_market_ids = set()
    for tag in sorted(selected):
        if tag not in by_tag:
            selected_countries[tag] = {'exists': False, 'reason': 'No living country_manager record; no market membership inferred'}
            continue
        c = countries[by_tag[tag]].copy()
        c['exists'] = True
        c['usm_subject_chain'] = chains.get(tag)
        c['market_owner'] = markets[c['raw']['market']]['owner_tag'] if c['raw']['market'] in markets else None
        c['same_market_as_usm'] = c['raw']['market'] == usm_market
        c['state_ids'] = [sid for sid, st in states.items() if st['tag'] == tag]
        c['population'] = sum(st['population'] for st in states.values() if st['tag'] == tag)
        selected_countries[tag] = c
        selected_market_ids.add(c['raw']['market'])
    relevant_blocs = {}
    for bid, body in records(sec['power_bloc_manager']).items():
        n = record_node(body)
        if n.scalar('leader') in {by_tag.get(tag) for tag in selected}:
            relevant_blocs[bid] = {'leader_id': n.scalar('leader'),
                                   'leader_tag': countries.get(n.scalar('leader'), {}).get('tag'),
                                   'identity': n.scalar('identity'),
                                   'principles': n.get('principles').values() if n.get('principles') else [],
                                   'raw_record': body.strip()}
    if hashlib.sha256(source.read_bytes()).hexdigest() != digest:
        raise ValueError('Source save changed during read; discard this observation')
    return {'source': str(source), 'sha256': digest, 'date': re.search(r'game_date=(\S+)', text)[1],
            'countries': selected_countries,
            'markets': {mid: markets[mid] for mid in sorted(selected_market_ids) if mid in markets},
            'subject_pacts': [e for e in subject_edges if e['overlord'] in selected or e['subject'] in selected],
            'usm_subject_chains': chains, 'states': states, 'power_blocs': relevant_blocs,
            'building_goods_fields': goods_rows,
            'checks': {'source_unchanged': True, 'market_records': len(markets),
                       'living_country_records': len(by_tag), 'selected_state_records': len(states)}}


def markdown(result):
    lines = ['# 南朝及相关国家：实际存档市场网络', '',
             '本报告从原生存档读取country.market，再以market_manager.database.owner核对市场主人。宗属与同市场分别记录；不是从历史声明推断。未对游戏进行新操作。', '',
             '## 两日期的市场归属', '',
             '|TAG|存活|市场/主人（首份存档）|市场/主人（末份存档）|实际USM宗属链|', '|---|---|---|---|---|']
    first, last = result['snapshots'][0], result['snapshots'][-1]
    for tag in sorted(set(first['countries']) | set(last['countries'])):
        a, b = first['countries'].get(tag, {}), last['countries'].get(tag, {})
        def label(c):
            return str(c.get('raw', {}).get('market', '无')) + '/' + str(c.get('market_owner', '无'))
        lines.append(f"|{tag}|{'是' if b.get('exists') else '否'}|{label(a)}|{label(b)}|{'→'.join(b.get('usm_subject_chain') or [])}|")
    lines += ['', '## 共同市场与地区归属', '']
    for mid, market in last['markets'].items():
        lines.append(f"- {market['owner_tag']}市场（原始ID {mid}），{len(market['member_tags'])}个存活TAG：" + '、'.join(market['member_tags']) + '。')
    direct = [e for e in last['subject_pacts'] if e['overlord'] == 'USM' and not e['dead_endpoint']]
    indirect = [chain for chain in last['usm_subject_chains'].values() if len(chain) > 2]
    lines += ['', f"本次实际USM拥有{len(direct)}个直接属国；另外{len(indirect)}个间接属国：" + '、'.join('→'.join(chain) for chain in indirect) + '。', '',
              'CNE—HUS同市场的存档旁证是贸易联盟中的principle_market_unification_3；这不意味着HUS变成CNE属国。FRA与MUG也在同一实际市场。内战干预、贸易恢复、征税和商品供给分析必须把这些跨国市场关系带入。', '',
              '|实际州|所有TAG|末份存档人口|其国家市场|', '|---|---|---:|---|']
    for st in last['states'].values():
        if st['region'] in {'STATE_MYSORE', 'STATE_GUJARAT', 'STATE_KYUSHU', 'STATE_SHIKOKU'}:
            lines.append(f"|{st['region']}|{st['tag']}|{st['population']:,}|{st['country_market_id']}|")
    lines += ['', '## 所在国的部分实际产业', '',
              '下表为末份存档的建筑levels；括号为原始staffing。它说明生产设施的位置，不证明满负荷商品已运到某个消费国。完整州、建筑及原始投入/产出数字商品ID保留在JSON。', '',
              '|TAG|造纸厂|工具厂|兵工厂|硫矿|煤矿|', '|---|---:|---:|---:|---:|---:|']
    for tag in ['USM', 'HNA', 'SIH', 'GNG', 'JAP', 'BUR', 'DEI', 'PHI', 'YN1', 'MUG', 'FRA', 'CNE', 'HUS']:
        totals = collections.defaultdict(lambda: {'levels': 0, 'staffing': 0})
        for st in last['states'].values():
            if st['tag'] == tag:
                for typ, b in st['located_buildings'].items():
                    for key in ('levels', 'staffing'):
                        totals[typ][key] += b[key]
        values = []
        for typ in ['building_paper_mill', 'building_tooling_workshop', 'building_arms_industry', 'building_sulfur_mine', 'building_coal_mine']:
            b = totals[typ]
            values.append(f"{b['levels']:g} ({b['staffing']:.2f})")
        lines.append('|' + tag + '|' + '|'.join(values) + '|')
    lines += ['', '## 读数边界', '',
              '- 同市场不会合并国家身份、财政、政府和战争选择；直辖STATE_MYSORE等仍是USM自己的州，没有独立MYS市场。',
              '- 市场ID只在各存档内部解析；报告同时保留主人TAG及country ID，不能把数字当成跨版本固定ID。',
              '- 建筑input_goods/output_goods原字段、数字商品ID、物理所在国/州单独保留在JSON。没有猜商品ID、将物理出产地冒充投资者，或将生产字段直接叫成实际跨国交付量。',
              '- staffing是建筑等级等效用工指标，不是工人数。市场成员不保证100%市场接入、物流可达或商品有购买力。',
              '- 两份存档均来自CNE玩家局；其他国家行为是该局AI运行，不能当作各国独立默认玩家的财政验收。',
              '- 本工具读取现有存档，没有验证战争退出、独立后的条约/市场重组和读档。', '', '## 原始来源', '']
    for snap in result['snapshots']:
        lines += [f"- {snap['date']}：`{snap['source']}`；SHA-256 `{snap['sha256']}`。"]
    return '\n'.join(lines) + '\n'


def main():
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument('sources', nargs='+', type=Path)
    cli.add_argument('--mod', required=True, type=Path)
    cli.add_argument('--out', required=True, type=Path, help='JSON report under WORK; paired .md is also written')
    args = cli.parse_args()
    destination = args.out.resolve()
    if not destination.is_relative_to(WORK.resolve()) or destination.suffix != '.json':
        raise ValueError('Reports must be JSON paths inside WORK')
    subject_actions = symbolic_subject_actions(args.mod)
    result = {'candidate': str(args.mod.resolve()), 'subject_action_definitions': subject_actions,
              'notes': ['Membership is read from actual country.market and market database.owner.',
                        'Numeric goods IDs, absent goods blocks, and cache semantics are not inferred.',
                        'Input/output fields describe located buildings, not delivery contracts or foreign ownership.'],
              'snapshots': [read_snapshot(p.resolve(), subject_actions) for p in args.sources]}
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
    destination.with_suffix('.md').write_text(markdown(result), encoding='utf-8')
    print(json.dumps({'report': str(destination), 'dates': [s['date'] for s in result['snapshots']],
                      'usm_chains': [len(s['usm_subject_chains']) for s in result['snapshots']],
                      'building_goods_rows': [len(s['building_goods_fields']) for s in result['snapshots']]}, ensure_ascii=False))


if __name__ == '__main__':
    main()
