import os
import xml.etree.ElementTree as ET
from urllib.parse import urlparse

xml_file = 'tiendaholsticarex.WordPress.2026-07-27-paginas.xml'

print(f"📂 Leyendo {xml_file}...")
try:
    tree = ET.parse(xml_file)
    root = tree.getroot()
except Exception as e:
    print(f"❌ Error leyendo XML: {e}")
    exit()

url_map = {}
for item in root.findall('.//item'):
    slug = None
    old_link = None
    for elem in item.iter():
        # Manejar namespaces de WordPress (ej: {http://wordpress.org/export/1.2/}post_name)
        tag_name = elem.tag.split('}')[-1] if '}' in elem.tag else elem.tag
        if tag_name == 'post_name' and elem.text:
            slug = elem.text.strip()
        if tag_name == 'link' and elem.text:
            old_link = elem.text.strip()
            
    if slug and old_link:
        parsed = urlparse(old_link)
        path = parsed.path
        if not path.endswith('/'):
            path += '/'
        url_map[slug + '.md'] = path

print(f"✅ Se encontraron {len(url_map)} artículos/páginas en el XML.")

# Ahora inyectamos los aliases en los archivos .md
archivos_procesados = 0
archivos_saltados = 0

for root_dir, dirs, files in os.walk('content'):
    for file in files:
        if file.endswith('.md') and file in url_map:
            filepath = os.path.join(root_dir, file)
            old_url = url_map[file]
            
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Si ya tiene aliases, lo saltamos y lo contamos
            if 'aliases = ' in content:
                archivos_saltados += 1
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

print(f"\n📊 Resumen del diagnóstico:")
print(f"   - Archivos actualizados hoy: {archivos_procesados}")
print(f"   - Archivos saltados (ya tenían alias): {archivos_saltados}")
print(f"   - Total de coincidencias encontradas: {archivos_procesados + archivos_saltados}")
