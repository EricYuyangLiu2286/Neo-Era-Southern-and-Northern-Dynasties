"""Read-only population envelope audit against the ORIGINAL mod, never the last candidate.

The fixed reference combines pre-update-20261030T233944Z with the frozen vanilla
1.13.11 / 24799966 source snapshot. Current vanilla is a separate comparison.
New regions are mapped by province membership to their original parent region.
Cross-parent regions require an explicit per-history-pop geographic ledger;
missing provinces and a zero-to-positive baseline still require review.
The tool never silently chooses the largest overlap.
"""
from pathlib import Path
from collections import Counter, defaultdict
from datetime import datetime, timezone
import argparse
import hashlib
import json
import sys

SKILL = Path(r'C:/Users/Eric Liu/.codex/skills/nesnd-victoria3/scripts')
sys.path.insert(0, str(SKILL))
from pdx import read, effective_files, basekey

WORK = Path(r'D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench')
GAME = Path(r'D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game')
ORIGINAL = WORK / 'backups/pre-update-20261030T233944Z/mod'
FROZEN_GAME = WORK / 'baselines/vanilla-1.13.11-24799966/game'
ORIGINAL_MANIFEST_SHA = 'fcbc00f4e12c03984f44c6d17c58fec5b455dc93b0c665731b88cef25997cb1a'
FROZEN_MANIFEST_SHA = 'baaac1a4ea1ceee78af81529b29ec742152dd26dd29b03d39d3419040f887834'
FOLDERS = ('map_data/state_regions', 'common/history/pops')
SPLIT_REFERENCE = WORK / 'backups/checkpoint-national-reference-month-20261031T124519Z/mod'
SPLIT_MANIFEST_SHA = '94cc320660592932233d95ddf3b52a442317c25bec0e94000ee8b1a53d0128df'
# This old MOD province entry was a lake, not a transfer of inhabited territory.
KNOWN_WATER_REPAIRS = {'STATE_GANSU': {'XBD5671'}}



def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def fixed_reference_integrity():
    """Pinned manifests prevent accidental rebasing, including inherited vanilla."""
    om = ORIGINAL.parent / 'manifest.json'
    gm = FROZEN_GAME.parent / 'manifest.json'
    if sha(om) != ORIGINAL_MANIFEST_SHA or sha(gm) != FROZEN_MANIFEST_SHA:
        raise ValueError('Fixed reference manifest changed; do not silently rebase the ±25% envelope.')
    original = json.loads(om.read_text(encoding='utf-8-sig'))['sha256']
    vanilla = json.loads(gm.read_text(encoding='utf-8-sig'))['files']
    sm = SPLIT_REFERENCE.parent / 'manifest.json'
    if sha(sm) != SPLIT_MANIFEST_SHA:
        raise ValueError('Fixed split allocation manifest changed; do not silently rebase.')
    split = json.loads(sm.read_text(encoding='utf-8-sig'))['sha256']
    checked = []
    for root, manifest in ((ORIGINAL, original), (FROZEN_GAME, vanilla), (SPLIT_REFERENCE, split)):
        relevant = {k: v for k, v in manifest.items() if any(k.startswith(folder + '/') for folder in FOLDERS) and k.endswith('.txt')}
        actual = {p.relative_to(root).as_posix() for folder in FOLDERS for p in (root / folder).rglob('*.txt')}
        if actual != set(relevant):
            raise ValueError('Fixed reference file membership changed: ' + str(root))
        for rel, expected in relevant.items():
            expected = expected['sha256'] if isinstance(expected, dict) else expected
            if sha(root / rel) != expected:
                raise ValueError('Fixed reference source changed: ' + str(root / rel))
            checked.append({'file': str(root / rel), 'sha256': expected})
    return checked


def extract(roots):
    regions, source_files = {}, []
    population = defaultdict(Counter)
    population_rows = defaultdict(list)
    groups = defaultdict(Counter)
    pop_sources = defaultdict(set)
    for folder in FOLDERS:
        for path in effective_files(roots, folder):
            _, tree = read(path)
            source_files.append({'file': str(path), 'sha256': sha(path)})
            if folder == 'map_data/state_regions':
                for node in tree.children:
                    key = basekey(node.key)
                    if not node.get('provinces'):
                        continue
                    if key in regions:
                        raise ValueError('Duplicate region definition cannot be silently resolved: ' + key)
                    regions[key] = sorted({x.upper() for x in node.get('provinces').values()})
            else:
                for wrapper in tree.children:
                    for node in wrapper.children or []:
                        if not node.key or not node.key.startswith('s:'):
                            continue
                        region = node.key[2:]
                        for state in node.children or []:
                            if not state.key or not state.key.startswith('region_state:'):
                                continue
                            tag = state.key.split(':', 1)[1]
                            for pop in state.all('create_pop'):
                                value = pop.scalar('size', '')
                                if not value.isdigit():
                                    raise ValueError(f'Population size is not a literal integer: {path}, {region}, {value!r}')
                                population[region][tag] += int(value)
                                population_rows[region].append({'country':tag,'culture':pop.scalar('culture','<unspecified>'),'religion':pop.scalar('religion','<culture_default>'),'population':int(value)})
                                groups[region][(tag, pop.scalar('culture', '<unspecified>'), pop.scalar('religion', '<culture_default>'))] += int(value)
                                pop_sources[region].add(str(path))
    unknown = sorted(set(population) - set(regions))
    if unknown:
        raise ValueError('Population references unknown regions: ' + ', '.join(unknown))
    return {'regions': regions, 'population_rows':dict(population_rows), 'population': {r: dict(c) for r, c in population.items()},
            'groups': groups, 'pop_sources': pop_sources, 'source_files': source_files}


def grouped_rows(counter):
    return [{'country': k[0], 'culture': k[1], 'religion': k[2], 'population': v}
            for k, v in sorted(counter.items())]


def dimension_totals(data):
    counters = {'country': Counter(), 'culture': Counter(), 'religion_explicit_or_default': Counter()}
    for groups in data['groups'].values():
        for (tag, culture, religion), count in groups.items():
            counters['country'][tag] += count
            counters['culture'][culture] += count
            counters['religion_explicit_or_default'][religion] += count
    return {key: dict(value) for key, value in counters.items()}



def audit(candidate, reasons=None):
    reasons = reasons or {}
    verified = fixed_reference_integrity()
    baseline = extract([FROZEN_GAME, ORIGINAL])
    split_reference = extract([FROZEN_GAME, SPLIT_REFERENCE])
    vanilla = extract([GAME])
    default_map = GAME / 'map_data/default.map'
    _, default_tree = read(default_map)
    lakes = {p.upper() for p in default_tree.get('lakes').values()}
    proposed = extract([GAME, candidate])
    memberships=Counter(p for ps in proposed['regions'].values() for p in ps)
    if any(count!=1 for count in memberships.values()):raise ValueError('Candidate province occurs in multiple regions; geographical duplication cannot create a population allowance.')
    province_parent = {}
    for region, provinces in baseline['regions'].items():
        for province in provinces:
            if province in province_parent:
                raise ValueError('Original map has duplicate province membership: ' + province)
            province_parent[province] = region
    ledger_path = Path(candidate) / 'EDITOR-GEOGRAPHIC-POPULATION.json'
    ledger = json.loads(ledger_path.read_text(encoding='utf-8-sig')) if ledger_path.exists() else {}
    if ledger and ledger.get('fixed_manifest_sha256') != ORIGINAL_MANIFEST_SHA:
        raise ValueError('Geographic population ledger does not name the fixed original baseline.')
    allocations = {}
    children, mapping, multiple_mapping, unresolved = defaultdict(list), {}, {}, []
    for region, provinces in proposed['regions'].items():
        parents = Counter(province_parent[p] for p in provinces if p in province_parent)
        unknown = [p for p in provinces if p not in province_parent]
        recorded = ledger.get('regions',{}).get(region)
        if recorded is not None:
            actual = proposed['population_rows'].get(region,[])
            if len(recorded)!=len(actual) or any({k:v for k,v in item.items() if k!='original_region'}!=row for item,row in zip(recorded,actual)):
                raise ValueError('Geographic population ledger differs from actual history rows: '+region)
            if any(item['original_region'] not in parents for item in recorded):
                raise ValueError('Population origin has no actual geographic intersection in '+region)
            alloc = defaultdict(Counter)
            for item in recorded:
                alloc[item['original_region']][(item['country'],item['culture'],item['religion'])]+=item['population']
        elif len(parents)==1:
            alloc={next(iter(parents)):proposed['groups'].get(region,Counter())}
        else:
            alloc={}
        if not parents or unknown or (len(parents)>1 and recorded is None):
            unresolved.append({'candidate_region': region, 'parent_province_counts': dict(parents), 'unknown_provinces': unknown, 'population': sum(proposed['population'].get(region, {}).values()),'requires_explicit_population_ledger':len(parents)>1})
            continue
        allocations[region]=alloc
        multiple_mapping[region]=sorted(parents)
        for parent in parents:children[parent].append(region)
        if len(parents)==1:mapping[region]=next(iter(parents))
    rows = []
    for parent, provinces in baseline['regions'].items():
        old_country = baseline['population'].get(parent, {})
        old = sum(old_country.values())
        child_regions = sorted(children[parent])
        new_country = Counter()
        new_groups = Counter()
        child_allocations = []
        mapped_provinces = set()
        for child in child_regions:
            child_groups=allocations[child].get(parent,Counter())
            child_country=Counter()
            for (tag,culture,religion),amount in child_groups.items():child_country[tag]+=amount
            new_country.update(child_country)
            new_groups.update(child_groups)
            fixed_child = sum(split_reference['population'].get(child, {}).values())
            child_total = sum(child_country.values())
            child_allocations.append({'region': child, 'fixed_split_population': fixed_child,
                'candidate_population': child_total, 'change_since_fixed_split': child_total - fixed_child,
                'fixed_split_by_country': split_reference['population'].get(child, {}),
                'candidate_by_country': dict(child_country),
                'entire_candidate_region_population':sum(proposed['population'].get(child,{}).values()),
                'fixed_split_demographics': grouped_rows(split_reference['groups'].get(child, {})),
                'candidate_demographics': grouped_rows(child_groups),
                'geometry_matches_fixed_split': set(split_reference['regions'].get(child, [])) == set(proposed['regions'][child]),
                'candidate_population_sources': sorted(proposed['pop_sources'].get(child, []))})
            mapped_provinces.update(p for p in proposed['regions'][child] if province_parent.get(p)==parent)
        new = sum(new_country.values())
        missing = set(provinces) - mapped_provinces
        verified_water_repairs = missing & KNOWN_WATER_REPAIRS.get(parent, set()) & lakes
        complete = mapped_provinces == set(provinces) - verified_water_repairs
        # Integer arithmetic makes the ±25% boundary inclusive and exact.
        within = (3 * old <= 4 * new <= 5 * old) if old else new == 0
        status = 'within_envelope' if complete and within else 'population_outside_envelope' if complete else 'geography_requires_review'
        current_vanilla = sum(vanilla['population'].get(parent, {}).values())
        rows.append({'original_region': parent, 'candidate_children': child_regions, 'original_population': old, 'candidate_aggregate_population': new, 'change': new - old, 'change_percent': 100 * (new - old) / old if old else None, 'lower_bound': old * .75, 'upper_bound': old * 1.25, 'within_population_envelope': within, 'complete_province_coverage': complete, 'status': status, 'original_population_by_country': old_country, 'candidate_population_by_country': dict(new_country), 'current_vanilla_same_key_population': current_vanilla, 'current_vanilla_same_key_geometry_matches': set(vanilla['regions'].get(parent, [])) == set(provinces), 'missing_provinces': sorted(missing),
                     'verified_noninhabitable_water_removal': sorted(verified_water_repairs),
                     'original_demographics': grouped_rows(baseline['groups'].get(parent, {})),
                     'candidate_demographics': grouped_rows(new_groups),
                     'child_allocations_since_fixed_split': child_allocations,
                     'original_population_sources': sorted(baseline['pop_sources'].get(parent, [])),
                     'demographic_composition_changed': baseline['groups'].get(parent, Counter()) != new_groups,
                     'population_change_reason': reasons.get(parent),
                     'population_change_reason_required': new != old and not reasons.get(parent)})
    return {'generated_at_utc': datetime.now(timezone.utc).isoformat(), 'candidate': str(candidate), 'fixed_baseline_mod': str(ORIGINAL), 'fixed_baseline_inherited_game': str(FROZEN_GAME), 'fixed_split_reference': str(SPLIT_REFERENCE), 'fixed_manifest_sha256': {'mod': ORIGINAL_MANIFEST_SHA, 'game': FROZEN_MANIFEST_SHA, 'split_reference': SPLIT_MANIFEST_SHA}, 'water_classification_source': {'path': str(default_map), 'sha256': sha(default_map), 'note': 'Only explicit known old lake repair xBD5671 is allowed; new geography differences remain review items.'}, 'current_vanilla': str(GAME), 'rule': 'Candidate child regions aggregate to original geographic parent. Inclusive 75%–125% of ORIGINAL mod population. Baseline is never the last candidate. Vanilla is comparison only.', 'notes': ['History create_pop sizes are initial population including dependents, not workforce or runtime immigration.', 'All country owners in each original geographic region are aggregated. Ownership transfers are also visible by country but do not reset the regional baseline.', 'New subdivisions do not each receive a separate fresh ±25% allowance.', 'Cross-parent mappings require a validated per-pop geographic ledger retaining the fixed original parent; unknown province mappings remain blocked. No majority-overlap guessing.', 'Passing this numeric envelope is not design approval or engine validation. Population changes are optional, not a target.', 'Current vanilla same-key populations may cover different geography; the geometry-match flag identifies this limitation.',
                'World population need not be conserved for a separately justified balance adjustment within each original regional envelope; pure subdivision remains conservation-only.',
                'Split allocation reference is fixed, not the latest candidate; every child delta is shown. Parent regional envelope is enforced to prevent new-key bypass.',
                'Religion <culture_default> preserves omitted history religion instead of guessing resolved engine religion.'], 'totals': {'original': sum(sum(x.values()) for x in baseline['population'].values()), 'current_vanilla': sum(sum(x.values()) for x in vanilla['population'].values()), 'candidate': sum(sum(x.values()) for x in proposed['population'].values())}, 'demographic_totals': {'original': dimension_totals(baseline), 'current_vanilla': dimension_totals(vanilla), 'fixed_split': dimension_totals(split_reference), 'candidate': dimension_totals(proposed)}, 'demographic_changes_requiring_explanation': [r['original_region'] for r in rows if r['demographic_composition_changed']],
     'missing_change_reasons': [r['original_region'] for r in rows if r['population_change_reason_required']], 'counts': dict(Counter(r['status'] for r in rows)), 'unresolved_mapping': unresolved, 'candidate_to_original_region': mapping, 'candidate_to_original_regions':multiple_mapping, 'geographic_population_ledger':{'path':str(ledger_path),'sha256':sha(ledger_path)} if ledger_path.exists() else None, 'rows': rows, 'verified_fixed_reference_files': verified, 'current_vanilla_sources': vanilla['source_files'], 'candidate_effective_sources': proposed['source_files'], 'engine_verified': False}


def main():
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument('--candidate', type=Path, required=True)
    cli.add_argument('--out', type=Path, required=True, help='JSON report inside WORK; a Markdown companion is written beside it.')
    cli.add_argument('--reasons', type=Path, help='Optional JSON original-region -> reason mapping, required for any changed regional total.')
    args = cli.parse_args()
    candidate, out = args.candidate.resolve(), args.out.resolve()
    if not out.is_relative_to(WORK.resolve()):
        raise ValueError('Reports must stay inside WORK.')
    if not candidate.is_dir():
        raise ValueError('Candidate directory does not exist.')
    reasons = json.loads(args.reasons.read_text(encoding='utf-8-sig')) if args.reasons else {}
    result = audit(candidate, reasons)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    lines = ['# 固定原始人口 ±25% 审计', '', result['rule'], '', '原始MOD：' + str(ORIGINAL), '原始继承本体：' + str(FROZEN_GAME), '候选：' + str(candidate), '', '这里只验证人口边界，不代表需要修改人口、不代表游戏内验收。独立人口调整允许各地区界内有理由的增减；全球守恒不是新增硬条件。拆州本身仍须守恒。', '', '|原始地区及拆出州|原始人口|候选合计|变化率|当前原版同名人口|状态|', '|---|---:|---:|---:|---:|---|']
    for row in result['rows']:
        if row['change'] or len(row['candidate_children']) != 1 or row['status'] != 'within_envelope':
            pct = f"{row['change_percent']:+.2f}%" if row['change_percent'] is not None else '零基准，需审议'
            lines.append(f"|{row['original_region']} → {', '.join(row['candidate_children'])}|{row['original_population']:,}|{row['candidate_aggregate_population']:,}|{pct}|{row['current_vanilla_same_key_population']:,}|{row['status']}|")
    lines.extend(['', '固定拆分方案：' + str(SPLIT_REFERENCE), '', '|新拆地区|固定拆分人口|候选人口|后续变化|', '|---|---:|---:|---:|'])
    for row in result['rows']:
        if len(row['candidate_children']) > 1:
            for child in row['child_allocations_since_fixed_split']:
                lines.append(f"|{child['region']}|{child['fixed_split_population']:,}|{child['candidate_population']:,}|{child['change_since_fixed_split']:+,}|")
    lines.extend(['', '世界人口：' + json.dumps(result['totals'], ensure_ascii=False),
                  '缺少调整理由：' + str(result['missing_change_reasons']), '',
                  '已证地理修复：甘肃旧 xBD5671 是 default.map 中湖面，迁移删除它不代表搬移人口；原始人口基准仍保持不变。', '',
                  '全部未变地区、各国家所有者和来源哈希保存在同名JSON。跨父地区/缺失province不能静默通过。', '', '统计：' + json.dumps(result['counts'], ensure_ascii=False), '未解决地图归并：' + str(len(result['unresolved_mapping']))])
    out.with_suffix('.md').write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print(json.dumps({'report': str(out), 'counts': result['counts'], 'unresolved_mapping': len(result['unresolved_mapping']), 'totals': result['totals']}, ensure_ascii=False))
    return 2 if result['unresolved_mapping'] or result['missing_change_reasons'] or any(r['status'] != 'within_envelope' for r in result['rows']) else 0


if __name__ == '__main__':
    raise SystemExit(main())
