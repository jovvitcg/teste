# instala as 13 skills ig-* e o voice.md no claude code deste computador (windows / powershell).
#
#   .\install.ps1            copia as skills; so cria o voice.md se ele nao existir
#   .\install.ps1 -Force     tambem sobrescreve o voice.md que ja estiver na home
param([switch]$Force)
$ErrorActionPreference = "Stop"

$Here = Split-Path -Parent $MyInvocation.MyCommand.Path
$SkillsDir = Join-Path $HOME ".claude\skills"
$IgDir = Join-Path $HOME ".claude\instagram"

New-Item -ItemType Directory -Force $SkillsDir | Out-Null
New-Item -ItemType Directory -Force $IgDir | Out-Null

$count = 0
Get-ChildItem -Directory (Join-Path $Here ".claude\skills") -Filter "ig-*" | ForEach-Object {
    $dest = Join-Path $SkillsDir $_.Name
    if (Test-Path $dest) { Remove-Item -Recurse -Force $dest }
    Copy-Item -Recurse $_.FullName $dest
    $count++
}
Write-Host "skills copiadas pra ${SkillsDir}: $count"

$voice = Join-Path $IgDir "voice.md"
if ((Test-Path $voice) -and -not $Force) {
    Write-Host "voice.md ja existe em $IgDir, mantive o seu (rode com -Force pra trocar)"
} else {
    Copy-Item (Join-Path $Here "instagram\voice.md") $voice
    Write-Host "voice.md copiado pra $voice"
}

if (Test-Path (Join-Path $SkillsDir "ig-reel\SKILL.md")) {
    Write-Host "ok: $SkillsDir\ig-reel\SKILL.md existe"
} else {
    throw "erro: $SkillsDir\ig-reel\SKILL.md nao apareceu"
}

$py = Get-Command python3 -ErrorAction SilentlyContinue
if (-not $py) { $py = Get-Command python -ErrorAction SilentlyContinue }
if ($py) { Write-Host "python encontrado: $($py.Source)" }
else { Write-Host "aviso: python nao encontrado. as skills escrevem mesmo assim, mas nao pontuam." }

Write-Host ""
Write-Host "agora reinicia o claude code e digita /ig- pra ver a lista."
