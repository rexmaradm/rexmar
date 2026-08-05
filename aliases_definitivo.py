import os
import re
import xml.etree.ElementTree as ET
from urllib.parse import urlparse

print("🔍 Iniciando proceso de inyección de aliases SEO...")
print("=" * 60)

# 1. Leer el índice de Zola para obtener las rutas actuales
print("\n📂 Paso 1: Leyendo índice de Zola...")
with open('cont.txt', 'r', encoding='utf-8') as f:
    content = f.read()

# Extraer todas las URLs de Zola
zola_urls = set(re.findall(r'https://rexmar\.pages\.dev(/[a-zA-Z0-9\-/]+)', content))
zola_paths = set(url.rstrip('/') + '/' for url in zola_urls)
print(f"   ✅ Encontradas {len(zola_paths)} rutas en Zola")

# 2. Leer el XML de WordPress
print("\n📂 Paso 2: Leyendo backup de WordPress...")
xml_file = 'tiendaholsticarex.WordPress.2026-07-27-paginas.xml'
try:
    tree = ET.parse(xml_file)
    root = tree.getroot()
except Exception as e:
    print(f"   ❌ Error leyendo XML: {e}")
    exit()

# Extraer URLs de WordPress y quitar el prefijo /wp/
wp_urls = {}
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
        
        # Quitar el prefijo /wp/ si existe
        if wp_path.startswith('/wp/'):
            wp_path = wp_path[4:]
        elif wp_path.startswith('/wp'):
            wp_path = wp_path[3:]
        
        if not wp_path.endswith('/'):
            wp_path += '/'
        
        wp_urls[post_name] = wp_path

print(f"   ✅ Encontradas {len(wp_urls)} URLs en WordPress")

# 3. Crear índice completo de todos los archivos .md en content/
print("\n📂 Paso 3: Indexando archivos .md en content/...")
md_files_index = {}
total_md_files = 0

for root_dir, dirs, files in os.walk('content'):
    for file in files:
        if file.endswith('.md'):
            total_md_files += 1
            filepath = os.path.join(root_dir, file)
            
            # Calcular la ruta relativa desde content/
            rel_path = os.path.relpath(filepath, 'content')
            
            # Convertir a formato URL (reemplazar \ con /, quitar .md, agregar /)
            url_path = '/' + rel_path.replace('\\', '/').replace('.md', '')
            if not url_path.endswith('/'):
                url_path += '/'
            
            # Si es _index.md, la URL es la carpeta padre
            if file == '_index.md':
                url_path = '/' + os.path.dirname(rel_path).replace('\\', '/') + '/'
                if url_path == '/':
                    url_path = '/'
            
            md_files_index[url_path] = {
                'filepath': filepath,
                'filename': file,
                'url_path': url_path
            }

print(f"   ✅ Indexados {total_md_files} archivos .md")
print(f"   ✅ Generadas {len(md_files_index)} rutas URL")

# 4. Comparar URLs y preparar inyección
print("\n Paso 4: Comparando URLs de WordPress vs Zola...")
aliases_to_inject = {}
urls_that_match = 0
urls_that_differ = 0

for post_name, wp_path in wp_urls.items():
    # Buscar si esta URL de WordPress existe en Zola
    if wp_path in md_files_index:
        urls_that_match += 1
    else:
        # La URL no existe exactamente, buscar coincidencias parciales
        urls_that_differ += 1
        
        # Intentar encontrar el archivo .md correspondiente
        # Buscar por post_name en los filenames
        for url_path, file_info in md_files_index.items():
            filename_without_ext = file_info['filename'].replace('.md', '')
            
            # Si el post_name coincide con el nombre del archivo (sin extensión)
            if post_name == filename_without_ext:
                aliases_to_inject[file_info['filepath']] = wp_path
                break

print(f"   ✅ URLs que COINCIDEN exactamente: {urls_that_match}")
print(f"   ⚠️  URLs que NO coinciden: {urls_that_differ}")
print(f"   🎯 Coincidencias encontradas para inyectar: {len(aliases_to_inject)}")

# 5. Inyectar aliases
print("\n🚀 Paso 5: Inyectando aliases en archivos .md...")
injected = 0
skipped = 0
errors = 0

for filepath, wp_path in aliases_to_inject.items():
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            md_content = f.read()
        
        # Si ya tiene aliases, saltar
        if 'aliases = ' in md_content:
            skipped += 1
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
            
            injected += 1
            print(f"   ✅ {filepath} -> {wp_path}")
        else:
            errors += 1
            print(f"   ❌ Error de formato en: {filepath}")
    except Exception as e:
        errors += 1
        print(f"   ❌ Error procesando {filepath}: {e}")

print("\n" + "=" * 60)
print(" RESUMEN FINAL:")
print(f"   - Total de archivos .md en content/: {total_md_files}")
print(f"   - URLs de WordPress procesadas: {len(wp_urls)}")
print(f"   - URLs que ya coinciden (no necesitan alias): {urls_that_match}")
print(f"   - Aliases inyectados exitosamente: {injected}")
print(f"   - Archivos saltados (ya tenían alias): {skipped}")
print(f"   - Errores: {errors}")
print("=" * 60)

if injected > 0:
    print("\n ¡Proceso completado! Ahora ejecuta:")
    print("   git add .")
    print('   git commit -m "Inyectados aliases SEO para redirección desde WordPress"')
    print("   git push origin main")
else:
    print("\n⚠️  No se inyectaron nuevos aliases. Esto puede significar que:")
    print("   1. Las URLs de WordPress y Zola ya coinciden (¡excelente!)")
    print("   2. Los archivos ya tenían aliases previamente")
