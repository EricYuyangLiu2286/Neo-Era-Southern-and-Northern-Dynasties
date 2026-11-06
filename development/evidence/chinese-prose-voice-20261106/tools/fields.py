"""Classify localization keys into UI fields using script definitions.
Imported by other tools. classify(key, repo_index) -> field label.
"""
import os, re

TOP = re.compile(r'^([A-Za-z_0-9.\-]+)\s*=\s*\{', re.M)


def defs(repo, sub):
    out = set()
    d = os.path.join(repo, sub)
    if not os.path.isdir(d):
        return out
    for dp, _, fs in os.walk(d):
        for f in fs:
            if f.endswith('.txt'):
                t = open(os.path.join(dp, f), encoding='utf-8-sig', errors='replace').read()
                out.update(TOP.findall(t))
    return out


def index(repo):
    ev = set()
    for dp, _, fs in os.walk(os.path.join(repo, 'events')):
        for f in fs:
            t = open(os.path.join(dp, f), encoding='utf-8-sig', errors='replace').read()
            ev.update(re.findall(r'^([A-Za-z_0-9]+\.\d+)\s*=\s*\{', t, re.M))
    return {
        'button': defs(repo, 'common/scripted_buttons'),
        'modifier': defs(repo, 'common/static_modifiers'),
        'je': defs(repo, 'common/journal_entries'),
        'bar': defs(repo, 'common/scripted_progress_bars'),
        'decision': defs(repo, 'common/decisions'),
        'event': ev,
    }


FIELDS = ['事件标题', '事件正文', '事件选项', '日志标题', '日志正文', '日志状态/目标', '按钮名', '按钮说明',
          '修正名', '修正说明', '进度条', '通知', '决议', '提示/条件', '名称类', '其他']


NAMEISH = re.compile(r'^([A-Z]{2,3}\d?|[A-Z]{2,3}\d?_ADJ|STATE_.*|HUB_NAME_.*|REGION_.*|dp_.*|nesnd_given_.*)$')
STATUSISH = re.compile(r'_(running|paused|completed|success|failed|active|confident|gone|truce|conclusion|ended|done|open|closed|blocked|waiting|ready)(_\w+)?$')


def classify(k, ix):
    if NAMEISH.match(k) or re.search(r'_(first|last|name)$', k):
        return '名称类'
    if re.search(r'_feedback_|_(up|down)_\d|_bound$|_delta_', k):
        return '提示/条件'
    if k.endswith('_option') or re.match(r'^[A-Za-z_0-9]+\.(cancel|defer|accept|refuse|confirm)$', k):
        return '事件选项'
    m = re.match(r'^(.+\.\d+)\.(.+)$', k)
    if m:
        base, suf = m.groups()
        if suf == 't':
            return '事件标题'
        if suf.startswith('d') or suf in ('desc',):
            return '事件正文'
        if suf.startswith('f') and len(suf) <= 2:
            return '事件正文'  # flavor text
        if re.fullmatch(r'[a-z]\d?(_tt)?|option.*', suf):
            return '事件选项' if not suf.endswith('_tt') else '提示/条件'
        return '事件正文' if base in ix['event'] else '其他'
    if k.startswith('notification_'):
        return '通知'
    for name in ix['bar']:
        if k == name or k == name + '_desc':
            return '进度条'
    if k in ix['je']:
        return '日志标题'
    if k.endswith('_reason') and k[:-7] in ix['je']:
        return '日志正文'
    if k.endswith('_goal') or k.endswith('_status') or 'status_desc' in k or k.endswith('_status_desc'):
        return '日志状态/目标'
    if k in ix['button']:
        return '按钮名'
    if k.endswith('_desc') and k[:-5] in ix['button']:
        return '按钮说明'
    if k in ix['modifier']:
        return '修正名'
    if k.endswith('_desc') and k[:-5] in ix['modifier']:
        return '修正说明'
    if k in ix['decision'] or (k.endswith('_desc') and k[:-5] in ix['decision']):
        return '决议'
    if k.endswith('_reason'):
        return '日志正文'
    if re.search(r'(_tt|_tooltip|_rules?|_cond|_conditions?|_effect|_cost|_requirement|_req|_hint|_detail)s?$', k) or '_tt_' in k:
        return '提示/条件'
    if k.endswith('_bar') or k.endswith('_bar_desc'):
        return '进度条'
    if STATUSISH.search(k):
        return '日志状态/目标'
    if k.endswith('_desc'):
        return '其他说明'
    return '其他'
