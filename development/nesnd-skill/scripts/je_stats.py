"""Shape statistics for journal entries: lines, outcomes, buttons, bars, timeout, pulses, random events.
Usage: python je_stats.py "<vanilla glob>" "<author glob>" "<mod glob>"
Counts are structural only; they do not judge quality."""
import re,sys,glob,statistics as st,os
def blocks(path):
    txt=open(path,encoding='utf-8-sig',errors='replace').read()
    lines=txt.split('\n');out=[];d=0;name=None
    for i,l in enumerate(lines):
        s=re.sub(r'#.*','',l)
        if d==0:
            m=re.match(r'\s*(@?[\w\.]+)\s*=\s*\{',s)
            if m and not m.group(1).startswith('@'): name=m.group(1);start=i
        d+=s.count('{')-s.count('}')
        if d==0 and name:
            out.append((name,'\n'.join(re.sub(r'#.*','',x) for x in lines[start:i+1])));name=None
    return out
def stats(files):
    R=[]
    for f in files:
        for n,b in blocks(f):
            if 'outcome' not in b and 'complete' not in b and 'scripted_button' not in b: continue
            c=lambda p: len(re.findall(p,b,re.M))
            R.append(dict(name=n,lines=b.count('\n')+1,
              outcomes=c(r'\boutcome\s*=')+c(r'^\s*(complete|fail|invalid)\s*=\s*\{'),
              hidden_inv=c(r'hidden\s+invalid_outcome')+c(r'^\s*invalid\s*='),
              buttons=c(r'scripted_button\s*='),bars=c(r'scripted_progress_bar\s*=')+c(r'progressbar\s*=\s*yes'),
              timeout=c(r'^\s*timeout\s*='),pulses=c(r'on_(weekly|monthly|yearly)_pulse'),
              randev=c(r'random_events'),helpers=c(r'\b\w+\s*=\s*yes\b')-c(r'\b(always|popup|hidden|default_\w+|progressbar|highlight|is_\w+|has_\w+|exists|should_\w+|can_\w+|transferable|display_\w+|\w+_trigger|\w+_live|\w+ruler_is\w*)\s*=\s*yes'),
              custom_tt=c(r'custom_tooltip'),safe=c(r'\?=')))
    return R
def summarize(label,R):
    if not R: print(label,'none');return
    keys=['lines','outcomes','buttons','bars','timeout','pulses','randev','custom_tt','safe']
    print(f"{label}: {len(R)} JEs")
    for k in keys:
        v=[r[k] for r in R]
        print(f"  {k:9s} median {st.median(v):5.1f}  p90 {sorted(v)[int(len(v)*0.9)-1 if len(v)>1 else 0]:4}  max {max(v):4}  share>0 {sum(1 for x in v if x)/len(v):.0%}")
if __name__=='__main__':
    for label,pat in [('VANILLA 1.15',sys.argv[1]),('AUTHOR ce_ (original 20261030)',sys.argv[2]),('GPT nesnd_ (current)',sys.argv[3])]:
        summarize(label,stats(glob.glob(pat)))
