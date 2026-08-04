#!/usr/bin/env python3
import os
import re

directorio = 'content'

# Lista de patrones específicos y sus reemplazos seguros
# Solo toca lo que coincide, el resto del archivo queda intacto.
patrones = [
    # 1. Arreglar shortcodes con llaves de más: {{ youtube(id="ID") }}}} -> {{ youtube(id="ID") }}
    (r'\{\{\s*youtube\(id="([a-zA-Z0-9_-]{11})"\)\s*\}+\}', r'{{ youtube(id="\1") }}'),
    
    # 2. Arreglar shortcodes sin llaves de apertura: youtube(id="ID") -> {{ youtube(id="ID") }}
    (r'(?<!\{)\s*youtube\(id="([a-zA-Z0-9_-]{11})"\)', r'{{ youtube(id="\1") }}'),
    
    # 3. Reemplazar enlaces de YouTube Shorts
    (r'https?://(?:www\.)?youtube\.com/shorts/([a-zA-Z0-9_-]{11})[^\s<>"{}]*', r'{{ youtube(id="\1") }}'),
    
    # 4. Reemplazar enlaces de YouTube Watch
    (r'https?://(?:www\.)?youtube\.com/watch\?v=([a-zA-Z0-9_-]{11})[^\s<>"{}]*', r'{{ youtube(id="\1") }}'),
    
    # 5. Reemplazar enlaces youtu.be
    (r'https?://(?:www\.)?youtu\.be/([a-zA-Z0-9_-]{11})[^\s<>"{}]*', r'{{ youtube(id="\1") }}'),
]

archivos_modificados = 0
total_videos_corregidos = 0

print("🔍 Iniciando conversión segura de videos de YouTube...")

for root, dirs, files in os.walk(directorio):
    for file in files:
        if file.endswith('.md'):
            filepath = os.path.join(root, file)
            
            with open(filepath, 'r', encoding='utf-8') as f:
                contenido = f.read()
            
            original = contenido
            videos_en_este_archivo = 0
            
            # Aplicar cada patrón de reemplazo
            for patron, reemplazo in patrones:
                # Contar cuántos hay antes de reemplazar
                matches = len(re.findall(patron, contenido))
                videos_en_este_archivo += matches
                
                # Reemplazar solo esa parte
                contenido = re.sub(patron, reemplazo, contenido)
            
            # Si el contenido cambió, guardamos el archivo
            if contenido != original:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(contenido)
                archivos_modificados += 1
                total_videos_corregidos += videos_en_este_archivo

print("=" * 50)
print("✅ ¡Proceso terminado con seguridad!")
print(f"📁 Archivos modificados: {archivos_modificados}")
print(f"🎬 Total de videos corregidos: {total_videos_corregidos}")
print("=" * 50)
