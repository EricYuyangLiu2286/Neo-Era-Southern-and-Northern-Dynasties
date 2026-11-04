$ErrorActionPreference = 'Stop'
$taskRoot = [IO.Path]::GetFullPath('D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench')
$taskReport = Join-Path $taskRoot 'reports/branch-naming-cleanup-20261104'
$keepBackups = @('pre-update-20261030T233944Z','pre-change-maintenance-pre-cleanup-20261104T213001Z')
if (Get-Process -Name victoria3 -ErrorAction SilentlyContinue) { throw 'Game is still running; old runtime cleanup must wait.' }
if (-not (Test-Path -LiteralPath (Join-Path $taskRoot 'exports/maintenance-current/.metadata/metadata.json'))) { throw 'Current candidate missing' }
foreach ($backupName in $keepBackups) {
    if (-not (Test-Path -LiteralPath (Join-Path $taskRoot "backups/$backupName/mod"))) { throw "Protected backup missing: $backupName" }
}
function Assert-TaskChild([string]$path) {
    $resolved = (Resolve-Path -LiteralPath $path).ProviderPath
    $relative = [IO.Path]::GetRelativePath($taskRoot, $resolved)
    if ([IO.Path]::IsPathRooted($relative) -or $relative -eq '.' -or $relative -eq '..' -or $relative.StartsWith('..' + [IO.Path]::DirectorySeparatorChar)) { throw "Unsafe target: $resolved" }
    $cursor = Get-Item -LiteralPath $resolved -Force
    while ($null -ne $cursor -and $cursor.FullName -ne $taskRoot) {
        if ($cursor.Attributes -band [IO.FileAttributes]::ReparsePoint) { throw "Reparse path: $resolved" }
        $cursor = $cursor.Parent
        if ($null -eq $cursor -and (Test-Path -LiteralPath (Split-Path -Parent $resolved))) { break }
    }
    return $resolved
}
# One actual engine terminal sample, not entire historical runtime profiles.
$sampleSource = Join-Path $taskRoot 'runtime/profiles/20261103T100813Z/save games/观察者_1866_01_15.v3'
$sampleTarget = Join-Path $taskRoot 'evidence/key-engine-terminal/观察者_1866_01_15.v3'
if (Test-Path -LiteralPath $sampleSource) {
    [void](New-Item -ItemType Directory -Path (Split-Path -Parent $sampleTarget) -Force)
    Copy-Item -LiteralPath $sampleSource -Destination $sampleTarget
    $sampleHash = (Get-FileHash -LiteralPath $sampleTarget -Algorithm SHA256).Hash.ToLowerInvariant()
    if ($sampleHash -ne '84aeb299f56656c3c9ce2373299ef5ba98a78a3bf01bdc9a1b39f38c49ee67e4') { throw 'Terminal save verification failed' }
}
$targets = [System.Collections.Generic.List[string]]::new()
foreach ($group in @('exports','backups','runtime','validation/snapshots','validation/runs','releases','qa-fixtures')) {
    $parentPath = Join-Path $taskRoot $group
    if (-not (Test-Path -LiteralPath $parentPath)) { continue }
    foreach ($item in Get-ChildItem -LiteralPath $parentPath -Force) {
        if ($group -eq 'exports' -and $item.Name -eq 'maintenance-current') { continue }
        if ($group -eq 'backups' -and $keepBackups -contains $item.Name) { continue }
        $targets.Add((Assert-TaskChild $item.FullName))
    }
}
$plan = Get-Content -LiteralPath (Join-Path $taskReport 'cleanup-plan-review.json') -Raw | ConvertFrom-Json
$projectOperation = $plan.operations | Where-Object { $_.operation -eq 'delete_explicit_transient_directories_only' }
foreach ($name in $projectOperation.children) {
    if ($name -notmatch '^(editor-(export-staging|fixtures|load)-|phi-(expiry-probe-static|permission-static)-)[a-zA-Z0-9-]+$') { throw "Unapproved project: $name" }
    $path = Join-Path $taskRoot "projects/$name"
    if (Test-Path -LiteralPath $path) { $targets.Add((Assert-TaskChild $path)) }
}
$records = [System.Collections.Generic.List[object]]::new()
foreach ($path in $targets) {
    $resolved = Assert-TaskChild $path
    $item = Get-Item -LiteralPath $resolved -Force
    if ($item.PSIsContainer) {
        $children = @(Get-ChildItem -LiteralPath $resolved -Recurse -Force)
        if ($children | Where-Object { $_.Attributes -band [IO.FileAttributes]::ReparsePoint } | Select-Object -First 1) { throw "Nested reparse point: $resolved" }
        $files = @($children | Where-Object { -not $_.PSIsContainer })
        $bytes = ($files | Measure-Object -Property Length -Sum).Sum
        $count = $files.Count
    } else { $bytes = $item.Length; $count = 1 }
    Remove-Item -LiteralPath $resolved -Recurse -Force
    if (Test-Path -LiteralPath $resolved) { throw "Deletion incomplete: $resolved" }
    $records.Add([PSCustomObject]@{path=$resolved;files=$count;bytes=[long]$bytes;deleted=$true})
    if ($records.Count % 20 -eq 0) { Write-Output "Deleted $($records.Count) approved old entries" }
    $records | ConvertTo-Json -Depth 4 | Set-Content -LiteralPath (Join-Path $taskReport 'cleanup-deleted-directories.json') -Encoding utf8
}
$remainingSaves = @(Get-ChildItem -LiteralPath $taskRoot -Recurse -File -Filter '*.v3' -Force | Where-Object { $_.FullName -ne $sampleTarget -and -not $_.FullName.StartsWith((Join-Path $taskRoot 'projects/nesnd-repository') + [IO.Path]::DirectorySeparatorChar) })
foreach ($file in $remainingSaves) {
    $resolved = Assert-TaskChild $file.FullName
    Remove-Item -LiteralPath $resolved -Force
    $records.Add([PSCustomObject]@{path=$resolved;files=1;bytes=$file.Length;deleted=$true})
}
$records | ConvertTo-Json -Depth 4 | Set-Content -LiteralPath (Join-Path $taskReport 'cleanup-deleted-directories.json') -Encoding utf8
$result = [PSCustomObject]@{status='COMPLETED';entries=$records.Count;files=($records|Measure-Object files -Sum).Sum;logical_bytes=($records|Measure-Object bytes -Sum).Sum;kept_original=$keepBackups[0];kept_prechange=$keepBackups[1];kept_current_candidate='exports/maintenance-current';kept_engine_sample=$sampleTarget;normal_user_save_directory_touched=$false}
$result | ConvertTo-Json -Depth 4 | Set-Content -LiteralPath (Join-Path $taskReport 'cleanup-result.json') -Encoding utf8
$result | ConvertTo-Json -Compress
