from cne_native_context import *
import re,difflib
for rel in json.loads(read(R/'native-source-hashes.json')):
    p=C/rel;s=read(p)
    clean=re.sub(r'(?m)^[ \t]+',lambda m:re.sub(r' +\t','\t',m.group()),s)
    assert shape(parse(s))==shape(parse(clean))
    if clean!=s:write(p,clean)
bm=man(B);cm=man(C)
patch={rel:cm[rel] for rel in json.loads(read(R/'patch-files.json'))}
dump(R/'patch-files.json',patch)
diff=''
for rel in patch:
    old=B/rel if (B/rel).exists() else G/rel
    diff+=''.join(difflib.unified_diff(read(old).splitlines(True) if old.exists() else [],read(C/rel).splitlines(True),fromfile=str(old),tofile=str(C/rel)))
(R/'gameplay.diff').write_text(diff,'utf-8')
v=json.loads(read(R/'final-validation.json'));v['gameplay_files']=patch;dump(R/'final-validation.json',v)
print('Native indent whitespace normalized; ordered AST unchanged')
