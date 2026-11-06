"""Final step-1 statistics.
python3 -I report.py corpora.json repo outdir
"""
import json, os, re, subprocess, sys
from collections import Counter, defaultdict
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mine import clean, is_prose, chars
from fields import index, classify
from corpus import parse_text

S = r'[^。！？；\\]{0,40}'
# Final candidate list. (label, regex, note)
P = [
    ('也须／仍须／还须／须先', r'(也|仍|还|亦)须|须先', '补一条义务或代价'),
    ('承担', r'承担', '“谁承担多少”式收尾'),
    ('安排', r'安排', '泛指制度/协议'),
    ('生计', r'生计', ''),
    ('往来', r'往来', '泛指外交/贸易'),
    ('争取', r'争取', ''),
    ('共同（共同的/共同市场以外）', r'共同(?!市场)', ''),
    ('经营（共同市场/旧例以外）', r'(?<!继续)(?<!依旧例)(?<!旧例)经营(?!共同市场)', ''),
    ('仍（仍在/仍然/仍须）', r'仍', '“A已……，B仍……”对举'),
    ('地方（泛称）', r'地方(?!失序|官|志|自治)', ''),
    ('本国（泛称自指）', r'本国', ''),
    ('政府（泛称主语）', r'政府', ''),
    ('朝廷（泛称主语）', r'朝廷', ''),
    ('两国／双方（对称叙述）', r'两国|双方', ''),
    ('维持', r'维持', ''),
    ('却（转折）', r'却', ''),
    ('如今', r'如今', ''),
    ('已经', r'已经', '完成体铺陈'),
    ('希望（某方希望……）', r'希望', ''),
    ('“，……也须/也要/也将……”补述', r'，(?:[^，。]{0,8})也(?:须|要|得|将|会|不)', '每说一个好处就补一个代价'),
    ('须决定／须判断／须衡量／须考虑（把问题抛给玩家）', r'(须|应当|要)(先)?(决定|判断|衡量|考虑|权衡|选择)', ''),
    ('等候／等待……决定或答复', r'(等候|等待)' + S + r'(决定|答复|裁断)', '段尾“等候某人决定”'),
    ('能否……决定／关系着', r'能否' + S + r'(将决定|决定|关系|取决)', '段尾总括'),
    ('关系着／关系到', r'关系(着|到)', ''),
    ('由谁／听谁／归谁（设问罗列）', r'由谁|听谁|归谁', ''),
    ('……的余地', r'余地', ''),
    ('有了（……有了新的……）', r'有了', ''),
    ('事务', r'事务', ''),
    ('处置／处理', r'处置|处理', ''),
    ('各自', r'各自', ''),
    ('若……则／便', r'若' + S + r'(则|便)', ''),
    ('既……也／又', r'既' + S + r'(也|又)', ''),
    ('不再', r'不再', ''),
    ('只能／只得', r'只能|只得', ''),
    ('也有人／有人主张（各方并陈）', r'也有人|有人(主张|认为|希望)', ''),
    ('此项／本项／本次（开发口吻）', r'此项|本项|本次', ''),
    ('原有／现有／既有', r'原有|现有|既有', ''),
    ('答复', r'答复', ''),
]
KNOWN = [
    ('然而……（并）不能／无法', r'然而' + S + r'(并不能|不能|无法|难以)'),
    ('不是……而是', r'不是' + S + r'而是'),
    ('在……之间', r'在' + S + r'之间'),
    ('相关', r'相关'),
    ('推进', r'推进'),
]
DEV = re.compile(r'此项|本项|本次|相关|推进|子项目|子日志|原规则|按原|继续决定|核验|重新累计|口径|事务随|已有.{0,6}保留|保留已有|清零|累计')
NARR = {'事件正文', '事件选项', '日志正文', '日志状态/目标', '按钮说明', '修正名', '修正说明', '通知', '决议',
        '其他说明', '事件标题', '日志标题', '其他'}
MECH = {'提示/条件', '进度条', '按钮名'}


def author_revisions(repo):
    out = {}
    p = os.path.join(repo, 'development/workbench/reports/canon-prose-20261102/author-revision-original.txt')
    for k, v, _ in parse_text(open(p, encoding='utf-8-sig').read()):
        out[k] = ('canon-prose-20261102/author-revision-original.txt', v)
    blob = subprocess.run(['git', '-C', repo, 'show',
                           'be56496:localization/simp_chinese/replace/zzzzzzzzzzzz_nesnd_batch_c_l_simp_chinese.yml'],
                          capture_output=True).stdout.decode('utf-8', 'replace')
    diff = subprocess.run(['git', '-C', repo, 'show', 'be56496', '--', '*.yml'], capture_output=True).stdout.decode()
    changed = set(re.findall(r'^\+\s*([A-Za-z0-9_.]+):', diff, re.M))
    for k, v, _ in parse_text(blob):
        if k in changed:
            out[k] = ('be56496（作者本机改稿）', v)
    return out


def main(cp, repo, outdir):
    d = json.load(open(cp, encoding='utf-8'))
    ix = index(repo)
    rev = author_revisions(repo)
    explicit_author = {'nesnd_american_restoration.2.d': 'prose-icons-20261106 审查记“作者改稿整段保留”',
                       'nesnd_khanate_suppression_failed_tt': '含作者 11-05 指定措辞“围绕大平原的纷争已经结束”',
                       'nesnd_ui_khanate_campaign_ended_tt': '同上'}
    pending_files = {'nesnd_india_l_simp_chinese.yml': '作者本机M有未上传改稿（任务45），本仓库看不到差异',
                     'nesnd_qin_persia_l_simp_chinese.yml': 'journal-war-feedback-20261103 记为 preserved_preexisting_author_files，归属不明'}
    rows = []
    for r in d['current']:
        r = dict(r)
        r['field'] = classify(r['key'], ix)
        fn = os.path.basename(r['file'])
        if r['status'] in ('agent_new', 'agent_changed'):
            if r['key'] in rev:
                r['status'] = 'author_revision' if rev[r['key']][1] == r['value'] else 'author_revision_then_agent'
                r['rev_src'] = rev[r['key']][0]
            elif r['key'] in explicit_author:
                r['status'] = 'author_revision'
                r['rev_src'] = explicit_author[r['key']]
            elif fn in pending_files:
                r['status'] = 'pending_confirm'
        rows.append(r)

    agent_ok = ('agent_new', 'agent_changed', 'author_revision_then_agent')

    def scope(r):
        if r['status'] not in agent_ok:
            return None
        if r['field'] == '名称类':
            return None
        if r['field'] in MECH:
            return 'mech_dev' if DEV.search(clean(r['value'])) else None
        if r['field'] == '其他' and not re.search(r'[一-鿿]{6}', clean(r['value'])):
            return None
        return 'narr'

    for r in rows:
        r['scope'] = scope(r)

    narr = [(r['key'], r['value']) for r in rows if r['scope'] == 'narr' and is_prose(r['value'])]
    author = [(k, v) for k, vs in d['author'].items() for v in vs if is_prose(v)]
    vanilla = [(k, v) for k, v in d['vanilla'].items() if is_prose(v)]
    cg, ca, cv = chars([v for _, v in narr]), chars([v for _, v in author]), chars([v for _, v in vanilla])

    def cnt(entries, rx):
        o, ks = 0, []
        for k, v in entries:
            n = len(re.findall(rx, clean(v)))
            if n:
                o += n
                ks.append(k)
        return o, ks

    res = []
    for label, rx, note in P:
        g, gk = cnt(narr, rx)
        a, _ = cnt(author, rx)
        v, _ = cnt(vanilla, rx)
        rg, ra, rv = g / cg * 1e4, a / ca * 1e4, v / cv * 1e4
        score = min(rg / max(ra, .2), rg / max(rv, .2))
        res.append(dict(label=label, rx=rx, note=note, g=g, gk=len(gk), a=a, v=v, rg=rg, ra=ra, rv=rv,
                        score=score, ex=gk[:6]))
    res.sort(key=lambda x: -x['score'] * (x['g'] ** .5))
    top = res[:30]
    known = []
    for label, rx in KNOWN:
        g, gk = cnt(narr, rx)
        a, _ = cnt(author, rx)
        v, _ = cnt(vanilla, rx)
        known.append(dict(label=label, g=g, gk=len(gk), a=a, v=v, rg=g / cg * 1e4, ra=a / ca * 1e4, rv=v / cv * 1e4,
                          ex=gk[:6]))

    toprx = [re.compile(t['rx']) for t in top]
    perfile = defaultdict(Counter)
    for r in rows:
        f = r['file'].replace('localization/simp_chinese/', '')
        c = perfile[f]
        c['total'] += 1
        c[r['status']] += 1
        if r['scope'] == 'narr':
            c['narr'] += 1
            hits = sum(1 for x in toprx if x.search(clean(r['value'])))
            if hits:
                c['hit'] += 1
            if hits >= 3:
                c['hit3'] += 1
            if DEV.search(clean(r['value'])):
                c['dev'] += 1
        elif r['scope'] == 'mech_dev':
            c['mech_dev'] += 1
        if r['status'] == 'pending_confirm' and r['field'] != '名称类':
            c['pending_text'] += 1
    fieldc = Counter(r['field'] for r in rows if r['scope'])
    out = dict(chars=dict(agent_narr=cg, author=ca, vanilla=cv),
               entries=dict(agent_narr=len(narr), author=len(author), vanilla=len(vanilla)),
               top=top, rest=res[30:], known=known, perfile={k: dict(v) for k, v in perfile.items()},
               fields=dict(fieldc),
               status=dict(Counter(r['status'] for r in rows)),
               author_revision_rows=[dict(key=r['key'], file=r['file'], status=r['status'], src=r.get('rev_src'))
                                     for r in rows if r['status'].startswith('author_revision')])
    json.dump(out, open(os.path.join(outdir, 'step1-stats.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    json.dump(rows, open(os.path.join(outdir, 'step1-rows.json'), 'w', encoding='utf-8'), ensure_ascii=False)
    print(out['chars'], out['entries'], out['status'])
    print(out['fields'])
    for t in top:
        print(f"{t['label'][:26]:<28} 代理{t['g']}({t['rg']:.1f})/{t['gk']}键 作者{t['a']}({t['ra']:.1f}) 原版{t['v']}({t['rv']:.1f}) s={t['score']:.1f}")
    print('-- rest')
    for t in res[30:]:
        print(f"{t['label'][:26]:<28} 代理{t['g']}({t['rg']:.1f}) 作者{t['a']}({t['ra']:.1f}) 原版{t['v']}({t['rv']:.1f})")
    print('-- known')
    for t in known:
        print(t['label'], t['g'], t['a'], t['v'], t['ex'])
    print('author_revision rows', len(out['author_revision_rows']), Counter(x['status'] for x in out['author_revision_rows']))


main(*sys.argv[1:4])
