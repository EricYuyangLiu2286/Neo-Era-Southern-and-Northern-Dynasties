# NESND 部署：源目录 -> MOD 文件夹。由 deploy.bat 调用。
#   deploy  部署：清空 MOD 文件夹，按白名单复制运行文件，写入新版本号
#   preview 预览：只列出将删除、将复制的内容和版本号检查结果，不改任何文件
#   check   检查：只核对两边版本号与 update_record.json 最后一条记录
#   deploy 与 check 结束时都会列出源目录里尚未提交到 Git 的文件，并标出哪些已经在 MOD 文件夹里。
#   部署不提交、也不因未提交而停止：做到一半先部署测试是正常的。它只负责把这件事说出来。
#   force   版本号不一致时，经你逐字确认后仍然部署（会删掉 MOD 文件夹里的全部改动）
#   menu    双击时的菜单
# 退出码：0 成功/一致；1 检查不一致；2 前置检查未通过（未删除任何东西）；3 部署中途出错
param([ValidateSet('menu', 'deploy', 'preview', 'check', 'force')][string]$Mode = 'menu')

$ErrorActionPreference = 'Stop'
Set-StrictMode -Version 2
[Console]::OutputEncoding = New-Object System.Text.UTF8Encoding $false
$OutputEncoding = [Console]::OutputEncoding

# ---------- 固定路径：逐字比对，不要改成相对路径或变量拼接 ----------
$SOURCE = 'D:\Users\Eric Liu\Documents\Paradox Interactive\Victoria 3\nesnd-source'
$TARGET = 'D:\Users\Eric Liu\Documents\Paradox Interactive\Victoria 3\mod\Neo-Era Southern and Northern Dynasties'
$TARGET_PARENT = 'D:\Users\Eric Liu\Documents\Paradox Interactive\Victoria 3\mod'
$TARGET_LEAF = 'Neo-Era Southern and Northern Dynasties'
$LOG_DIR = 'D:\Users\Eric Liu\Documents\Paradox Interactive\Victoria 3\nesnd-workbench\reports\deploy-logs'
$WHITELIST = Join-Path $PSScriptRoot 'deploy-whitelist.txt'
$VERSION_FILE = 'nesnd_deploy_version.txt'
$RECORD_FILE = 'update_record.json'
$CONTENT_DIRS = @('common', 'events', 'gfx', 'gui', 'localization', 'map_data')
$PROCESSES = @('victoria3', 'Paradox Launcher', 'dowser', 'bootstrapper-v2')
$UTF8 = New-Object System.Text.UTF8Encoding $false

$script:Log = New-Object System.Text.StringBuilder
$script:Step = '-'
$script:TargetState = '未改动'
$script:RerunHint = '修正问题后重新运行 deploy.bat。'

function Say([string]$Text, [string]$Color = 'Gray') {
    Write-Host $Text -ForegroundColor $Color
    [void]$script:Log.AppendLine($Text)
}
function Note([string]$Text) { [void]$script:Log.AppendLine($Text) }   # 只写日志
function Save-Log([string]$Kind) {
    try {
        [void][IO.Directory]::CreateDirectory($LOG_DIR)
        $p = Join-Path $LOG_DIR ('{0}-{1}.txt' -f $Kind, (Get-Date -Format 'yyyyMMdd-HHmmss'))
        [IO.File]::WriteAllText($p, $script:Log.ToString(), $UTF8)
        Write-Host "日志：$p" -ForegroundColor DarkGray
    } catch { Write-Host "日志未能保存：$($_.Exception.Message)" -ForegroundColor DarkYellow }
}
class StopDeploy : System.Exception { StopDeploy([string]$m) : base($m) {} }
function Stop-Here([string]$Message) { throw [StopDeploy]::new($Message) }

function Get-Sha([string]$Path) {
    $sha = [Security.Cryptography.SHA256]::Create()
    $fs = [IO.File]::OpenRead($Path)
    try { return ([BitConverter]::ToString($sha.ComputeHash($fs))).Replace('-', '') } finally { $fs.Dispose(); $sha.Dispose() }
}
function Get-Rel([string]$Root, [string]$Full) { return $Full.Substring($Root.Length + 1).Replace('\', '/') }

# ---------- 白名单 ----------
function ConvertTo-GlobRegex([string]$Glob) {
    $g = $Glob.Replace('\', '/'); $sb = New-Object System.Text.StringBuilder '^'
    $i = 0
    while ($i -lt $g.Length) {
        if ($g.Substring($i).StartsWith('**/')) { [void]$sb.Append('(?:.*/)?'); $i += 3 }
        elseif ($g.Substring($i).StartsWith('**')) { [void]$sb.Append('.*'); $i += 2 }
        elseif ($g[$i] -eq '*') { [void]$sb.Append('[^/]*'); $i++ }
        elseif ($g[$i] -eq '?') { [void]$sb.Append('[^/]'); $i++ }
        else { [void]$sb.Append([regex]::Escape([string]$g[$i])); $i++ }
    }
    [void]$sb.Append('$')
    return New-Object regex ($sb.ToString(), 'IgnoreCase, CultureInvariant')
}
function Read-Whitelist {
    if (-not (Test-Path -LiteralPath $WHITELIST -PathType Leaf)) { Stop-Here "找不到白名单：$WHITELIST" }
    $rules = @(); $n = 0
    foreach ($line in [IO.File]::ReadAllLines($WHITELIST, $UTF8)) {
        $n++
        $t = ($line -replace '\s+#.*$', '').Trim()
        if ($t -eq '' -or $t.StartsWith('#')) { continue }
        $parts = $t -split '\s+', 2
        if ($parts.Count -ne 2 -or $parts[0] -notin @('include', 'exclude', 'doubt')) { Stop-Here "白名单第 $n 行无法识别：$line" }
        $rules += [pscustomobject]@{ Kind = $parts[0]; Glob = $parts[1]; Regex = (ConvertTo-GlobRegex $parts[1]); Line = $n }
    }
    if (-not ($rules | Where-Object Kind -eq 'include')) { Stop-Here '白名单里没有 include 规则' }
    return $rules
}
function Get-Plan($Rules) {
    $deploy = New-Object System.Collections.Generic.List[string]
    $doubt = New-Object System.Collections.Generic.List[object]
    $skipped = New-Object System.Collections.Generic.List[object]
    $byKind = @{}
    foreach ($k in 'doubt', 'exclude', 'include') { $byKind[$k] = @($Rules | Where-Object Kind -eq $k) }
    foreach ($f in [IO.Directory]::EnumerateFiles($SOURCE, '*', [IO.SearchOption]::AllDirectories)) {
        $rel = Get-Rel $SOURCE $f
        if ($rel.StartsWith('.git/')) { $skipped.Add([pscustomobject]@{ Rel = $rel; Why = 'Git 数据' }); continue }
        $hit = $null; foreach ($r in $byKind['doubt']) { if ($r.Regex.IsMatch($rel)) { $hit = $r; break } }
        if ($hit) { $doubt.Add([pscustomobject]@{ Rel = $rel; Why = "存疑（白名单第 $($hit.Line) 行 $($hit.Glob)）" }); continue }
        foreach ($r in $byKind['exclude']) { if ($r.Regex.IsMatch($rel)) { $hit = $r; break } }
        if ($hit) { $skipped.Add([pscustomobject]@{ Rel = $rel; Why = "排除（白名单第 $($hit.Line) 行 $($hit.Glob)）" }); continue }
        foreach ($r in $byKind['include']) { if ($r.Regex.IsMatch($rel)) { $hit = $r; break } }
        if ($hit) { $deploy.Add($rel) } else { $skipped.Add([pscustomobject]@{ Rel = $rel; Why = '不匹配任何 include' }) }
    }
    $deploy.Sort([StringComparer]::Ordinal)
    return [pscustomobject]@{ Deploy = $deploy; Doubt = $doubt; Skipped = $skipped }
}

# ---------- 版本号 ----------
function Read-Text([string]$Path) {
    if (Test-Path -LiteralPath $Path -PathType Leaf) { return [IO.File]::ReadAllText($Path, $UTF8).Trim() } else { return $null }
}
function Read-Records {
    $p = Join-Path $SOURCE $RECORD_FILE
    if (-not (Test-Path -LiteralPath $p -PathType Leaf)) { return [pscustomobject]@{ Exists = $false; Text = $null; Items = @() } }
    $text = [IO.File]::ReadAllText($p, $UTF8)
    if (-not $text.Trim().StartsWith('[')) { Stop-Here "$RECORD_FILE 不是 JSON 数组，无法核对" }
    try { $parsed = $text | ConvertFrom-Json } catch { Stop-Here "$RECORD_FILE 无法解析：$($_.Exception.Message)" }
    $items = @(); foreach ($x in $parsed) { $items += $x }
    return [pscustomobject]@{ Exists = $true; Text = $text; Items = $items }
}
function Get-VersionState {
    $src = Read-Text (Join-Path $SOURCE $VERSION_FILE)
    $tgt = Read-Text (Join-Path $TARGET $VERSION_FILE)
    $rec = Read-Records
    $last = $null; if ($rec.Items.Count -gt 0) { $last = [string]$rec.Items[-1].version }
    if ($null -eq $src -and $null -eq $tgt -and $rec.Items.Count -eq 0) { $state = 'first' }
    elseif ($src -and $tgt -and $last -and $src -ceq $tgt -and $tgt -ceq $last) { $state = 'ok' }
    else { $state = 'mismatch' }
    return [pscustomobject]@{ State = $state; Source = $src; Target = $tgt; Last = $last; Records = $rec }
}
function Show-Versions($V, [int]$Count = 5) {
    $na = '（无）'
    Say ("  MOD 文件夹版本号      : {0}" -f $(if ($V.Target) { $V.Target } else { $na }))
    Say ("  源目录版本号          : {0}" -f $(if ($V.Source) { $V.Source } else { $na }))
    Say ("  update_record 最后一条: {0}" -f $(if ($V.Last) { $V.Last } else { $na }))
    $items = $V.Records.Items
    if ($items.Count -gt 0) {
        Say "  最近 $([Math]::Min($Count, $items.Count)) 条记录（共 $($items.Count) 条，最新在下）："
        foreach ($r in ($items | Select-Object -Last $Count)) {
            $uc = $r.PSObject.Properties['uncommitted_files']   # 2026-11-20 起才有这一项
            $ucText = $(if ($uc -and [int]$uc.Value -gt 0) { "  部署时未提交 $($uc.Value) 个" } elseif ($uc -and [int]$uc.Value -lt 0) { '  部署时未能读取 Git 状态' } else { '' })
            Say ("    {0}  {1}  HEAD {2}  {3} 个文件{4}" -f $r.deployed_at, $r.version, $r.source_git_head, $r.file_count, $ucText)
        }
    }
}
function Show-MismatchWarning($V) {
    Say ''
    Say '！！警告：版本号不一致。' Red
    Say '上次部署之后，MOD 文件夹可能被直接修改过，或者上次部署没有完成。' Red
    Say '继续部署会删掉 MOD 文件夹里的这些改动。本次没有删除任何东西。' Red
    Show-Versions $V 5
    Say '请先查看 MOD 文件夹与 update_record.json，决定如何处理；确认 MOD 文件夹里没有需要保留的改动后，才可运行 deploy.bat force。' Yellow
}
function Write-VersionCheck($V) {
    switch ($V.State) {
        'ok' { Say "版本号一致：$($V.Target)" Green }
        'first' { Say '首次部署：两边都还没有版本号，update_record.json 尚无记录（例外，允许部署）。' Yellow }
        default { Say '版本号不一致。' Red }
    }
}

# ---------- 检查项 ----------
function Test-Processes {
    $running = @(Get-Process -ErrorAction SilentlyContinue | Where-Object { $PROCESSES -contains $_.ProcessName })
    return $running
}
function Test-Source {
    $problems = @()
    if (-not (Test-Path -LiteralPath $SOURCE -PathType Container)) { return @("源目录不存在：$SOURCE") }
    $meta = Join-Path $SOURCE '.metadata\metadata.json'
    if (-not (Test-Path -LiteralPath $meta -PathType Leaf)) { $problems += '源目录缺少 .metadata\metadata.json' }
    else {
        try { $m = [IO.File]::ReadAllText($meta, $UTF8) | ConvertFrom-Json; if ($m.name -ne $TARGET_LEAF) { $problems += "metadata.json 的 name 不是 $TARGET_LEAF" } }
        catch { $problems += "metadata.json 无法解析：$($_.Exception.Message)" }
    }
    foreach ($d in $CONTENT_DIRS) { if (-not (Test-Path -LiteralPath (Join-Path $SOURCE $d) -PathType Container)) { $problems += "源目录缺少内容目录 $d" } }
    return $problems
}
function Test-Target {
    $problems = @()
    $full = [IO.Path]::GetFullPath($TARGET)
    if (-not [string]::Equals($full, 'D:\Users\Eric Liu\Documents\Paradox Interactive\Victoria 3\mod\Neo-Era Southern and Northern Dynasties', [StringComparison]::Ordinal)) { $problems += "目标路径与写死的 MOD 文件夹路径不一致：$full" }
    if (-not [string]::Equals([IO.Path]::GetDirectoryName($full), $TARGET_PARENT, [StringComparison]::Ordinal)) { $problems += '目标的上级目录不是文档下的 mod 文件夹' }
    if (-not [string]::Equals([IO.Path]::GetFileName($full), $TARGET_LEAF, [StringComparison]::Ordinal)) { $problems += '目标文件夹名不是本 MOD' }
    $s = [IO.Path]::GetFullPath($SOURCE).TrimEnd('\') + '\'; $t = $full.TrimEnd('\') + '\'
    if ($s.StartsWith($t, [StringComparison]::OrdinalIgnoreCase) -or $t.StartsWith($s, [StringComparison]::OrdinalIgnoreCase)) { $problems += '源目录与 MOD 文件夹互相包含' }
    if (-not (Test-Path -LiteralPath $full -PathType Container)) { $problems += "MOD 文件夹不存在：$full（首次部署前请手动新建这个空文件夹）" }
    else {
        $item = Get-Item -LiteralPath $full -Force
        if ($item.Attributes -band [IO.FileAttributes]::ReparsePoint) { $problems += 'MOD 文件夹本身是目录连接或符号链接，拒绝清空' }
        $links = @(Get-ChildItem -LiteralPath $full -Recurse -Force -ErrorAction Stop | Where-Object { $_.Attributes -band [IO.FileAttributes]::ReparsePoint })
        if ($links.Count) { $problems += "MOD 文件夹内有 $($links.Count) 个目录连接或符号链接（如 $($links[0].FullName)），拒绝清空" }
    }
    return $problems
}
function Get-TargetListing {
    if (-not (Test-Path -LiteralPath $TARGET -PathType Container)) { return @() }
    return @(Get-ChildItem -LiteralPath $TARGET -Recurse -Force -File | ForEach-Object { Get-Rel $TARGET $_.FullName } | Sort-Object)
}
function Group-Top([string[]]$Rels) {
    $Rels | Group-Object { if ($_.Contains('/')) { $_.Split('/')[0] + '/' } else { $_ } } | Sort-Object Name |
        ForEach-Object { Say ("    {0,-28} {1,6}" -f $_.Name, $_.Count) }
}
function Get-GitHead {
    $h = & git -C $SOURCE rev-parse HEAD 2>$null
    if ($LASTEXITCODE -ne 0 -or -not $h) { Stop-Here '读取源目录的 Git HEAD 失败' }
    return $h.Trim()
}

# ---------- 未提交的改动 ----------
# 部署只复制文件，不提交。这里列出源目录里 Git 尚未提交的文件，并标出哪些已经原样在 MOD 文件夹里。
# 版本号文件与 update_record.json 已列入 .git/info/exclude，不会出现在这里。
function Get-Uncommitted {
    $lines = @(& git -C $SOURCE -c core.quotepath=false status --porcelain --untracked-files=all 2>$null)
    if ($LASTEXITCODE -ne 0) { return $null }
    $items = @()
    foreach ($l in $lines) {
        if (-not $l -or $l.Length -lt 4) { continue }
        $rel = $l.Substring(3)
        $arrow = $rel.IndexOf(' -> '); if ($arrow -ge 0) { $rel = $rel.Substring($arrow + 4) }
        $rel = $rel.Trim('"')
        $src = Join-Path $SOURCE $rel; $tgt = Join-Path $TARGET $rel
        $deployed = $false
        if ((Test-Path -LiteralPath $src -PathType Leaf) -and (Test-Path -LiteralPath $tgt -PathType Leaf)) { $deployed = ((Get-Sha $src) -eq (Get-Sha $tgt)) }
        $items += [pscustomobject]@{ Rel = $rel; Deployed = $deployed }
    }
    return , $items
}
function Show-Uncommitted([bool]$AfterDeploy) {
    $u = Get-Uncommitted
    if ($null -eq $u) { Say '未能读取源目录的 Git 状态，无法判断是否有未提交的改动。' Yellow; return }
    $u = @($u)
    if ($u.Count -eq 0) { Say '源目录没有未提交的改动。' Green; return }
    $dep = @($u | Where-Object { $_.Deployed })
    Say ''
    Say "！！提醒：源目录有 $($u.Count) 个文件尚未提交到 Git，其中 $($dep.Count) 个已经在 MOD 文件夹里（已部署、未提交）。" Yellow
    foreach ($x in ($u | Select-Object -First 20)) { Say ("    {0}  {1}" -f $(if ($x.Deployed) { '已部署' } else { '未部署' }), $x.Rel) Yellow }
    if ($u.Count -gt 20) { Say "    ……另有 $($u.Count - 20) 个，运行 git status 查看全部。" Yellow }
    if ($AfterDeploy) { Say '任务做完后把本任务的改动提交到 Git；交付时写明提交号，或写明还有哪些文件没有提交。' Yellow }
    else { Say '这些若是本任务正在改的文件，做完后提交；若是别的任务留下的，先告诉作者，不要代为提交或回退。' Yellow }
}

# ---------- 记录 ----------
function ConvertTo-JsonString([string]$s) {
    $sb = New-Object System.Text.StringBuilder '"'
    foreach ($c in $s.ToCharArray()) {
        switch ($c) { '"' { [void]$sb.Append('\"') } '\' { [void]$sb.Append('\\') } default {
            if ([int]$c -lt 32) { [void]$sb.AppendFormat('\u{0:x4}', [int]$c) } else { [void]$sb.Append($c) } } }
    }
    return $sb.Append('"').ToString()
}
function Add-Record([string]$Version, [string]$Head, [int]$Count, $Before, [int]$Uncommitted) {
    $p = Join-Path $SOURCE $RECORD_FILE
    $entry = "  {`n" +
        "    `"deployed_at`": $(ConvertTo-JsonString (Get-Date -Format 'yyyy-MM-ddTHH:mm:sszzz')),`n" +
        "    `"version`": $(ConvertTo-JsonString $Version),`n" +
        "    `"mod_folder`": $(ConvertTo-JsonString $TARGET),`n" +
        "    `"source_git_head`": $(ConvertTo-JsonString $Head),`n" +
        "    `"file_count`": $Count,`n" +
        "    `"uncommitted_files`": $Uncommitted`n  }"
    if (-not $Before.Exists) { $prefix = "[`n"; $new = $prefix + $entry + "`n]`n" }
    else {
        $old = $Before.Text; $cut = $old.LastIndexOf(']')
        if ($cut -lt 0) { Stop-Here "$RECORD_FILE 缺少结尾的 ]" }
        $prefix = $old.Substring(0, $cut).TrimEnd()
        $sep = $(if ($Before.Items.Count -gt 0) { ",`n" } else { "`n" })
        $new = $prefix + $sep + $entry + "`n]`n"
    }
    [IO.File]::WriteAllText($p, $new, $UTF8)
    $after = Read-Records
    if (-not ([IO.File]::ReadAllText($p, $UTF8)).StartsWith($prefix, [StringComparison]::Ordinal)) { Stop-Here "$RECORD_FILE 的旧记录被改动" }
    if ($after.Items.Count -ne $Before.Items.Count + 1 -or [string]$after.Items[-1].version -cne $Version) { Stop-Here "$RECORD_FILE 追加后核对失败" }
}

# ---------- 模式 ----------
function Invoke-Check {
    Say '== 检查：版本号' Cyan
    $v = Get-VersionState
    Show-Versions $v 5
    if ($v.State -eq 'ok') { Say '三者一致。' Green; Show-Uncommitted $false; return 0 }
    if ($v.State -eq 'first') { Say '尚未部署过（两边都没有版本号，也没有记录）。' Yellow; return 1 }
    Show-MismatchWarning $v
    Show-Uncommitted $false
    return 1
}

function Invoke-Preview {
    Say '== 预览（不改动任何文件）' Cyan
    $p = @(Test-Processes)
    if ($p.Count) { Say ("a. 游戏或启动器正在运行：{0}。实际部署会提示后继续。" -f (($p | ForEach-Object { "$($_.ProcessName)($($_.Id))" }) -join '、')) Yellow }
    else { Say 'a. 游戏和启动器均已关闭。' Green }
    $sp = @(Test-Source); if ($sp.Count) { $sp | ForEach-Object { Say "b. $_" Red } } else { Say 'b. 源目录检查通过。' Green }
    $tp = @(Test-Target); if ($tp.Count) { $tp | ForEach-Object { Say "c. $_" Red } } else { Say "c. 目标路径核对通过：$TARGET" Green }
    $v = Get-VersionState
    Say 'd. 版本号检查：'; Show-Versions $v 5; Write-VersionCheck $v
    if ($v.State -eq 'mismatch') { Show-MismatchWarning $v }
    if ($sp.Count) { return 2 }
    $rules = Read-Whitelist; $plan = Get-Plan $rules
    $del = @(Get-TargetListing)
    Say ''
    Say "e. 将删除 MOD 文件夹内全部 $($del.Count) 个文件（及所有子文件夹），按顶层分组：" Cyan
    if ($del.Count) { Group-Top $del }
    Say "f. 将从源目录复制 $($plan.Deploy.Count) 个运行文件，按顶层分组：" Cyan
    Group-Top $plan.Deploy
    Say "h. 将生成新版本号，写入 MOD 文件夹与源目录的 $VERSION_FILE，并追加 $RECORD_FILE。"
    $inContent = @($plan.Skipped | Where-Object { $r = $_.Rel; $CONTENT_DIRS + @('.metadata') | Where-Object { $r.StartsWith("$_/") } })
    Say ''
    Say "内容目录中不部署的文件（$($inContent.Count) 个）：" Cyan
    foreach ($x in $inContent) { Say "    $($x.Rel)   —— $($x.Why)" }
    Say "存疑、不部署（$($plan.Doubt.Count) 个）：" Yellow
    foreach ($x in $plan.Doubt) { Say "    $($x.Rel)   —— $($x.Why)" Yellow }
    $rootSkipped = @($plan.Skipped | Where-Object { $r = $_.Rel; -not ($CONTENT_DIRS + @('.metadata') | Where-Object { $r.StartsWith("$_/") }) } | ForEach-Object Rel)
    Say "内容目录之外不部署的开发资料（$($rootSkipped.Count) 个），按顶层分组：" Cyan
    Group-Top $rootSkipped
    Note ''; Note '---- 将删除的文件（MOD 文件夹现有内容）----'; $del | ForEach-Object { Note "D $_" }
    Note ''; Note '---- 将复制的文件 ----'; $plan.Deploy | ForEach-Object { Note "C $_" }
    Note ''; Note '---- 不部署的文件 ----'; $plan.Skipped | ForEach-Object { Note "S $($_.Rel)  ($($_.Why))" }
    Say '完整清单见日志。没有改动任何文件。' Green
    return 0
}

function Invoke-Deploy([bool]$Force) {
    Say "== 部署$(if ($Force) { '（force）' })  $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')" Cyan
    $script:Step = 'a'
    $p = @(Test-Processes)
    # The author confirmed on 2026-11-14 that deploying under a running game does not crash it; warn only.
    if ($p.Count) { Say ("a. 游戏或启动器正在运行：{0}。继续部署，新内容在下次启动游戏时生效。" -f (($p | ForEach-Object { "$($_.ProcessName)($($_.Id))" }) -join '、')) Yellow }
    else { Say 'a. 游戏和启动器均已关闭。' Green }

    $script:Step = 'b'
    $sp = @(Test-Source); if ($sp.Count) { Stop-Here ($sp -join '；') }
    $rules = Read-Whitelist
    $head = Get-GitHead
    $plan = Get-Plan $rules
    if (-not $plan.Deploy.Contains('.metadata/metadata.json')) { Stop-Here '白名单没有选中 .metadata/metadata.json' }
    Say "b. 源目录检查通过；将部署 $($plan.Deploy.Count) 个文件；源目录 HEAD $head。" Green

    $script:Step = 'c'
    $tp = @(Test-Target); if ($tp.Count) { Stop-Here ($tp -join '；') }
    Say "c. 目标路径核对通过：$TARGET" Green

    $script:Step = 'd'
    $v = Get-VersionState
    Show-Versions $v 5
    Write-VersionCheck $v
    if ($v.State -eq 'mismatch') {
        Show-MismatchWarning $v
        if (-not $Force) { Stop-Here '版本号不一致，部署已停止，没有删除任何东西。' }
        Say ''
        Say "force：将清空 $TARGET 中的全部内容。确认 MOD 文件夹里没有需要保留的改动后，输入大写 DELETE 继续，其他任何输入都会取消。" Red
        if ((Read-Host '确认') -cne 'DELETE') { Stop-Here '未确认，已取消。没有删除任何东西。' }
        Note 'force 已确认（输入 DELETE）。'
    }

    # 复制前先算好源文件哈希；源目录中的文件只读不改
    $srcHash = @{}
    foreach ($rel in $plan.Deploy) { $srcHash[$rel] = Get-Sha (Join-Path $SOURCE $rel) }

    $script:Step = 'e'
    $script:TargetState = '正在清空（部分文件可能已删除）'
    $script:RerunHint = '版本号已无法对上，常规部署会在第 d 步停止。确认 MOD 文件夹里没有需要保留的改动后，运行 deploy.bat force。'
    $prefix = $TARGET.TrimEnd('\') + '\'
    # 先删版本号文件：之后任何中断都会在下次第 d 步表现为版本号不一致
    $tv = Join-Path $TARGET $VERSION_FILE
    if (Test-Path -LiteralPath $tv -PathType Leaf) { (Get-Item -LiteralPath $tv -Force).Attributes = [IO.FileAttributes]::Normal; [IO.File]::Delete($tv) }
    foreach ($it in @(Get-ChildItem -LiteralPath $TARGET -Force)) {
        if (-not $it.FullName.StartsWith($prefix, [StringComparison]::Ordinal)) { Stop-Here "拒绝删除 MOD 文件夹之外的路径：$($it.FullName)" }
        if ($it.Attributes -band [IO.FileAttributes]::ReparsePoint) { Stop-Here "拒绝删除链接：$($it.FullName)" }
        if ($it.PSIsContainer) {
            Get-ChildItem -LiteralPath $it.FullName -Recurse -Force | ForEach-Object {
                $_.Attributes = $(if ($_.PSIsContainer) { [IO.FileAttributes]::Directory } else { [IO.FileAttributes]::Normal }) }
            $it.Attributes = [IO.FileAttributes]::Directory
            [IO.Directory]::Delete($it.FullName, $true)
        } else {
            $it.Attributes = [IO.FileAttributes]::Normal
            [IO.File]::Delete($it.FullName)
        }
    }
    $left = @(Get-ChildItem -LiteralPath $TARGET -Force)
    if ($left.Count) { Stop-Here "清空后仍有 $($left.Count) 项残留，如 $($left[0].FullName)" }
    $script:TargetState = '已清空，尚未复制'
    Say 'e. MOD 文件夹已清空（文件夹本身保留）。' Green

    $script:Step = 'f'
    $n = 0; $total = $plan.Deploy.Count
    foreach ($rel in $plan.Deploy) {
        $dst = Join-Path $TARGET $rel
        [void][IO.Directory]::CreateDirectory([IO.Path]::GetDirectoryName($dst))
        [IO.File]::Copy((Join-Path $SOURCE $rel), $dst, $false)
        $n++; $script:TargetState = "已清空，复制未完成（已复制 $n / $total）"
    }
    $script:TargetState = '运行文件已复制，尚未核对，版本号尚未写入'
    Say "f. 已复制 $n 个文件。" Green

    $script:Step = 'g'
    $bad = @()
    foreach ($rel in $plan.Deploy) { if ((Get-Sha (Join-Path $TARGET $rel)) -ne $srcHash[$rel]) { $bad += $rel } }
    if ($bad.Count) { Stop-Here "$($bad.Count) 个文件哈希不一致，如 $($bad[0])" }
    $present = @(Get-TargetListing)
    if ($present.Count -ne $total) { Stop-Here "MOD 文件夹中有 $($present.Count) 个文件，应为 $total 个" }
    foreach ($rel in $plan.Deploy) { if ((Get-Sha (Join-Path $SOURCE $rel)) -ne $srcHash[$rel]) { Stop-Here "部署期间源文件被修改：$rel" } }
    $mS = [IO.File]::ReadAllText((Join-Path $SOURCE '.metadata\metadata.json'), $UTF8) | ConvertFrom-Json
    $mT = [IO.File]::ReadAllText((Join-Path $TARGET '.metadata\metadata.json'), $UTF8) | ConvertFrom-Json
    if ($mS.name -ne $mT.name -or $mS.id -ne $mT.id -or $mS.version -ne $mT.version) { Stop-Here '.metadata 核对不一致' }
    $script:TargetState = '运行文件已复制并核对，版本号尚未写入'
    Say "g. $total 个文件逐一核对 SHA-256 一致；.metadata 一致（$($mT.name) / id $($mT.id) / $($mT.version)）。" Green

    $script:Step = 'h'
    $rng = [Security.Cryptography.RandomNumberGenerator]::Create()
    do {
        $bytes = New-Object byte[] 16; $rng.GetBytes($bytes)
        $ver = ([BitConverter]::ToString($bytes)).Replace('-', '').ToLowerInvariant()
    } while ($v.Records.Items | Where-Object { [string]$_.version -eq $ver })
    [IO.File]::WriteAllText((Join-Path $TARGET $VERSION_FILE), "$ver`n", $UTF8)
    $script:TargetState = '运行文件已就绪；MOD 文件夹版本号已写入，源目录版本号与记录尚未写入'
    [IO.File]::WriteAllText((Join-Path $SOURCE $VERSION_FILE), "$ver`n", $UTF8)
    $script:TargetState = '运行文件已就绪；两边版本号已写入，update_record.json 尚未追加'
    $uc = Get-Uncommitted
    $ucCount = $(if ($null -eq $uc) { -1 } else { @($uc).Count })
    Add-Record $ver $head $total $v.Records $ucCount
    $script:TargetState = '部署完成'
    $final = Get-VersionState
    if ($final.State -ne 'ok') { Stop-Here '写入后三处版本号仍不一致' }
    Say "h. 新版本号 $ver 已写入两边并追加到 $RECORD_FILE。" Green
    Say "部署完成：$total 个运行文件 + $VERSION_FILE。" Green
    Show-Uncommitted $true
    return 0
}

function Invoke-Menu {
    Write-Host 'NESND 部署（源目录 -> MOD 文件夹）' -ForegroundColor Cyan
    Write-Host "  源目录    : $SOURCE"
    Write-Host "  MOD 文件夹: $TARGET"
    Write-Host '  1  部署：清空 MOD 文件夹，复制运行文件，写入新版本号'
    Write-Host '  2  预览：只列出将删除、将复制的内容和版本号检查，不改动'
    Write-Host '  3  检查：只核对两边版本号与最后一条记录'
    Write-Host '  q  退出'
    switch ((Read-Host '选择').Trim()) {
        '1' { return 'deploy' } '2' { return 'preview' } '3' { return 'check' } default { return $null }
    }
}

$rc = 0
$run = $Mode
try {
    if ($run -eq 'menu') { $run = Invoke-Menu; if (-not $run) { exit 0 } }
    switch ($run) {
        'check' { $rc = Invoke-Check }
        'preview' { $rc = Invoke-Preview }
        'deploy' { $rc = Invoke-Deploy $false }
        'force' { $rc = Invoke-Deploy $true }
    }
} catch {
    $msg = $_.Exception.Message
    Say ''
    if ($script:Step -in @('-', 'a', 'b', 'c', 'd')) {
        Say "已停止（第 $($script:Step) 步）：$msg" Red
        Say 'MOD 文件夹状态：未改动，没有删除任何东西。' Yellow
        Say "重新运行：$($script:RerunHint)" Yellow
        $rc = 2
    } else {
        Say "部署在第 $($script:Step) 步出错：$msg" Red
        Say "MOD 文件夹状态：$($script:TargetState)" Red
        Say "重新运行：$($script:RerunHint)" Yellow
        $rc = 3
    }
    if ($_.Exception -isnot [StopDeploy]) { Note $_.ScriptStackTrace }
} finally {
    if ($run -in @('preview', 'deploy', 'force')) { Save-Log $run }
}
exit $rc
