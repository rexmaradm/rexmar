#!/usr/bin/env bash
# Uso: ./add_taxonomies.sh [directorio]
# Por defecto usa el directorio actual.

set -euo pipefail

DIR="${1:-.}"

# Bloque a insertar (TOML)
TOML_BLOCK=$'\n[taxonomies]\ntags = ["rexmar", "agua de mar", "Perú", "biología", "salud", "ciencia"]\n'

# Bloque a insertar (YAML)
YAML_BLOCK=$'\ntaxonomies:\n  tags:\n    - rexmar\n    - agua de mar\n    - Perú\n    - biología\n    - salud\n    - ciencia\n'

count_added=0
count_skipped=0

# Encuentra todos los .md recursivamente
while IFS= read -r -d '' file; do
  # Lee la primera línea para detectar el tipo de front matter
  first_line=$(head -n 1 "$file" || true)

  # Sólo procesamos archivos con front matter TOML (+++) o YAML (---)
  if [[ "$first_line" == "+++" ]]; then
    delim="+++"
    block="$TOML_BLOCK"
  elif [[ "$first_line" == "---" ]]; then
    delim="---"
    block="$YAML_BLOCK"
  else
    echo "⚠️  Sin front matter, se omite: $file"
    ((count_skipped++)) || true
    continue
  fi

  # Verifica si ya existe [taxonomies] o taxonomies: en el front matter
  # Extrae el bloque entre los dos delimitadores
  front=$(awk -v d="$delim" '
    NR==1 && $0==d {inside=1; next}
    inside && $0==d {exit}
    inside {print}
  ' "$file")

  if grep -qE '^\s*\[taxonomies\]|^\s*taxonomies\s*:' <<<"$front"; then
    echo "✅ Ya tiene taxonomies: $file"
    ((count_skipped++)) || true
    continue
  fi

  # Inserta el bloque justo antes del delimitador de cierre
  tmp=$(mktemp)
  awk -v d="$delim" -v blk="$block" '
    BEGIN { count=0; inserted=0 }
    {
      if ($0==d) {
        count++
        if (count==2 && !inserted) {
          printf "%s", blk
          inserted=1
        }
      }
      print
    }
  ' "$file" > "$tmp" && mv "$tmp" "$file"

  echo "➕ Agregado en: $file"
  ((count_added++)) || true

done < <(find "$DIR" -type f -name '*.md' -print0)

echo
echo "Resumen: $count_added archivos modificados, $count_skipped omitidos."
