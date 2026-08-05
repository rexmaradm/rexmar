import os
import re
import xml.etree.ElementTree as ET
from urllib.parse import urlparse

print("🔍 Iniciando proceso de inyección de aliases SEO (versión robusta)...")
print("=" * 60)

# 1. Leer el índice de Zola para obtener las rutas actuales
print("\n📂 Paso 1: Leyendo índice de Zola...")
with open('cont.txt', 'r', encoding='utf-8') as f:
    content = f.read()

zola_urls = set(re.findall(r'https://rexmar\.pages\.dev(/[a-zA-Z0-9\-/]+)', content))
zola_paths = set(url.rstrip('/') + '/' for url in zola_urls)
print(f"   ✅ Encontradas {len(zola_paths)} rutas en Zola")

# 2. Leer el XML de WordPress
print("\n Paso 2: Leyendo backup de WordPress...")
xml_file = 'tiendaholsticarex.WordPress.2026-07-27-paginas.xml'
try:
    tree = ET.parse(xml_file)
    root = tree.getroot()
except Exception as e:
    print(f"   ❌ Error leyendo XML: {e}")
    exit()

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

# 3. Crear índice de archivos .md
print("\n Paso 3: Indexando archivos .md en content/...")
md_files_index = {}
total_md_files = 0

for root_dir, dirs, files in os.walk('content'):
    for file in files:
        if file.endswith('.md'):
            total_md_files += 1
            filepath = os.path.join(root_dir, file)
            
            rel_path = os.path.relpath(filepath, 'content')
            url_path = '/' + rel_path.replace('\\', '/').replace('.md', '')
            if not url_path.endswith('/'):
                url_path += '/'
            
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

# 4. Comparar URLs y preparar inyección
print("\n📊 Paso 4: Comparando URLs de WordPress vs Zola...")
aliases_to_inject = {}
urls_that_match = 0
urls_that_differ = 0

for post_name, wp_path in wp_urls.items():
    if wp_path in md_files_index:
        urls_that_match += 1
    else:
        urls_that_differ += 1
        
        for url_path, file_info in md_files_index.items():
            filename_without_ext = file_info['filename'].replace('.md', '')
            
            if post_name == filename_without_ext:
                aliases_to_inject[file_info['filepath']] = wp_path
                break

print(f"   ✅ URLs que COINCIDEN exactamente: {urls_that_match}")
print(f"   ⚠️  URLs que NO coinciden: {urls_that_differ}")
print(f"    Coincidencias encontradas para inyectar: {len(aliases_to_inject)}")

# 5. Función robusta para inyectar aliases
def inject_alias_robust(filepath, wp_path):
    """Intenta inyectar el alias de múltiples formas"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Si ya tiene aliases, saltar
        if 'aliases = ' in content or 'aliases=' in content:
            return 'skipped'
        
        # Intento 1: Front matter estándar con +++
        if content.startswith('+++'):
            partes = content.split('+++', 2)
            if len(partes) >= 2:
                front_matter = partes[1]
                resto = partes[2] if len(partes) > 2 else ""
                
                nuevo_front_matter = front_matter.rstrip() + f'\naliases = ["{wp_path}"]\n'
                nuevo_contenido = '+++' + nuevo_front_matter + '+++' + resto
                
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(nuevo_contenido)
                return 'success'
        
        # Intento 2: Front matter con ---
        if content.startswith('---'):
            partes = content.split('---', 2)
            if len(partes) >= 2:
                front_matter = partes[1]
                resto = partes[2] if len(partes) > 2 else ""
                
                nuevo_front_matter = front_matter.rstrip() + f'\naliases: ["{wp_path}"]\n'
                nuevo_contenido = '---' + nuevo_front_matter + '---' + resto
                
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(nuevo_contenido)
                return 'success'
        
        # Intento 3: Sin front matter, agregar al inicio
        # Solo si el archivo no empieza con # (título markdown)
        if not content.startswith('#'):
            nuevo_contenido = f'+++\ntitle = "{os.path.basename(filepath).replace(".md", "").replace("-", " ").title()}"\naliases = ["{wp_path}"]\n+++\n\n{content}'
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(nuevo_contenido)
            return 'success'
        
        return 'error_no_frontmatter'
        
    except Exception as e:
        return f'error: {str(e)}'

# 6. Inyectar aliases
print("\n🚀 Paso 5: Inyectando aliases en archivos .md...")
injected = 0
skipped = 0
errors = 0
error_details = {}

for filepath, wp_path in aliases_to_inject.items():
    result = inject_alias_robust(filepath, wp_path)
    
    if result == 'success':
        injected += 1
        print(f"   ✅ {filepath} -> {wp_path}")
    elif result == 'skipped':
        skipped += 1
    elif result.startswith('error'):
        errors += 1
        error_type = result.split(':')[0] if ':' in result else result
        if error_type not in error_details:
            error_details[error_type] = []
        error_details[error_type].append(filepath)

print("\n" + "=" * 60)
print("📊 RESUMEN FINAL:")
print(f"   - Total de archivos .md en content/: {total_md_files}")
print(f"   - URLs de WordPress procesadas: {len(wp_urls)}")
print(f"   - URLs que ya coinciden (no necesitan alias): {urls_that_match}")
print(f"   - Aliases inyectados exitosamente: {injected}")
print(f"   - Archivos saltados (ya tenían alias): {skipped}")
print(f"   - Errores: {errors}")

if error_details:
    print("\n️  Detalles de errores:")
    for error_type, files in error_details.items():
        print(f"   - {error_type}: {len(files)} archivos")
        if len(files) <= 5:
            for f in files:
                print(f"     • {f}")

if injected > 0:
    print("\n🎉 ¡Proceso completado! Ahora ejecuta:")
    print("   git add .")
    print('   git commit -m "Inyectados aliases SEO para redirección desde WordPress"')
    print("   git push origin main")
else:
    print("\n⚠️  No se inyectaron nuevos aliases.")
