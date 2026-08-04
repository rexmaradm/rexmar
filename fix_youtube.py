import os
import re

print("🔍 Convirtiendo enlaces de YouTube...")
archivos_modificados = 0
videos_convertidos = 0

for root, dirs, files in os.walk('content'):
    for file in files:
        if file.endswith('.md'):
            filepath = os.path.join(root, file)
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original = content
            videos_en_archivo = []
            
            # Buscar TODOS los formatos de YouTube
            videos_en_archivo.extend(re.findall(r'youtube\.com/watch\?v=([a-zA-Z0-9_-]{11})', content))
            videos_en_archivo.extend(re.findall(r'youtu\.be/([a-zA-Z0-9_-]{11})', content))
            videos_en_archivo.extend(re.findall(r'youtube\.com/shorts/([a-zA-Z0-9_-]{11})', content))
            
            # Eliminar enlaces crudos de YouTube
            content = re.sub(r'https?://(?:www\.)?youtube\.com/[^\s<>"{}]+', '', content)
            content = re.sub(r'https?://(?:www\.)?youtu\.be/[^\s<>"{}]+', '', content)
            
            # Eliminar shortcodes rotos
            content = re.sub(r'\{\{\s*youtube.*?\}\}', '', content, flags=re.IGNORECASE)
            
            # Agregar shortcodes limpios al inicio (después del front matter)
            if videos_en_archivo:
                video_ids = list(set(videos_en_archivo))
                frontmatter_match = re.search(r'\+\+\+.*?\+\+\+\n', content, re.DOTALL)
                if frontmatter_match:
                    insert_pos = frontmatter_match.end()
                    videos_shortcode = '\n'.join([f'{{{{ youtube(id="{vid}") }}}}' for vid in video_ids])
                    content = content[:insert_pos] + '\n' + videos_shortcode + '\n\n' + content[insert_pos:]
                    videos_convertidos += len(video_ids)
            
            if content != original:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
                archivos_modificados += 1

print(f"✅ Procesados {archivos_modificados} archivos")
print(f"🎬 Convertidos {videos_convertidos} videos de YouTube")
