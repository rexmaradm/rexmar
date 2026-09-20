#!/bin/bash
DIR="static/wp-content/uploads/2022/07"

for img in "$DIR"/*.{jpg,jpeg,png,gif,webp}; do
    [ -e "$img" ] || continue
    f=$(basename "$img")
    echo "<img src=\"/wp-content/uploads/2022/07/$f\" alt=\"$f\" style=\"max-width:90%; height:auto; display:block; margin:1em auto;\">"
done
