#!/bin/bash

echo "=== Páginas huérfanas en Zola ==="
echo ""

# Contador
count=0

# Buscar todos los archivos .md excepto _index.md
find content -name "*.md" -not -name "_index.md" | while read file; do
    # Obtener el directorio del archivo
    dir=$(dirname "$file")
    
    # Verificar si existe un _index.md en ese directorio
    if [ ! -f "$dir/_index.md" ]; then
        echo "Huérfana: $file"
        ((count++))
    fi
done

echo ""
echo "=== Total: $count páginas huérfanas ==="
