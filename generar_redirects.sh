#!/bin/bash
CSV="wp9e_posts.csv"
REDIRECTS="static/_redirects"

mkdir -p static
> "$REDIRECTS"

tail -n +2 "$CSV" | while IFS=',' read -r post_type slug titulo post_status; do
    slug=$(echo "$slug" | tr -d '"' | xargs)

    case "$slug" in
        prueba|prueba-1|prueba-a-ver|carrito|cart|tienda-3|pdf|listar-paginas)
            continue
            ;;
    esac

    found=$(find content/ -name "${slug}.md" 2>/dev/null | head -1)

    if [ -n "$found" ]; then
        url_nueva="/$(echo "$found" | sed 's|^content/||' | sed 's|\.md$||')/"
        url_nueva=$(echo "$url_nueva" | sed 's|/_index/$|/|')

        # SIN barra final (siempre útil, agrega la barra)
        echo "/${slug} ${url_nueva} 301" >> "$REDIRECTS"

        # CON barra final (solo si es distinta a la nueva)
        if [ "/${slug}/" != "$url_nueva" ]; then
            echo "/${slug}/ ${url_nueva} 301" >> "$REDIRECTS"
        fi
    fi
done

echo "✅ Generado: $REDIRECTS"
echo "   Redirecciones: $(wc -l < "$REDIRECTS")"
head -6 "$REDIRECTS"
