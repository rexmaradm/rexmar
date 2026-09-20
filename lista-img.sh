#!/bin/bash
# Asume que las imágenes están en la carpeta 'static' de tu proyecto Zola
DIR="static/wp-content/uploads/2022/07"

for img in "$DIR"/*.{jpg,jpeg,png,gif,webp}; do
    [ -e "$img" ] || continue
    f=$(basename "$img")
    echo "![$f](/wp-content/uploads/2022/07/$f)"
done
