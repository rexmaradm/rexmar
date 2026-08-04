#!/usr/bin/env python3
import os
import re

def procesar_archivo(ruta):
    with open(ruta, 'r', encoding='utf-8') as f:
        contenido = f.read()

    original = contenido
    cambios = 0

    # 1. Arreglar shortcodes con llaves de más: {{ youtube(id="ID") }}}} -> {{ youtube(id="ID") }}
    contenido, n = re.subn(r'\{\{\s*youtube\(id="([a-zA-Z0-9_-]{11})"\)\s*\}+\}', r'{{ youtube(id="\1") }}', contenido)
    cambios += n

    # 2. Arreglar shortcodes sin llaves: youtube(id="ID") -> {{ youtube(id="ID") }}
    contenido, n = re.subn(r'(?<!\{)\s*youtube\(id="([a-zA-Z0-9_-]{11})"\)', r'{{ youtube(id="\1") }}', contenido)
    cambios += n

    # 3. Reemplazar enlaces estándar de YouTube
    patrones_enlaces = [
        r'https?://(?:www\.)?youtube\.com/watch\?v=([a-zA-Z0-9_-]{11})[^\s<>"{}]*',
        r'https?://(?:www\.)?youtu\.be/([a-zA-Z0-9_-]{11})[^\s<>"{}]*',
        r'https?://(?:www\.)?youtube\.com/shorts/([a-zA-Z0-9_-]{11})[^\s<>"{}]*'
    ]
    
    for patron in patrones_enlaces:
        contenido, n = re.subn(patron, r'{{ youtube(id="\1") }}', contenido)
        cambios += n

    # 4. Reemplazar iframes de YouTube
    patron_iframe = r'<iframe[^>]+src="[^"]*(?:youtube\.com/embed|youtube\.com/v)/([a-zA-Z0-9_-]{11})[^"]*"[^>]*>.*?</iframe>'
    contenido, n = re.subn(patron_iframe, r'{{ youtube(id="\1") }}', contenido, flags=re.DOTALL)
    cambios += n

    # Guardar solo si hubo cambios
    if contenido != original:
        with open(ruta, 'w', encoding='utf-8') as f:
            f.write(contenido)
        return cambios
    return 0

print("🔍 Iniciando búsqueda y reemplazo en línea...")
print("📁 Directorio base: content/")
print("=" * 60)

total_videos = 0
archivos_modificados = 0

# Recorrer TODOS los subdirectorios de content/
for root, dirs, files in os.walk('content'):
    for archivo in files:
        if archivo.endswith('.md'):
            ruta_completa = os.path.join(root, archivo)
            cambios = procesar_archivo(ruta_completa)
            if cambios > 0:
                print(f"  ✅ {cambios} videos arreglados en: {ruta_completa}")
                total_videos += cambios
                archivos_modificados += 1

print("=" * 60)
print(f"\n🎉 ¡TERMINADO!")
print(f"   Archivos modificados: {archivos_modificados}")
print(f"   Total de videos corregidos: {total_videos}")
