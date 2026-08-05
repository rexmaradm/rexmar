import os
import xml.etree.ElementTree as ET
from urllib.parse import urlparse
import re

# 1. Leer el índice de Zola para obtener las rutas actuales
with open('cont.txt', 'r', encoding='utf-8') as f:
    content = f.read()

# Extraer todas las URLs de Zola (ej: /home/formas-de-uso-y-tips/gatos/)
zola_paths = set(re.findall(r'(https://rexmar\.pages\.dev(/[a-zA-Z0-9\-/]+))', content))
# Guardamos solo la ruta para comparar
zola_paths_only = set(urlparse(url)[2] for url, _ in zola_paths)
print(f"✅ Se encontraron {len(zola_paths_only)} rutas actuales en Zola.")

# 2. Leer el XML de WordPress
xml_file = 'tiendaholsticarex.WordPress.2026-07-27-paginas.xml'
try:
    tree = ET.parse(xml_file)
    root = tree.getroot()
except Exception as e:
    print(f"❌ Error leyendo XML: {e}")
    exit()

cambios_detectados = 0
sin_cambios = 0
aliases_inyectados = 0

# Diccionario para guardar: { "nombre_archivo.md": "ruta_antigua" }
# Lo llenaremos solo si la ruta cambió
url_map = {}

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
        
        # Verificar si esta ruta de WP existe en las rutas de Zola
        if wp_path in zola_paths_only:
            sin_cambios += 1
        else:
            # La ruta cambió o no la encontramos exactamente. 
            # Intentamos buscar por el post_name en los archivos .md
            cambios_detectados += 1
            
            # Buscar el archivo .md que podría corresponder a este post_name
            for root_dir, dirs, files in os.walk('content'):
                for file in files:
                    if file.endswith('.md'):
                        # Si el nombre del archivo contiene el post_name o viceversa
                        file_without_ext = file[:-3]
                        if post_name in file_without_ext or file_without_ext in post_name:
                            filepath = os.path.join(root_dir, file)
                            url_map[file] = wp_path
                            break

print(f"\n📊 Diagnóstico de URLs:")
print(f"   - Rutas que NO cambiaron (no necesitan alias): {sin_cambios}")
print(f"   - Rutas que SÍ cambiaron o no coinciden exactamente: {cambios_detectados}")
print(f"   - Coincidencias encontradas para inyectar: {len(url_map)}")

# 3. Inyectar aliases solo en los que cambiaron
if url_map:
    print("\n🚀 Inyectando aliases en archivos con URLs diferentes...")
    for file, old_url in url_map.items():
        # Buscar el archivo en todo el directorio content
        filepath = None
        for root_dir, dirs, files in os.walk('content'):
            if file in files:
                filepath = os.path.join(root_dir, file)
                break
        
        if filepath:
            with open(filepath, 'r', encoding='utf-8') as f:
                md_content = f.read()
            
            if 'aliases = ' in md_content:
                continue # Ya tiene alias
            
            partes = md_content.split('+++', 2)
            if len(partes) >= 2:
                front_matter = partes[1]
                resto = partes[2] if len(partes) > 2 else ""
                
                nuevo_front_matter = front_matter.rstrip() + f'\naliases = ["{old_url}"]\n'
                nuevo_contenido = '+++' + nuevo_front_matter + '+++' + resto
                
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(nuevo_contenido)
                
                print(f"   ✅ {file} -> {old_url}")
                aliases_inyectados += 1

print(f"\n🎉 ¡Proceso terminado! Se inyectaron {aliases_inyectados} aliases.")
