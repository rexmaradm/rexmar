import os
import re

html_file = "Tienda Holística Rex – RexMar agua de mar Perú.html"
content_dir = "content"

# 1. Extraer todas las URLs antiguas del HTML
try:
    with open(html_file, 'r', encoding='utf-8') as f:
        html_content = f.read()
except FileNotFoundError:
    print(f"❌ No se encontró el archivo: {html_file}")
    print("Asegúrate de ejecutar este script en la misma carpeta donde está el HTML.")
    exit()

# Buscar patrones como: [Texto](https://th.org.pe/wp/ruta/al/articulo/)
pattern = r'\[.*?\]\(https://th\.org\.pe/wp/([^)]+)\)'
matches = re.findall(pattern, html_content)

# Crear un diccionario: { "nombre-archivo": "/ruta/antigua/completa/" }
url_map = {}
for path in matches:
    clean_path = path.rstrip('/')
    slug = clean_path.split('/')[-1]
    url_map[slug] = "/" + clean_path + "/"

print(f"✅ Se encontraron {len(url_map)} URLs antiguas en el HTML.")

# 2. Recorrer los archivos .md en la carpeta content
archivos_procesados = 0
for root, dirs, files in os.walk(content_dir):
    for file in files:
        if file.endswith(".md"):
            filename_without_ext = file[:-3]
            
            # Si el nombre del archivo coincide con un slug del HTML
            if filename_without_ext in url_map:
                filepath = os.path.join(root, file)
                old_url = url_map[filename_without_ext]
                
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Si ya tiene aliases, lo saltamos para no duplicar
                if "aliases = " in content:
                    continue 
                
                # Inyectar el alias en el front matter (después del primer +++)
                partes = content.split("+++", 2)
                if len(partes) >= 2:
                    front_matter = partes[1]
                    resto = partes[2] if len(partes) > 2 else ""
                    
                    nuevo_front_matter = front_matter.rstrip() + f'\naliases = ["{old_url}"]\n'
                    nuevo_contenido = "+++" + nuevo_front_matter + "+++" + resto
                    
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(nuevo_contenido)
                    
                    print(f"✅ {file} -> {old_url}")
                    archivos_procesados += 1

print(f"\n🎉 ¡Listo! Se inyectaron aliases en {archivos_procesados} archivos.")
