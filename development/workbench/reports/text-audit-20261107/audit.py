"""Record and verify individual Victoria 3 localization edits; regenerate report offline."""
import argparse
import codecs
from collections import Counter, defaultdict
from datetime import datetime, timezone
from hashlib import sha256
import json
from pathlib import Path
import re
import subprocess

HERE = Path(__file__).resolve().parent
DATA = HERE / "records.json"
ROW = re.compile(r'^(\s*([\w.-]+):\d*\s*")((?:\\.|[^"\\])*)(".*)$')
TOKEN = re.compile(r"\[[^\[\]]+\]|\$[^$\n]+\$|#[\w;,:.-]+|#!|[+-]?\d+(?:[.,]\d+)*(?:%)?")
GROUPS = ("技术错误", "AI 八股", "剧透", "机械性")
ACTIVE = {"nesnd_per_faith", "nesnd_per_rising", "nesnd_per_mines", "nesnd_per_tension", "nesnd_persia"}

def dump(path, obj):
    temp = path.with_suffix(".json.tmp")
    temp.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    temp.replace(path)

def digest(raw):
    return sha256(raw).hexdigest()

def git(repo, *args):
    return subprocess.check_output(["git", "-C", str(repo), *args])

def inspect(raw, lang):
    assert raw.startswith(codecs.BOM_UTF8), "BOM"
    lines = raw.decode("utf-8-sig").splitlines(keepends=True)
    assert lines[0].strip() == f"l_{lang}:"
    keys = {}
    for index, line in enumerate(lines[1:], 1):
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        match = ROW.fullmatch(line.rstrip("\r\n"))
        assert match and match[2] not in keys, f"line {index + 1}: {line}"
        keys[match[2]] = (index, match)
    return lines, keys

def capture(mod, repo):
    if DATA.exists():
        raise SystemExit("Existing frozen audit. Use report or verify.")
    previous = mod / ".scratch/debug-release/issues/68-description-spoilers.md"
    cutoff = previous.stat().st_mtime
    head = git(repo, "rev-parse", "HEAD").decode().strip()
    commits = git(repo, "log", "--all", "--format=%ct", "--name-only",
                  "--since=2026-11-07T00:00:00Z", "--", "localization").decode().splitlines()
    recent = {}
    stamp = 0
    for line in commits:
        if line.isdigit():
            stamp = int(line)
        elif line.startswith("localization/") and stamp > cutoff:
            recent[line] = max(stamp, recent.get(line, 0))
    result = dict(cutoff=datetime.fromtimestamp(cutoff, timezone.utc).isoformat(),
                  evidence=previous.relative_to(mod).as_posix(), git=head, files=[], skipped=[],
                  changes=[], uncertain=[], scripts=[], notes=[])
    tracked = set(git(repo, "ls-tree", "-r", "--name-only", head, "localization").decode().splitlines())
    for f in sorted((mod / "localization").rglob("nesnd_*.yml")):
        rel = f.relative_to(mod).as_posix()
        if rel not in recent and f.stat().st_mtime <= cutoff:
            continue
        raw = f.read_bytes()
        if rel in recent:
            basis = "Git 提交"
        elif rel not in tracked:
            basis = "Git 无此文件，取主 MOD 修改时间"
        else:
            committed = git(repo, "show", f"{head}:{rel}")
            if committed.replace(b"\r\n", b"\n") == raw.replace(b"\r\n", b"\n"):
                continue
            basis = "主 MOD 版本未提交，取主 MOD 修改时间"
        item = dict(file=rel, basis=basis, time=datetime.fromtimestamp(
            recent.get(rel, f.stat().st_mtime), timezone.utc).isoformat(), before=digest(raw))
        stem = f.name.split("_l_")[0]
        if stem in ACTIVE:
            result["skipped"].append(item)
            continue
        _, keys = inspect(raw, rel.split("/")[1])
        item["count"] = len(keys)
        result["files"].append(item)
        backup = HERE / "backup" / rel
        backup.parent.mkdir(parents=True, exist_ok=True)
        backup.write_bytes(raw)
    dump(DATA, result)

def transform(source, item, edits):
    lines, keys = inspect(source, item["file"].split("/")[1])
    for edit in edits:
        index, match = keys[edit["key"]]
        assert match[3] == edit["old"] and index + 1 == edit["line"]
        new = edit["new"]
        if new is None:
            assert edit["type"] == GROUPS[0]
            lines[index] = ""
            continue
        if edit["type"] != GROUPS[0]:
            assert TOKEN.findall(match[3]) == TOKEN.findall(new), edit["key"]
        ending = lines[index][len(lines[index].rstrip("\r\n")):]
        lines[index] = match[1] + new + match[4] + ending
    result = "".join(lines).encode("utf-8-sig")
    inspect(result, item["file"].split("/")[1])
    return result

def apply_plan(mod, plan_path):
    data = json.loads(DATA.read_text(encoding="utf-8"))
    if data["changes"]:
        install(mod, data)
        return
    plan = json.loads(plan_path.read_text(encoding="utf-8-sig"))
    by_file = defaultdict(list)
    keyset = set()
    for item in data["files"]:
        rel = item["file"]
        raw = (mod / rel).read_bytes()
        assert digest(raw) == item["before"], f"Concurrent change: {rel}"
        stem, lang = Path(rel).name.split("_l_")
        lang = lang[:-4]
        _, keys = inspect(raw, lang)
        for edit in plan["edits"]:
            if edit["stem"] != stem or lang not in edit["langs"]:
                continue
            key = edit["key"]
            assert (rel, key) not in keyset
            keyset.add((rel, key))
            index, match = keys[key]
            new = edit["new"]
            if "replace" in edit:
                old_part, new_part = edit["replace"]
                assert match[3].count(old_part) == 1
                new = match[3].replace(old_part, new_part)
            assert match[3] != new
            by_file[rel].append(dict(file=rel, key=key, line=index+1, type=edit["type"],
                                     severity=edit["severity"], old=match[3], new=new,
                                     reason=edit["reason"]))
    assert len(keyset) == sum(len(e["langs"]) for e in plan["edits"])
    outputs = {}
    for item in data["files"]:
        rel = item["file"]
        edits = sorted(by_file[rel], key=lambda e:e["line"])
        outputs[rel] = transform((HERE / "backup" / rel).read_bytes(), item, edits)
        item["after"] = digest(outputs[rel])
        data["changes"].extend(edits)
    for field in ("uncertain", "scripts", "notes"):
        data[field] = plan[field]
    data["sync"] = [e["key"] for e in data["changes"] if e["type"] != GROUPS[0] and
                    e["key"] in inspect(outputs[e["file"].replace("simp_chinese","english")], "english")[1]]
    dump(DATA, data)
    install(mod, data)

def install(mod, data):
    pending = {}
    for item in data["files"]:
        rel = item["file"]
        p = mod / rel
        actual = digest(p.read_bytes())
        if actual == item["after"]:
            continue
        assert actual == item["before"], f"Concurrent edit: {rel}"
        edits = [e for e in data["changes"] if e["file"] == rel]
        updated = transform(p.read_bytes(), item, edits)
        assert digest(updated) == item["after"]
        pending[p] = (actual, updated)
    for p, (expected, updated) in pending.items():
        tmp = p.with_suffix(".audit-tmp")
        tmp.write_bytes(updated)
        assert digest(p.read_bytes()) == expected, f"Concurrent edit: {p}"
        tmp.replace(p)

def verify(mod, data, game=None):
    by_language = {}
    for item in data["files"]:
        rel = item["file"]
        current = (mod / rel).read_bytes()
        assert digest(current) == item["after"], rel
        lang = rel.split("/")[1]
        _, keys = inspect(current, lang)
        by_language.setdefault(lang, {})[Path(rel).name.split("_l_")[0]] = keys
        backup = HERE / "backup" / rel
        if backup.exists():
            assert digest(backup.read_bytes()) == item["before"]
            assert transform(backup.read_bytes(), item, [e for e in data["changes"] if e["file"] == rel]) == current
    for stem, rows in by_language["english"].items():
        assert rows.keys() == by_language["simp_chinese"][stem].keys(), stem
    for lang, files in by_language.items():
        definitions = Counter()
        for f in (mod / "localization" / lang).rglob("*.yml"):
            definitions.update(re.findall(r"^\s*([\w.-]+):\d*\s*\"", f.read_text(encoding="utf-8-sig"), re.M))
        known = set(definitions)
        if game:
            folder = game / "localization" / lang
            assert folder.is_dir(), folder
            for f in folder.rglob("*.yml"):
                known.update(re.findall(r"^\s*([\w.-]+):\d*\s*\"", f.read_text(encoding="utf-8-sig"), re.M))
        for rows in files.values():
            for key, (_, match) in rows.items():
                value = match[3]
                assert definitions[key] == 1, key
                assert not re.search(r"TRIGGER_[A-Z_]+|国家没有相关变量", value), key
                assert not re.search(r"[\[\]]", re.sub(r"\[[^\[\]]+\]", "", value)), key
                for code in re.findall(r"\[([^\[\]]+)\]", value):
                    assert code.count("(") == code.count(")") and code.count("'") % 2 == 0, (key, code)
                level = 0
                for tag in re.findall(r"#!|#[A-Za-z_]+", value):
                    level += -1 if tag == "#!" else 1
                    assert level >= 0, key
                assert level == 0, key
                if game:
                    for ref in re.findall(r"\$([\w.-]+)(?:\|[^$]*)?\$", value):
                        assert ref in known, (key, ref)

def report(data):
    counts = Counter(e["type"] for e in data["changes"])
    lines = ["# NESND 本地化审核 · 2026-11-07", "",
             f"**审核界限**　{data['cutoff']}（伦敦，UTC+0；严格晚于）。任务 68 的两轮剧透审核均已记入 \x60{data['evidence']}\x60。该报告未署时分秒，采用最终落盘时间。备份目录中的两轮文件早于该时间。", "",
             f"Git 工作副本基线 \x60{data['git']}\x60。检查所有本地可见分支的提交者时间。游戏加载目录与 Git 分开；无提交的新增文件以及内容异于 Git 的本地版本用文件修改时间。仅换行不同视为同一版本。", "",
             "## 审核范围与计数", "", data["notes"][0], "",
             f"波斯另有 {data.get('deferred_count', 0)} 条工作底稿留作外审。下列表格只计算实际写入的修改。", "",
             "| 完整文件 | 审前键数 | 判定依据 | 时间（UTC） | 修改条数 |", "|---|---:|---|---|---:|"]
    for f in data["files"]:
        lines.append(f"| \x60{f['file']}\x60 | {f['count']} | {f['basis']} | {f['time']} | {sum(e['file']==f['file'] for e in data['changes'])} |")
    lines += ["", "每个语言文件中的一个键按一处计，按首要问题归类。一个废键在中英各删一次，计两处。", "",
              "、".join(f"**{g} {counts[g]} 处**" for g in GROUPS) + "。", ""]
    def cell(value):
        if value is None:
            return "〔删除此键〕"
        return value.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;").replace("|","&#124;").replace("[","&#91;").replace("]","&#93;").replace("_","&#95;").replace("$","&#36;")
    for g in GROUPS:
        lines += [f"## {g}（{counts[g]}）", "", "| 文件 | 键 | 原文 | 新文 | 理由 |", "|---|---|---|---|---|"]
        for e in data["changes"]:
            if e["type"] == g:
                lines.append(" | ".join(["| \x60"+Path(e["file"]).name+"\x60", "\x60"+e["key"]+"\x60",cell(e["old"]),cell(e["new"]),f"【{e['severity']}】{e['reason']} |"]))
        lines.append("")
    for title, items in [
        ("未确认的未使用键", data["uncertain"]), ("英文需同步", ["\x60"+k+"\x60" for k in data["sync"]]),
        ("跳过的文件", ["\x60"+i["file"]+"\x60　波斯专档，按作者最后指示留给外部代理复核。" for i in data["skipped"]]),
        ("发现的脚本问题", data["scripts"]), ("校验与抽查", data["notes"][1:])]:
        lines += ["## "+title, ""] + ["- "+s for s in items or ["无。"]] + [""]
    lines += ["在本目录运行 \x60python audit.py report\x60 即可由 \x60records.json\x60 重建本报告。使用 \x60python audit.py verify --mod \"主 MOD 路径\"\x60 核对各文件的交付指纹。", ""]
    (HERE / "report.md").write_bytes("\n".join(lines).encode("utf-8"))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", nargs="?", default="report", choices=("capture","apply","report","verify"))
    parser.add_argument("--mod", type=Path, default=Path.cwd())
    parser.add_argument("--repo", type=Path)
    parser.add_argument("--game", type=Path, help="Victoria 3/game directory; verify base-game localization references")
    parser.add_argument("--plan", type=Path)
    args = parser.parse_args()
    if args.action == "capture":
        capture(args.mod, args.repo)
    elif args.action == "apply":
        apply_plan(args.mod, args.plan)
    else:
        data = json.loads(DATA.read_text(encoding="utf-8"))
        if args.action == "verify":
            verify(args.mod, data, args.game)
        else:
            report(data)
