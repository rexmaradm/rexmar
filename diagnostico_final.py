import os
import re
from urllib.parse import urlparse
import xml.etree.ElementTree as ET

# 1. Leer el índice de Zola
with open('cont.txt', 'r', encoding='utf-8') as f:
    content = f.read()

# Extraer rutas y asegurar que todas terminen en '/' para comparar igual
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

url_map = {}
matches = 0
mismatches = []

for item in root.findall('.//item'):
    link = None
    post_name = None
    
    for elem in item.iter():
        tag_name = elem.tag.split('}')[-1] if '}' in elem.tag else elem.tag
        if tag_name == 'link' and elem.text:
            link = elem.text.strip()
        if tag_name == 'post_name' and elem.text:
            post_name = elem.text.strip()
    
    if link and post_name:
        parsed = urlparse(link)
        wp_path = parsed.path
        if not wp_path.endswith('/'):
            wp_path += '/'
        
        # Comparación justa
        if wp_path in zola_paths_only:
            matches += 1
        else:
            mismatches.append((post_name + '.md', wp_path))
            url_map[post_name + '.md'] = wp_path

print(f"\n📊 Diagnóstico REAL de URLs:")
print(f"   ✅ Rutas que COINCIDEN exactamente (NO necesitan alias): {matches}")
print(f"   ⚠️  Rutas que NO coinciden (necesitan alias): {len(mismatches)}")

if len(mismatches) > 0:
    print("\n🔍 Primeros 5 ejemplos de rutas que NO coinciden:")
    for file, wp_path in mismatches[:5]:
        print(f"   - {file}  -->  {wp_path}")

# 3. Inyectar aliases solo en las que realmente cambiaron
aliases_inyectados = 0
saltados = 0
no_encontrados = 0

for file, old_url in url_map.items():
    filepath = None
    for root_dir, dirs, files in os.walk('content'):
        if file in files:
            filepath = os.path.join(root_dir, file)
            break
    
    if not filepath:
        no_encontrados += 1
        continue 
        
    with open(filepath, 'r', encoding='utf-8') as f:
        md_content = f.read()
    
    if 'aliases = ' in md_content:
        saltados += 1
        continue 
    
    partes = md_content.split('+++', 2)
    if len(partes) >= 2:
        front_matter = partes[1]
        resto = partes[2] if len(partes) > 2 else ""
        
        nuevo_front_matter = front_matter.rstrip() + f'\naliases = ["{old_url}"]\n'
        nuevo_contenido = '+++' + nuevo_front_matter + '+++' + resto
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(nuevo_contenido)
        
        aliases_inyectados += 1

print(f"\n🚀 Proceso de inyección completado:")
print(f"   - Aliases inyectados exitosamente: {aliases_inyectados}")
print(f"   - Archivos saltados (ya tenían alias): {saltados}")
print(f"   - Archivos no encontrados en carpeta content/: {no_encontrados}")
