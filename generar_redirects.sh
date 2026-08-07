#!/bin/bash
CSV="wp9e_posts.csv"
REDIRECTS="static/_redirects"

mkdir -p static
> "$REDIRECTS"

count=0
skip=0

tail -n +2 "$CSV" | while IFS=',' read -r post_type slug titulo post_status; do
    slug=$(echo "$slug" | tr -d '"' | xargs)
    
    # Saltar páginas que ya no necesitás
    case "$slug" in
        prueba|prueba-1|prueba-a-ver|carrito|cart|tienda-3|pdf|listar-paginas)
            skip=$((skip + 1))
            continue
            ;;
    esac

    # Buscar el archivo en content/
    found=$(find content/ -name "${slug}.md" 2>/dev/null | head -1)

    if [ -n "$found" ]; then
        # Convertir a URL de Zola
        url_nueva="/$(echo "$found" | sed 's|^content/||' | sed 's|\.md$||')/"
        url_nueva=$(echo "$url_nueva" | sed 's|/_index/$|/|')

        # URL vieja: /slug/
        url_vieja="/${slug}/"

        # No redirigir si son iguales
        if [ "$url_vieja" != "$url_nueva" ]; then
            echo "${url_vieja} ${url_nueva} 301" >> "$REDIRECTS"
            count=$((count + 1))
        fi
    else
        echo "⚠️  No encontrado: ${slug}" >> /tmp/redirects_faltantes.txt
    fi
done

echo "✅ Generado: $REDIRECTS"
echo "   Redirecciones: $(wc -l < "$REDIRECTS")"
echo ""
echo "--- Primeras 15 líneas ---"
head -15 "$REDIRECTS"
echo ""
if [ -f /tmp/redirects_faltantes.txt ]; then
    echo "⚠️  Slugs no encontrados en Zola:"
    cat /tmp/redirects_faltantes.txt
    rm /tmp/redirects_faltantes.txt
fi
