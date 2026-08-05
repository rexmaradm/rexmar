import os
import re
import xml.etree.ElementTree as ET
from urllib.parse import urlparse

# 1. Leer el índice de Zola
with open('cont.txt', 'r', encoding='utf-8') as f:
    content = f.read()

# Extraer rutas de Zola y normalizar (quitar dominio, asegurar que termine en /)
zola_paths = set(re.findall(r'https://rexmar\.pages\.dev(/[a-zA-Z0-9\-/]+)', content))
zola_paths_only = set(p.rstrip('/') + '/' for p in zola_paths)
print(f"✅ Se encontraron {len(zola_paths_only)} rutas actuales en Zola.")

# 2. Leer el XML de WordPress
xml_file = 'tiendaholsticarex.WordPress.2026-07-27-paginas.xml'
try:
    tree = ET.parse(xml_file)
    root = tree.getroot()
except Exception as e:
    print(f"❌ Error leyendo XML: {e}")
    exit()

# Diccionario para guardar: { "ruta_zola": "ruta_wordpress" }
url_map = {}
matches = 0
mismatches = []

for item in root.findall('.//item'):
    link = None
    post_name = None
    title = None
    
    for elem in item.iter():
        tag_name = elem.tag.split('}')[-1] if '}' in elem.tag else elem.tag
        if tag_name == 'link' and elem.text:
            link = elem.text.strip()
        if tag_name == 'post_name' and elem.text:
            post_name = elem.text.strip()
        if tag_name == 'title' and elem.text:
            title = elem.text.strip()
    
    if link and post_name:
        parsed = urlparse(link)
        wp_path = parsed.path
        
        # QUITAR EL PREFIJO /wp/ de las URLs de WordPress
        if wp_path.startswith('/wp/'):
            wp_path = wp_path[4:]  # Quitar los primeros 4 caracteres: /wp/
        
        if not wp_path.endswith('/'):
            wp_path += '/'
        
        # Ahora comparar correctamente
        if wp_path in zola_paths_only:
            matches += 1
        else:
            mismatches.append((post_name + '.md', wp_path, title))
            url_map[post_name] = wp_path

print(f"\n📊 Diagnóstico CORREGIDO de URLs:")
print(f"   ✅ Rutas que COINCIDEN (NO necesitan alias): {matches}")
print(f"   ️  Rutas que NO coinciden (necesitan alias): {len(mismatches)}")

if len(mismatches) > 0:
    print("\n🔍 Primeros 5 ejemplos de rutas que NO coinciden:")
    for file, wp_path, title in mismatches[:5]:
        print(f"   - {file} (título: {title})  -->  {wp_path}")

# 3. Ahora buscar los archivos .md y inyectar aliases
# Primero, crear un diccionario de todos los archivos .md con sus títulos
md_files = {}
for root_dir, dirs, files in os.walk('content'):
    for file in files:
        if file.endswith('.md'):
            filepath = os.path.join(root_dir, file)
            with open(filepath, 'r', encoding='utf-8') as f:
                md_content = f.read()
            
            # Extraer el título del front matter
            title_match = re.search(r'title\s*=\s*"([^"]+)"', md_content)
            if title_match:
                title = title_match.group(1)
                md_files[file] = {
                    'path': filepath,
                    'title': title,
                    'content': md_content
                }

print(f"\n📁 Se encontraron {len(md_files)} archivos .md en content/")

# 4. Inyectar aliases
aliases_inyectados = 0
saltados = 0
no_encontrados = 0

for post_name, wp_path in url_map.items():
    # Buscar el archivo .md que corresponda
    archivo_encontrado = None
    
    # Intento 1: Buscar por nombre de archivo exacto
    if post_name + '.md' in md_files:
        archivo_encontrado = md_files[post_name + '.md']
    else:
        # Intento 2: Buscar por título (más flexible)
        for file, info in md_files.items():
            # Normalizar el título para comparar (quitar acentos, minúsculas, etc.)
            title_normalized = re.sub(r'[^\w\s]', '', info['title']).lower().strip()
            post_name_normalized = re.sub(r'[^\w\s]', '', post_name.replace('-', ' ')).lower().strip()
            
            if title_normalized == post_name_normalized or post_name in title_normalized:
                archivo_encontrado = info
                break
    
    if archivo_encontrado:
        filepath = archivo_encontrado['path']
        md_content = archivo_encontrado['content']
        
        # Si ya tiene aliases, saltar
        if 'aliases = ' in md_content:
            saltados += 1
            continue
        
        # Inyectar alias en el front matter
        partes = md_content.split('+++', 2)
        if len(partes) >= 2:
            front_matter = partes[1]
            resto = partes[2] if len(partes) > 2 else ""
            
            nuevo_front_matter = front_matter.rstrip() + f'\naliases = ["{wp_path}"]\n'
            nuevo_contenido = '+++' + nuevo_front_matter + '+++' + resto
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(nuevo_contenido)
            
            print(f"   ✅ {filepath} -> {wp_path}")
            aliases_inyectados += 1
    else:
        no_encontrados += 1

print(f"\n🚀 Proceso de inyección completado:")
print(f"   - Aliases inyectados exitosamente: {aliases_inyectados}")
print(f"   - Archivos saltados (ya tenían alias): {saltados}")
print(f"   - Archivos no encontrados: {no_encontrados}")
