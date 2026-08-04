#!/usr/bin/env python3
import os
import re

def procesar_archivo(ruta):
    with open(ruta, 'r', encoding='utf-8') as f:
        contenido = f.read()

    original = contenido
    cambios = 0

    # 1. Corregir shortcodes con llaves extras: {{ youtube(id="ID") }}}} -> {{ youtube(id="ID") }}
    # Este regex busca {{ youtube(id="...") seguido de una o más llaves de cierre
    patron_llaves = r'\{\{\s*youtube\(id="([a-zA-Z0-9_-]{11})"\)\s*\}+\}'
    contenido, n = re.subn(patron_llaves, r'{{ youtube(id="\1") }}', contenido)
    cambios += n

    # 2. Corregir shortcodes sin llaves de apertura: youtube(id="ID") -> {{ youtube(id="ID") }}
    patron_sin_llaves = r'(?<!\{)\s*youtube\(id="([a-zA-Z0-9_-]{11})"\)'
    contenido, n = re.subn(patron_sin_llaves, r'{{ youtube(id="\1") }}', contenido)
    cambios += n

    # 3. Convertir enlaces youtube.com/watch?v=
    patron_watch = r'https?://(?:www\.)?youtube\.com/watch\?v=([a-zA-Z0-9_-]{11})[^\s<>"{}]*'
    contenido, n = re.subn(patron_watch, r'{{ youtube(id="\1") }}', contenido)
    cambios += n

    # 4. Convertir enlaces youtu.be/
    patron_youtu = r'https?://(?:www\.)?youtu\.be/([a-zA-Z0-9_-]{11})[^\s<>"{}]*'
    contenido, n = re.subn(patron_youtu, r'{{ youtube(id="\1") }}', contenido)
    cambios += n

    # 5. Convertir enlaces youtube.com/shorts/
    patron_shorts = r'https?://(?:www\.)?youtube\.com/shorts/([a-zA-Z0-9_-]{11})[^\s<>"{}]*'
    contenido, n = re.subn(patron_shorts, r'{{ youtube(id="\1") }}', contenido)
    cambios += n

    # 6. Convertir iframes de YouTube
    patron_iframe = r'<iframe[^>]+src="[^"]*(?:youtube\.com/embed|youtube\.com/v)/([a-zA-Z0-9_-]{11})[^"]*"[^>]*>.*?</iframe>'
    contenido, n = re.subn(patron_iframe, r'{{ youtube(id="\1") }}', contenido, flags=re.DOTALL)
    cambios += n

    # Guardar solo si hubo cambios
    if contenido != original:
        with open(ruta, 'w', encoding='utf-8') as f:
            f.write(contenido)
        return cambios
    return 0

print("🔍 Iniciando búsqueda y reemplazo...")
print("📁 Directorio base: content/")
print("=" * 60)

total_videos = 0
archivos_modificados = 0

for root, dirs, files in os.walk('content'):
    for archivo in files:
        if archivo.endswith('.md'):
            ruta_completa = os.path.join(root, archivo)
            cambios = procesar_archivo(ruta_completa)
            if cambios > 0:
                print(f"  ✅ {cambios} videos en: {ruta_completa}")
                total_videos += cambios
                archivos_modificados += 1

print("=" * 60)
print(f"\n ¡TERMINADO!")
print(f"   Archivos modificados: {archivos_modificados}")
print(f"   Total de videos corregidos: {total_videos}")
