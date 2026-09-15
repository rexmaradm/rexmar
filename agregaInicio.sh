#!/usr/bin/env bash
set -euo pipefail

find . -type f -name '*.md' ! -name '_index.md' | while IFS= read -r file; do
  if grep -qF '[ir a Inicio](/)' "$file"; then
    echo "Ya tiene el enlace, salto: $file"
    continue
  fi

  # asegurar que el archivo termine en newline antes de agregar
  if [ -s "$file" ] && [ "$(tail -c1 "$file")" != "" ]; then
    echo >> "$file"
  fi

  {
    echo ""
    echo '<div align="center">'
    echo ""
    echo '[ir a Inicio](/)'
    echo ""
    echo '</div>'
  } >> "$file"

  echo "Agregado: $file"
done
