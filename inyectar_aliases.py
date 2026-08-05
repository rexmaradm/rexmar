import os
import re

# Leer el archivo cont.txt
with open('cont.txt', 'r', encoding='utf-8') as f:
    content = f.read()

# Extraer todas las URLs únicas del archivo
pattern = r'https://rexmar\.pages\.dev(/[a-zA-Z0-9\-/]+)'
urls = set(re.findall(pattern, content))

print(f"✅ Se encontraron {len(urls)} URLs únicas")

# Crear un mapeo: {nombre_archivo.md: "/url/antigua/"}
url_map = {}
for url in urls:
    # Extraer el slug (última parte de la URL)
    slug = url.rstrip('/').split('/')[-1]
    url_map[slug + '.md'] = url

print(f"✅ Se mapearon {len(url_map)} archivos")

# Recorrer todos los archivos .md en content/
archivos_procesados = 0
for root, dirs, files in os.walk('content'):
    for file in files:
        if file.endswith('.md') and file in url_map:
            filepath = os.path.join(root, file)
            old_url = url_map[file]
            
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Si ya tiene aliases, saltar
            if 'aliases = ' in content:
                continue
            
            # Inyectar alias en el front matter
            partes = content.split('+++', 2)
            if len(partes) >= 2:
                front_matter = partes[1]
                resto = partes[2] if len(partes) > 2 else ""
                
                nuevo_front_matter = front_matter.rstrip() + f'\naliases = ["{old_url}"]\n'
                nuevo_contenido = '+++' + nuevo_front_matter + '+++' + resto
                
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(nuevo_contenido)
                
                print(f"✅ {file} -> {old_url}")
                archivos_procesados += 1

print(f"\n🎉 ¡Listo! Se inyectaron aliases en {archivos_procesados} archivos.")
