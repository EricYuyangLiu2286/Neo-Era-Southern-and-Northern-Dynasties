"""Static cross-check of a group of script files against the 1.15 script_docs export.

Usage: python scripts/script_xcheck.py "common/**/nesnd_sha_*.txt" "events/nesnd_sha_*.txt"  (globs relative to the MOD)
Generalised from WORK/tools/sha_logic_check/sha_check.py (2026-11-11, written for the Denglai files).


Checks:
  1. every key used as a trigger/effect exists in the 1.15 docs or as a scripted trigger/effect
  2. triggers used in effect context and effects in trigger context
  3. trigger/effect supported scopes against a tracked scope type
  4. variables read but never set / set but never read; global vs country mix
  5. static modifiers, events, buttons, bars, journal entries, loc keys referenced but undefined
"""
import re, sys, glob, os, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pdx

MOD = r'D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties'
GAME = r'D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game'
DOCS = r'D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/docs'

out = []
def report(kind, f, msg):
    out.append((kind, f.replace('\\', '/').replace(MOD + '/', ''), msg))

# ---------- docs ----------
def read_doc(path):
    d = {}
    cur = None
    for line in open(path, encoding='utf-8', errors='replace'):
        m = re.match(r'^## (\S+)', line)
        if m:
            cur = m.group(1); d[cur] = {'scopes': set(), 'targets': set()}; continue
        if cur:
            m = re.match(r'\*\*Supported Scopes\*\*: (.*)', line)
            if m: d[cur]['scopes'] = {s.strip() for s in m.group(1).split(',') if s.strip()}
            m = re.match(r'\*\*Supported Targets\*\*: (.*)', line)
            if m: d[cur]['targets'] = {s.strip() for s in m.group(1).split(',') if s.strip()}
    return d
TRIG = read_doc(DOCS + '/triggers.log')
EFF = read_doc(DOCS + '/effects.log')
LINKS = {}
cur = None
for line in open(DOCS + '/event_targets.log', encoding='utf-8', errors='replace'):
    m = re.match(r'^### (\S+)', line)
    if m: cur = m.group(1); LINKS[cur] = {'in': set(), 'out': set()}; continue
    if cur:
        m = re.match(r'Input Scopes: (.*)', line)
        if m: LINKS[cur]['in'] = {s.strip() for s in m.group(1).split(',')}
        m = re.match(r'Output Scopes: (.*)', line)
        if m: LINKS[cur]['out'] = {s.strip() for s in m.group(1).split(',')}

# ---------- definitions ----------
def top_keys(folder, roots=(GAME, MOD)):
    keys = set()
    for root in roots:
        for p in glob.glob(os.path.join(root, folder, '**', '*.txt'), recursive=True):
            try:
                _, n = pdx.read(p)
            except Exception:
                continue
            for c in n.children or []:
                if c.key: keys.add(pdx.basekey(c.key))
    return keys
STRIG = top_keys('common/scripted_triggers')
SEFF = top_keys('common/scripted_effects')
SVAL = top_keys('common/script_values')
SMOD = top_keys('common/static_modifiers')
BUTTONS = top_keys('common/scripted_buttons')
BARS = top_keys('common/scripted_progress_bars')
JES = top_keys('common/journal_entries')
EVENTS = set()
for root in (GAME, MOD):
    for p in glob.glob(os.path.join(root, 'events', '**', '*.txt'), recursive=True):
        for m in re.finditer(r'^\s*([\w.]+\.\d+)\s*=\s*\{', open(p, encoding='utf-8-sig', errors='replace').read(), re.M):
            EVENTS.add(m.group(1))

def loc_keys(lang):
    keys = set()
    for root in (GAME, MOD):
        for p in glob.glob(os.path.join(root, 'localization', lang, '**', '*.yml'), recursive=True):
            for line in open(p, encoding='utf-8-sig', errors='replace'):
                m = re.match(r'^\s*([\w.\-]+):\d*\s*"', line)
                if m: keys.add(m.group(1))
    return keys
LOC_ZH = loc_keys('simp_chinese'); LOC_EN = loc_keys('english')

# ---------- files ----------
PATTERNS = sys.argv[1:] or ['common/**/nesnd_sha_*.txt', 'events/nesnd_sha_*.txt']
FILES = sorted({p.replace('\\', '/') for pat in PATTERNS for p in glob.glob(MOD + '/' + pat, recursive=True)})
if not FILES:
    sys.exit('no files match ' + ' '.join(PATTERNS))

STRUCT_OPS = {'AND', 'OR', 'NOT', 'NOR', 'NAND'}
VALUE_KEYS = {'value', 'add', 'subtract', 'multiply', 'divide', 'min', 'max', 'round', 'floor', 'ceiling', 'abs',
              'desc', 'format', 'modulo', 'round_to', 'save_temporary_value_as', 'fixed_range', 'integer_range'}

PREFIX_SCOPE = {'c': 'country', 's': 'state_region', 'cu': 'culture', 'rel': 'religion', 'law_type': 'law_type',
                'pop_type': 'pop_type', 'ig': 'interest_group', 'je': 'journal_entry', 'flag': 'flag',
                'region_state': 'state', 'sr': 'strategic_region', 'g': 'goods', 'bt': 'building_type',
                'p': 'province', 'ideology': 'ideology', 'mt': 'military_type', 'unit_type': 'combat_unit_type',
                'decree_type': 'decree_type', 'institution_type': 'institution_type', 'ig_type': 'interest_group_type',
                'ig_trait': 'interest_group_trait', 'war_goal_type': 'war_goal_type', 'technology': 'technology',
                'company_type': 'company_type', 'law': 'law', 'power_bloc_identity': 'power_bloc_identity'}
UNKNOWN = None

def resolve_link(key, scope, root, prev):
    """Return (is_link, new_scope). new_scope None = unknown."""
    parts = key.split('.')
    s = scope
    for i, part in enumerate(parts):
        if ':' in part:
            pre, _ = part.split(':', 1)
            if pre in ('var', 'scope', 'global_var', 'local_var'):
                s = UNKNOWN; continue
            if pre in PREFIX_SCOPE:
                s = PREFIX_SCOPE[pre]; continue
            return (False, None) if i == 0 else (True, UNKNOWN)
        if part == 'root': s = root; continue
        if part == 'this': continue
        if part == 'prev': s = prev; continue
        if part in LINKS:
            outs = LINKS[part]['out']
            s = next(iter(outs)) if len(outs) == 1 else UNKNOWN
            continue
        return (False, None) if i == 0 else (True, UNKNOWN)
    return True, s

flags_set = collections.Counter(); flags_cmp = collections.Counter()
var_set = collections.defaultdict(set); var_read = collections.defaultdict(set)
gvar_set = collections.defaultdict(set); gvar_read = collections.defaultdict(set)
mods_used = []; events_used = []; loc_used = []

def check_scope(kind, name, scope, f, ctxpath):
    doc = TRIG.get(name) if kind == 'trigger' else EFF.get(name)
    if not doc or scope is UNKNOWN or not doc['scopes'] or 'none' in doc['scopes']:
        return
    if scope not in doc['scopes']:
        report('SCOPE', f, f'{kind} `{name}` used in {scope} scope (supports {sorted(doc["scopes"])}) at {ctxpath}')

def note_var(n, f, ctx):
    k, v = n.key, n.value
    def name_of(node):
        if node.children is not None:
            return node.scalar('name')
        return pdx.unquote(node.value)
    if k in ('set_variable', 'change_variable', 'add_to_variable_list', 'clamp_variable'):
        var_set[name_of(n)].add(f)
    elif k in ('set_global_variable', 'change_global_variable', 'add_to_global_variable_list'):
        gvar_set[name_of(n)].add(f)
    elif k in ('has_variable', 'remove_variable', 'has_variable_list', 'clear_variable_list', 'is_target_in_variable_list'):
        var_read[name_of(n)].add(f)
    elif k in ('has_global_variable', 'remove_global_variable', 'has_global_variable_list', 'clear_global_variable_list', 'is_target_in_global_variable_list'):
        gvar_read[name_of(n)].add(f)
    elif k in ('every_in_list', 'any_in_list', 'random_in_list', 'ordered_in_list'):
        if n.scalar('variable'): var_read[n.scalar('variable')].add(f)
        if n.scalar('global_variable'): gvar_read[n.scalar('global_variable')].add(f)

def scan_tokens(text, f):
    for m in re.finditer(r'(?<![\w])var:(\w+)', text): var_read[m.group(1)].add(f)
    for m in re.finditer(r'global_var:(\w+)', text): gvar_read[m.group(1)].add(f)

def walk(nodes, ctx, scope, root, prev, f, path):
    """ctx in {'trigger','effect','value','data'}"""
    for n in nodes or []:
        k = n.key
        here = f'{path}/{k}'
        if k is None:
            continue
        if n.value and isinstance(n.value, str):
            for m in re.finditer(r'flag:(\w+)', n.value):
                (flags_set if k in ('set_variable', 'value') else flags_cmp)[m.group(1)] += 1
        note_var(n, f, ctx)
        if k == 'name' and n.value and ctx == 'effect':
            pass
        if k in ('add_modifier', 'has_modifier', 'remove_modifier'):
            nm = n.scalar('name') if n.children is not None else pdx.unquote(n.value)
            mods_used.append((nm, f, here))
        if k == 'trigger_event':
            ev = n.scalar('id') if n.children is not None else pdx.unquote(n.value)
            events_used.append((ev, f, here))
        if k in ('custom_tooltip', 'custom_description', 'custom_label') and n.children is None:
            loc_used.append((pdx.unquote(n.value), f, here))
        if k in ('text', 'desc', 'title', 'name', 'custom_tooltip', 'custom_label') and n.children is None and ctx in ('effect', 'trigger') and k != 'name':
            loc_used.append((pdx.unquote(n.value), f, here))

        # --- structural keys ---
        if ctx in ('trigger', 'effect', 'value'):
            if k in ('if', 'else_if', 'else') and ctx in ('effect', 'value'):
                for c in n.children or []:
                    if c.key == 'limit':
                        walk(c.children, 'trigger', scope, root, prev, f, here + '/limit')
                walk([c for c in n.children or [] if c.key != 'limit'], ctx, scope, root, prev, f, here)
                continue
            if k in ('if', 'else_if', 'else') and ctx == 'trigger':
                report('CTX', f, f'`{k}` (effect form) used in trigger context at {here}; use trigger_if/trigger_else')
                walk([c for c in n.children or [] if c.key != 'limit'], ctx, scope, root, prev, f, here)
                continue
            if k in ('trigger_if', 'trigger_else_if', 'trigger_else'):
                if ctx != 'trigger':
                    report('CTX', f, f'`{k}` used in {ctx} context at {here}')
                for c in n.children or []:
                    if c.key == 'limit':
                        walk(c.children, 'trigger', scope, root, prev, f, here + '/limit')
                walk([c for c in n.children or [] if c.key != 'limit'], 'trigger', scope, root, prev, f, here)
                continue
            if k == 'limit':
                walk(n.children, 'trigger', scope, root, prev, f, here); continue
            if k in STRUCT_OPS:
                if ctx != 'trigger':
                    report('CTX', f, f'`{k}` used in {ctx} context at {here}')
                walk(n.children, 'trigger', scope, root, prev, f, here); continue
            if k in ('hidden_effect', 'show_as_tooltip'):
                walk(n.children, 'effect', scope, root, prev, f, here); continue
            if k == 'custom_tooltip' and n.children is not None:
                walk([c for c in n.children if c.key != 'text'], ctx, scope, root, prev, f, here)
                t = n.scalar('text')
                if t: loc_used.append((t, f, here))
                continue
            if k == 'random_list':
                for c in n.children or []:
                    walk([d for d in c.children or [] if d.key not in ('modifier',)], 'effect', scope, root, prev, f, here + '/' + str(c.key))
                continue
            if k == 'random' and ctx == 'effect':
                walk([c for c in n.children or [] if c.key not in ('chance',)], 'effect', scope, root, prev, f, here); continue
            if k == 'while' and ctx == 'effect':
                for c in n.children or []:
                    if c.key == 'limit': walk(c.children, 'trigger', scope, root, prev, f, here)
                walk([c for c in n.children or [] if c.key not in ('limit', 'count')], 'effect', scope, root, prev, f, here); continue
            if ctx == 'value' and k in VALUE_KEYS:
                if n.children is not None:
                    walk(n.children, 'value', scope, root, prev, f, here)
                continue
            # iterators
            m = re.match(r'^(any|every|random|ordered)_(.+)$', k)
            if m:
                docd = (TRIG if m.group(1) == 'any' else EFF).get(k)
                if docd is None and k not in STRIG and k not in SEFF:
                    report('UNKNOWN', f, f'iterator `{k}` not in docs at {here}')
                    continue
                if m.group(1) == 'any' and ctx not in ('trigger',):
                    report('CTX', f, f'trigger iterator `{k}` in {ctx} context at {here}')
                if m.group(1) in ('every', 'random', 'ordered') and ctx == 'trigger':
                    report('CTX', f, f'effect iterator `{k}` in trigger context at {here}')
                if docd:
                    check_scope('trigger' if m.group(1) == 'any' else 'effect', k, scope, f, here)
                tgt = next(iter(docd['targets'])) if docd and len(docd['targets']) == 1 else UNKNOWN
                sub = [c for c in n.children or [] if c.key not in ('count', 'percent', 'limit', 'max', 'order_by', 'position', 'min', 'check_range_bounds', 'variable', 'global_variable', 'list', 'type')]
                for c in n.children or []:
                    if c.key == 'limit': walk(c.children, 'trigger', tgt, root, scope, f, here + '/limit')
                    if c.key == 'order_by' and c.children is not None: walk(c.children, 'value', tgt, root, scope, f, here + '/order_by')
                walk(sub, 'trigger' if m.group(1) == 'any' else ctx, tgt, root, scope, f, here)
                continue
            # scope links
            is_link, new = resolve_link(k, scope, root, prev)
            if is_link and n.children is not None:
                walk(n.children, ctx, new, root, scope, f, here); continue
            if is_link and n.children is None:
                continue  # comparison like `c:CNE ?= this`, `owner = c:SHA`
            # quoted dynamic triggers
            if k.startswith('"') or '(' in k:
                continue
            # trigger / effect names
            if ctx == 'trigger':
                if k in TRIG:
                    check_scope('trigger', k, scope, f, here)
                    if k in ('custom_tooltip',): pass
                elif k in STRIG or k in SVAL:
                    pass
                elif k in EFF:
                    report('CTX', f, f'effect `{k}` used in trigger context at {here}')
                elif k in SEFF:
                    report('CTX', f, f'scripted effect `{k}` used in trigger context at {here}')
                else:
                    report('UNKNOWN', f, f'unknown trigger key `{k}` at {here}')
                if n.children is not None and k not in TRIG and k not in STRIG:
                    walk(n.children, 'data', scope, root, prev, f, here)
                continue
            if ctx == 'effect':
                if k in EFF:
                    check_scope('effect', k, scope, f, here)
                elif k in SEFF:
                    pass
                elif k in TRIG:
                    report('CTX', f, f'trigger `{k}` used in effect context at {here}')
                elif k in STRIG:
                    report('CTX', f, f'scripted trigger `{k}` used in effect context at {here}')
                else:
                    report('UNKNOWN', f, f'unknown effect key `{k}` at {here}')
                continue
            if ctx == 'value':
                if k in STRIG or k in SVAL or k in TRIG:
                    continue
                report('UNKNOWN', f, f'unknown value key `{k}` at {here}')
                continue
        # data context: descend looking for nested trigger/effect blocks
        if n.children is not None:
            walk(n.children, 'data', scope, root, prev, f, here)

# per-file-type entry points: (key -> ctx)
JE_BLOCKS = {'immediate': 'effect', 'on_complete': 'effect', 'on_fail': 'effect', 'on_timeout': 'effect', 'on_invalid': 'effect',
             'possible': 'trigger', 'complete': 'trigger', 'fail': 'trigger', 'invalid': 'trigger', 'is_shown_when_inactive': 'trigger',
             'should_be_pinned_by_default': 'trigger', 'should_show_when_not_involved': 'trigger', 'should_be_involved': 'trigger',
             'can_deactivate': 'trigger', 'can_revolution_inc': 'trigger'}
EV_BLOCKS = {'trigger': 'trigger', 'cancellation_trigger': 'trigger', 'immediate': 'effect', 'after': 'effect'}
BTN_BLOCKS = {'visible': 'trigger', 'possible': 'trigger', 'selected': 'trigger', 'effect': 'effect', 'ai_chance': 'value'}
DEC_BLOCKS = {'is_shown': 'trigger', 'possible': 'trigger', 'when_taken': 'effect', 'ai_chance': 'value'}

def process(f):
    try:
        text, root = pdx.read(f)
    except Exception as e:
        report('PARSE', f, str(e)); return
    scan_tokens(text, f)
    folder = f.replace('\\', '/').split('/common/')[-1].split('/')[0] if '/common/' in f.replace('\\', '/') else 'events'
    for top in root.children or []:
        k = top.key
        if k is None or k == 'namespace': continue
        if folder == 'scripted_triggers':
            walk(top.children, 'trigger', UNKNOWN, UNKNOWN, UNKNOWN, f, k)
        elif folder == 'scripted_effects':
            walk(top.children, 'effect', UNKNOWN, UNKNOWN, UNKNOWN, f, k)
        elif folder == 'script_values':
            walk(top.children, 'value', UNKNOWN, UNKNOWN, UNKNOWN, f, k)
        elif folder == 'journal_entries':
            for c in top.children or []:
                if c.key in JE_BLOCKS:
                    walk(c.children, JE_BLOCKS[c.key], 'country', 'country', UNKNOWN, f, f'{k}/{c.key}')
                elif c.key in ('on_weekly_pulse', 'on_monthly_pulse', 'on_yearly_pulse'):
                    for d in c.children or []:
                        if d.key == 'effect': walk(d.children, 'effect', 'country', 'country', UNKNOWN, f, f'{k}/{c.key}/effect')
                        if d.key == 'events':
                            for ev in d.values(): events_used.append((ev, f, f'{k}/{c.key}'))
                elif c.key == 'status_desc' or c.key == 'current_value' or c.key == 'goal_add_value':
                    walk(c.children, 'data', 'country', 'country', UNKNOWN, f, f'{k}/{c.key}')
                elif c.key == 'scripted_button':
                    if pdx.unquote(c.value) not in BUTTONS: report('REF', f, f'button `{c.value}` undefined in {k}')
                elif c.key == 'scripted_progress_bar':
                    if pdx.unquote(c.value) not in BARS: report('REF', f, f'bar `{c.value}` undefined in {k}')
                elif c.children is not None:
                    walk(c.children, 'data', 'country', 'country', UNKNOWN, f, f'{k}/{c.key}')
        elif folder == 'events':
            for c in top.children or []:
                if c.key in EV_BLOCKS:
                    walk(c.children, EV_BLOCKS[c.key], 'country', 'country', UNKNOWN, f, f'{k}/{c.key}')
                elif c.key == 'option':
                    for d in c.children or []:
                        if d.key == 'trigger': walk(d.children, 'trigger', 'country', 'country', UNKNOWN, f, f'{k}/option/trigger')
                        elif d.key == 'ai_chance': walk(d.children, 'value', 'country', 'country', UNKNOWN, f, f'{k}/option/ai_chance')
                        elif d.key in ('name', 'default_option', 'highlighted_option', 'fallback', 'is_shown'): pass
                        else: walk([d], 'effect', 'country', 'country', UNKNOWN, f, f'{k}/option')
                elif c.key in ('title', 'desc', 'flavor'):
                    if c.children is None: loc_used.append((pdx.unquote(c.value), f, f'{k}/{c.key}'))
                    else: walk(c.children, 'data', 'country', 'country', UNKNOWN, f, f'{k}/{c.key}')
        elif folder == 'scripted_buttons':
            for c in top.children or []:
                if c.key in BTN_BLOCKS:
                    walk(c.children, BTN_BLOCKS[c.key], 'country', 'country', UNKNOWN, f, f'{k}/{c.key}')
                elif c.key in ('name', 'desc'):
                    loc_used.append((pdx.unquote(c.value), f, f'{k}/{c.key}'))
        elif folder == 'decisions':
            for c in top.children or []:
                if c.key in DEC_BLOCKS:
                    walk(c.children, DEC_BLOCKS[c.key], 'country', 'country', UNKNOWN, f, f'{k}/{c.key}')
        elif folder == 'scripted_progress_bars':
            for c in top.children or []:
                if c.key in ('monthly_progress', 'weekly_progress', 'daily_progress'):
                    walk(c.children, 'value', UNKNOWN, UNKNOWN, UNKNOWN, f, f'{k}/{c.key}')
                elif c.key in ('name', 'desc'):
                    loc_used.append((pdx.unquote(c.value), f, f'{k}/{c.key}'))
        elif folder == 'on_actions':
            for c in top.children or []:
                if c.key == 'trigger': walk(c.children, 'trigger', UNKNOWN, UNKNOWN, UNKNOWN, f, f'{k}/trigger')
                elif c.key == 'effect': walk(c.children, 'effect', UNKNOWN, UNKNOWN, UNKNOWN, f, f'{k}/effect')
                elif c.key in ('events', 'random_events'):
                    for ev in c.values():
                        if re.match(r'^[\w.]+\.\d+$', ev): events_used.append((ev, f, f'{k}/{c.key}'))
        elif folder in ('diplomatic_actions', 'diplomatic_plays', 'war_goal_types'):
            for c in top.children or []:
                if c.key in ('potential', 'possible', 'valid', 'can_use', 'is_shown'):
                    walk(c.children, 'trigger', 'country', 'country', UNKNOWN, f, f'{k}/{c.key}')
                elif c.key and (c.key.endswith('_effect') or c.key in ('on_accept', 'on_decline', 'on_war_begins', 'on_weekly_pulse', 'on_enforced', 'on_created')):
                    walk(c.children, 'effect', UNKNOWN, UNKNOWN, UNKNOWN, f, f'{k}/{c.key}')
                elif c.children is not None:
                    walk(c.children, 'data', 'country', 'country', UNKNOWN, f, f'{k}/{c.key}')
        else:
            pass

for f in FILES:
    process(f)

# ---------- cross-references ----------
for nm, f, here in mods_used:
    if nm and nm not in SMOD and not nm.startswith('$'):
        report('REF', f, f'static modifier `{nm}` undefined at {here}')
for ev, f, here in events_used:
    if ev and ev not in EVENTS and '$' not in ev:
        report('REF', f, f'event `{ev}` undefined at {here}')
for key, f, here in loc_used:
    if not key or '$' in key or ' ' in key or key in ('yes', 'no'): continue
    if not key.startswith('nesnd'): continue
    if key not in LOC_ZH: report('LOC', f, f'loc `{key}` missing zh at {here}')
    if key not in LOC_EN: report('LOC', f, f'loc `{key}` missing en at {here}')

# variables: scan the whole mod for writers/readers so cross-file use counts
all_set = collections.defaultdict(set); all_read = collections.defaultdict(set)
all_gset = collections.defaultdict(set); all_gread = collections.defaultdict(set)
for p in glob.glob(MOD + '/common/**/*.txt', recursive=True) + glob.glob(MOD + '/events/**/*.txt', recursive=True):
    t = open(p, encoding='utf-8-sig', errors='replace').read()
    for m in re.finditer(r'\b(set_variable|change_variable|add_to_variable_list|clamp_variable)\s*=\s*(\{[^{}]*?name\s*=\s*(\w+)|(\w+))', t):
        all_set[m.group(3) or m.group(4)].add(p)
    for m in re.finditer(r'\b(set_global_variable|change_global_variable|add_to_global_variable_list)\s*=\s*(\{[^{}]*?name\s*=\s*(\w+)|(\w+))', t):
        all_gset[m.group(3) or m.group(4)].add(p)
    for m in re.finditer(r'\b(has_variable|has_variable_list|is_target_in_variable_list)\s*=\s*(\{[^{}]*?name\s*=\s*(\w+)|(\w+))', t):
        all_read[m.group(3) or m.group(4)].add(p)
    for m in re.finditer(r'(?<![\w])var:(\w+)', t): all_read[m.group(1)].add(p)
    for m in re.finditer(r'variable\s*=\s*(\w+)', t): all_read[m.group(1)].add(p)
    for m in re.finditer(r'\bhas_global_variable(_list)?\s*=\s*(\w+)', t): all_gread[m.group(2)].add(p)
    for m in re.finditer(r'global_var:(\w+)', t): all_gread[m.group(1)].add(p)
locvars = set()
for p in glob.glob(MOD + '/localization/**/*.yml', recursive=True):
    t = open(p, encoding='utf-8-sig', errors='replace').read()
    for m in re.finditer(r"Var\('(\w+)'\)|GetVariable\('(\w+)'\)|GetGlobalVariable\('(\w+)'\)", t):
        locvars.add(m.group(1) or m.group(2) or m.group(3))

sha_names = set(var_set) | set(var_read) | set(gvar_set) | set(gvar_read)
for v in sorted(x for x in sha_names if x):
    if (v in var_read or v in var_set) and v not in all_set and v not in all_gset:
        report('VAR', '/'.join([MOD, 'x']), f'variable `{v}` read but never set anywhere (read in {sorted(os.path.basename(x) for x in all_read.get(v, ()))})')
    if v in all_set and v not in all_read and v not in locvars:
        report('VAR', '/'.join([MOD, 'x']), f'variable `{v}` set but never read (set in {sorted(os.path.basename(x) for x in all_set[v])})')
    if v in all_gset and v in all_read and v not in all_gread:
        report('VAR', '/'.join([MOD, 'x']), f'`{v}` set as GLOBAL but read as country/state variable')
    if v in all_set and v in all_gread and v not in all_gset:
        report('VAR', '/'.join([MOD, 'x']), f'`{v}` set as scope variable but read as GLOBAL')

for fl in sorted(set(flags_cmp) | set(flags_set)):
    if flags_cmp[fl] and not flags_set[fl]:
        # may be set elsewhere via value = flag:x
        pass

order = {'PARSE': 0, 'CTX': 1, 'SCOPE': 2, 'UNKNOWN': 3, 'REF': 4, 'VAR': 5, 'LOC': 6}
seen = set()
for kind, f, msg in sorted(out, key=lambda x: (order.get(x[0], 9), x[1], x[2])):
    if (kind, f, msg) in seen: continue
    seen.add((kind, f, msg))
    print(f'[{kind}] {f}: {msg}')
print('files', len(FILES), 'issues', len(seen))

# ---------- pass 2: infer scripted trigger/effect scopes, then check call sites ----------
def infer(nodes, kind):
    acc = None
    for n in nodes or []:
        k = n.key
        if not k: continue
        if k in ('limit', 'AND', 'OR', 'NOT', 'NOR', 'NAND', 'trigger_if', 'trigger_else_if', 'trigger_else', 'if', 'else_if', 'else', 'hidden_effect', 'custom_tooltip'):
            sub = infer(n.children, kind)
        else:
            d = TRIG.get(k) if kind == 'trigger' else EFF.get(k)
            if d is None and kind == 'effect': d = TRIG.get(k) if False else None
            if d is None or not d['scopes'] or 'none' in d['scopes'] or k in ('save_scope_as', 'save_temporary_scope_as', 'custom_tooltip', 'trigger_event', 'set_variable', 'has_variable', 'remove_variable', 'change_variable', 'exists', 'always', 'this', 'debug_log', 'set_global_variable', 'has_global_variable'):
                continue
            sub = set(d['scopes'])
        if sub:
            acc = set(sub) if acc is None else (acc & sub)
    return acc

SDEF = {}
for f in FILES:
    fo = f.replace(chr(92), '/')
    if '/scripted_triggers/' in fo: kind = 'trigger'
    elif '/scripted_effects/' in fo: kind = 'effect'
    else: continue
    _, r = pdx.read(f)
    for top in r.children or []:
        if top.key:
            sc = infer(top.children, kind)
            if sc is not None and len(sc) <= 3:
                SDEF[top.key] = (kind, sc, f)
print('\n--- inferred scopes ---')
for k, (kind, sc, f) in sorted(SDEF.items()):
    print(f'{kind:7} {k}: {sorted(sc)}')

calls = []
_orig_walk = walk
def walk2(nodes, ctx, scope, root, prev, f, path):
    for n in nodes or []:
        if n.key in SDEF and scope is not UNKNOWN:
            kind, sc, df = SDEF[n.key]
            if scope not in sc:
                calls.append(f'[CALLSCOPE] {f.replace(MOD + "/", "")}: `{n.key}` (expects {sorted(sc)}) called in {scope} scope at {path}')
    return _orig_walk(nodes, ctx, scope, root, prev, f, path)
walk = walk2
out.clear()
for f in FILES:
    process(f)
print('\n--- call-site scope mismatches ---')
for c in sorted(set(calls)):
    print(c)
