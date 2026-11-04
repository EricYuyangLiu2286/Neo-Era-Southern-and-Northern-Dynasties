from pathlib import Path
p=Path(r"D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/tools/test_a2_source_effects_20261104.py")
text=p.read_text().split("results=[]")[0].replace("batch-a2-test-config.json","batch-c2-test-config.json")
text=text.replace('elif k=="floor":acc=math.floor(acc)','elif k=="ceiling":acc=math.ceil(acc)\n   elif k=="floor":acc=math.floor(acc)')
text=text.replace('if target is None:raise AssertionError(("UNSUPPORTED value",k))','if target is None:\n     if x.op=="?=":continue\n     raise AssertionError(("UNSUPPORTED value",k))')
Path(r"D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/tools/c2_source_adapter_20261104.py").write_text(text)

