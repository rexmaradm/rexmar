import os
import re

print("🔍 Buscando TODOS los formatos de YouTube (rotos y correctos)...")
archivos_modificados = 0
total_videos = 0

for root, dirs, files in os.walk('content'):
    for file in files:
        if file.endswith('.md'):
            filepath = os.path.join(root, file)
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original = content
            videos_encontrados = []
            
            # 1. Buscar shortcodes mal formados: {{ youtube(id="ID") }}}} o {{ youtube(id="ID") }}
            pattern1 = r'\{\{\s*youtube\(id="([a-zA-Z0-9_-]{11})"\)\s*\}+\}'
            videos_encontrados.extend(re.findall(pattern1, content))
            
            # 2. Buscar shortcodes sin llaves: youtube(id="ID")
            pattern2 = r'youtube\(id="([a-zA-Z0-9_-]{11})"\)'
            videos_encontrados.extend(re.findall(pattern2, content))
            
            # 3. Buscar enlaces crudos de YouTube
            pattern3 = r'youtube\.com/watch\?v=([a-zA-Z0-9_-]{11})'
            videos_encontrados.extend(re.findall(pattern3, content))
            
            pattern4 = r'youtu\.be/([a-zA-Z0-9_-]{11})'
            videos_encontrados.extend(re.findall(pattern4, content))
            
            pattern5 = r'youtube\.com/shorts/([a-zA-Z0-9_-]{11})'
            videos_encontrados.extend(re.findall(pattern5, content))
            
            # Eliminar duplicados
            videos_unicos = list(set(videos_encontrados))
            
            if videos_unicos:
                # Limpiar TODO el contenido problemático
                # 1. Eliminar bloques <figure> de WordPress
                content = re.sub(r'<figure[^>]*>.*?</figure>', '', content, flags=re.DOTALL | re.IGNORECASE)
                
                # 2. Eliminar bloques <div> con clases de WordPress
                content = re.sub(r'<div[^>]*class="[^"]*wp-block[^"]*"[^>]*>.*?</div>', '', content, flags=re.DOTALL | re.IGNORECASE)
                
                # 3. Eliminar TODOS los shortcodes de YouTube (bien o mal formados)
                content = re.sub(r'\{?\{?\s*youtube\(id="[^"]+"\)\s*\}+\}?', '', content, flags=re.IGNORECASE)
                
                # 4. Eliminar enlaces crudos de YouTube
                content = re.sub(r'https?://(?:www\.)?youtube\.com/[^\s<>"{}]+', '', content)
                content = re.sub(r'https?://(?:www\.)?youtu\.be/[^\s<>"{}]+', '', content)
                
                # 5. Eliminar llaves sueltas
                content = re.sub(r'\}+\s*\n?', '', content)
                content = re.sub(r'\{+\s*\n?', '', content)
                
                # 6. Insertar shortcodes CORRECTOS después del front matter
                if videos_unicos:
                    frontmatter_match = re.search(r'\+\+\+.*?\+\+\+\n', content, re.DOTALL)
                    if frontmatter_match:
                        insert_pos = frontmatter_match.end()
                        videos_shortcode = '\n'.join([f'{{{{ youtube(id="{vid}") }}}}' for vid in videos_unicos])
                        content = content[:insert_pos] + '\n' + videos_shortcode + '\n\n' + content[insert_pos:]
                        total_videos += len(videos_unicos)
                
                # 7. Limpiar líneas vacías múltiples
                content = re.sub(r'\n{3,}', '\n\n', content)
                
                if content != original:
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(content)
                    archivos_modificados += 1

print(f"✅ Procesados {archivos_modificados} archivos")
print(f"🎬 Total de videos encontrados y corregidos: {total_videos}")
