#!/usr/bin/env bash
# instala as 13 skills ig-* e o voice.md no claude code deste computador (macOS / linux).
#
#   ./install.sh            copia as skills; só cria o voice.md se ele não existir
#   ./install.sh --force    também sobrescreve o voice.md que já estiver na home
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILLS_DIR="${HOME}/.claude/skills"
IG_DIR="${HOME}/.claude/instagram"
FORCE=0
[ "${1:-}" = "--force" ] && FORCE=1

mkdir -p "$SKILLS_DIR" "$IG_DIR"

count=0
for src in "$HERE"/.claude/skills/ig-*/; do
  name="$(basename "$src")"
  rm -rf "${SKILLS_DIR:?}/${name}"
  cp -R "$src" "${SKILLS_DIR}/${name}"
  count=$((count + 1))
done
echo "skills copiadas pra ${SKILLS_DIR}: ${count}"

if [ -f "${IG_DIR}/voice.md" ] && [ "$FORCE" -eq 0 ]; then
  echo "voice.md já existe em ${IG_DIR}, mantive o seu (rode com --force pra trocar)"
else
  cp "$HERE/instagram/voice.md" "${IG_DIR}/voice.md"
  echo "voice.md copiado pra ${IG_DIR}/voice.md"
fi

if [ -f "${SKILLS_DIR}/ig-reel/SKILL.md" ]; then
  echo "ok: ${SKILLS_DIR}/ig-reel/SKILL.md existe"
else
  echo "erro: ${SKILLS_DIR}/ig-reel/SKILL.md não apareceu" >&2
  exit 1
fi

if command -v python3 >/dev/null 2>&1; then
  echo "python3 encontrado: $(python3 --version 2>&1)"
else
  echo "aviso: python3 não encontrado. as skills escrevem mesmo assim, mas não pontuam (hookscore, beats, caption, humanize, detect)."
fi

echo
echo "agora reinicia o claude code e digita /ig- pra ver a lista."
