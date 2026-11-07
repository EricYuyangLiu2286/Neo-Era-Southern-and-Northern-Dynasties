"""Prepare, apply and independently reproduce the approved localization review."""
import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path
import re
import runpy
import subprocess

HERE = Path(__file__).resolve().parent
AUDIT = HERE.parent
BASE = "9d6959a382a856f7b0bcfd0e098a207f11b3b14d"
DATA = HERE / "records.json"
inspect = runpy.run_path(str(AUDIT / "audit.py"))["inspect"]
TOKENS = re.compile(r"\[[^\[\]]+\]|\$[^$\n]+\$|#[\w;,:.-]+|#!|[+-]?\d+(?:[.,]\d+)*(?:%)?")
CHECKS = [
    "印度「诸邦之间」及「借法自强」：对照自治、独立、合邦来文，核对王公年金和土地、人民的管辖权。",
    "印度「南方的烽火」：依次悬停联络、暂停、恢复与举事，共用描述应适用于四种操作。",
    "日本「东洋交涉」：比较自治、独立、合邦和对外求援；停战与拨款期限在提案和答复中的时态应有区别。",
    "日本「机杼声中」：阅读工场雇佣与农户织造的叙述；对照同组「富足的生活」中的房租、米价和教育费用。",
    "法国「宫廷与外省」：核对王党或摄政期间的工程理由，再看五年评议对疆界可比州的统计与两档威望奖励。",
]

def load(path):
    return json.loads(path.read_bytes())

def write(path, content):
    tmp = path.with_name(path.name + ".tmp")
    tmp.write_bytes(content)
    tmp.replace(path)

def sha(raw):
    return hashlib.sha256(raw).hexdigest()

def git_file(repo, commit, rel):
    return subprocess.check_output(["git", "-C", str(repo), "show", f"{commit}:{rel}"])

def index(rows):
    result = {(e["file"], e["key"]): e for e in rows}
    assert len(result) == len(rows)
    return result

def render_file(raw, rel, rows):
    lang = rel.split("/")[1]
    lines, keys = inspect(raw, lang)
    for e in rows:
        if e["file"] != rel:
            continue
        key = e["key"]
        if e["previous"] is None:
            assert key not in keys and e["final"] is None
            continue
        pos, match = keys[key]
        assert match[3] == e["previous"], key
        assert TOKENS.findall(e["previous"]) == TOKENS.findall(e["final"]), key
        ending = lines[pos][len(lines[pos].rstrip("\r\n")):]
        lines[pos] = match[1] + e["final"] + match[4] + ending
    out = "".join(lines).encode("utf-8-sig")
    _, updated = inspect(out, lang)
    assert updated.keys() == keys.keys()
    for e in rows:
        if e["file"] == rel and e["final"] is not None:
            assert updated[e["key"]][1][3] == e["final"]
    return out

def prepare(mod, repo, decisions):
    old = load(AUDIT / "records.json")
    draft = index(load(decisions))
    assert draft.keys() == index(old["changes"]).keys()
    approved = index(load(HERE / "sample-10.json")["rows"])
    rows = []
    for e in old["changes"]:
        ident = (e["file"], e["key"])
        choice = draft[ident]
        if ident in approved:
            assert approved[ident]["proposed"] == choice["final"] and choice.get("approved")
        final = choice["final"]
        action = choice["action"]
        assert (action == "保留上轮稿") == (final == e["new"])
        assert action in ("保留上轮稿","恢复原文","局部修订","重写")
        if action == "恢复原文":
            assert final == e["old"]
        rows.append(dict(file=e["file"], key=e["key"], type=e["type"], severity=e["severity"],
                         original=e["old"], previous=e["new"], current=e["new"], final=final,
                         action=action, reason=choice["reason"], approved=ident in approved))
    files=[]
    for f in old["files"]:
        rel=f["file"]
        raw=(mod / rel).read_bytes()
        baseline=git_file(repo, BASE, rel)
        assert raw == baseline and sha(raw) == f["after"], f"Review concurrent changes in {rel}"
        after=render_file(raw, rel, rows)
        files.append(dict(file=rel, before=sha(raw), after=sha(after)))
    result=dict(baseline=BASE, files=files, rows=rows, previous_sync=old["sync"], spot_checks=CHECKS)
    serialized=(json.dumps(result, ensure_ascii=False, indent=2)+"\n").encode()
    write(DATA, serialized)

def apply(mod, repo, data):
    pending=[]
    for f in data["files"]:
        rel=f["file"]
        path=mod / rel
        actual=sha(path.read_bytes())
        if actual==f["after"]:
            continue
        assert actual==f["before"], f"Review concurrent changes in {rel}"
        raw=git_file(repo, data["baseline"], rel)
        updated=render_file(raw, rel, data["rows"])
        assert sha(updated)==f["after"]
        backup=HERE / "backup" / rel
        if not backup.exists():
            backup.parent.mkdir(parents=True, exist_ok=True)
            write(backup,raw)
        assert sha(backup.read_bytes())==actual
        pending.append((path,actual,updated))
    for path,expected,updated in pending:
        assert sha(path.read_bytes())==expected, path
        write(path,updated)

def verify(mod, repo, data, commit=None):
    sets={}
    for f in data["files"]:
        rel=f["file"]
        raw=git_file(repo, data["baseline"], rel)
        assert sha(raw)==f["before"]
        expected=render_file(raw, rel, data["rows"])
        assert sha(expected)==f["after"] and expected==(mod / rel).read_bytes(), rel
        if commit:
            assert expected==git_file(repo, commit, rel), rel
        stem,lang=Path(rel).stem.split("_l_")
        sets[(stem,lang)]=set(inspect(expected,lang)[1])
    for stem,lang in sets:
        assert sets[(stem,lang)]==sets[(stem,"english")]
    assert len(index(data["rows"]))==121
    for ident,sample in index(load(HERE / "sample-10.json")["rows"]).items():
        assert index(data["rows"])[ident]["final"]==sample["proposed"]
    print("Verified 121 records, 10 approved samples and 8 complete language files.")

def report(data):
    rows=data["rows"]
    actions=Counter(e["action"] for e in rows)
    counts=Counter(e["file"] for e in rows if e["previous"]!=e["final"])
    lines=["# NESND 玩家文本返工 · 2026-11-07", "",
           f"以提交 \x60{data['baseline'][:7]}\x60 及上轮 121 条记录为清单。复核了四组中英文文件。写入前，8 份主 MOD 文件逐字节与该提交一致。已确认的 10 条样稿均按原样定稿。",
           "", f"**实际修改 {sum(counts.values())} 条，涉及 {len(counts)} 份文件；复核保留 {actions['保留上轮稿']} 条，其中含已删除的 16 个中英文条目。** 恢复审核前原文 {actions['恢复原文']} 条，局部修订 {actions['局部修订']} 条，重写 {actions['重写']} 条。", "",
           "| 文件 | 复核条数 | 实际修改 | 复核保留 |", "|---|---:|---:|---:|"]
    for f in data["files"]:
        path=f["file"]
        n=sum(e["file"]==path for e in rows)
        lines.append(f"| \x60{path}\x60 | {n} | {counts[path]} | {n-counts[path]} |")
    lines+=["","问题类型和严重程度沿用首轮诊断。表中三版分别为审核前原文、上轮提交的文本、本次写入或保留的文本。波斯专档及共用文件中的波斯条目由外审负责。",""]
    def cell(value):
        if value is None:
            return "〔键已删除〕"
        return "\x60"+value.replace("|",r"\|")+"\x60"
    for f in data["files"]:
        path=f["file"]
        lines+=["## "+Path(path).name,"","| 键 | 问题／程度 | 审核前原文 | 上轮改文 | 本次定稿 | 处理 | 理由 |","|---|---|---|---|---|---|---|"]
        for e in rows:
            if e["file"]==path:
                lines.append("| "+" | ".join((cell(e["key"]),e["type"]+"／"+e["severity"],cell(e["original"]),cell(e["previous"]),cell(e["final"]),e["action"],e["reason"]))+" |")
        lines.append("")
    lines+=["## 上轮英文需同步清单","",f"原报告所列 {len(data['previous_sync'])} 键完整保留，供后续翻译使用。本次英文返工仅涉及上轮实际改过的句子。",""]
    lines.extend("- "+cell(k) for k in data["previous_sync"])
    lines+=["", "另记法国王党正文 `nesnd_court_royal_reason`。审核前英文称外省厂主亲自到场，确认的中文稿采用商会代表陈情。该英文人物叙述位于上轮未改过的句子，本轮仅修订上轮触及的结尾，人物称谓留待翻译同步。"]
    lines+=["","## 游戏外检查与实机抽查","","以审核基线逐字节重放改动，核对键集合、UTF-8 BOM、语言头、引号、动态函数、嵌套引用、数字与颜色，以及 10 条批准稿和 16 条已删记录。未启动游戏。",""]
    lines.extend("- "+s for s in data["spot_checks"])
    lines+=["","在本目录运行 \x60python rework.py report\x60 可由同目录的 \x60records.json\x60 重新生成报告。",""]
    write(HERE/"report.md","\n".join(lines).encode())

if __name__=="__main__":
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action",choices=["prepare","apply","verify","report"])
    parser.add_argument("--mod",type=Path,default=Path.cwd())
    parser.add_argument("--repo",type=Path)
    parser.add_argument("--decisions",type=Path,default=HERE/"decisions.json")
    parser.add_argument("--commit")
    args=parser.parse_args()
    if args.action=="prepare":
        prepare(args.mod,args.repo,args.decisions)
    elif args.action=="apply":
        apply(args.mod,args.repo,load(DATA))
    elif args.action=="verify":
        verify(args.mod,args.repo,load(DATA),args.commit)
    else:
        report(load(DATA))
