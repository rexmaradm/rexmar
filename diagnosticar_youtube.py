#!/usr/bin/env python3
import os
import re

print("=" * 70)
print("🔍 DIAGNÓSTICO COMPLETO DE VIDEOS DE YOUTUBE")
print("=" * 70)

total_videos = 0
archivos_con_videos = {}

for root, dirs, files in os.walk('content'):
    for file in files:
        if file.endswith('.md'):
            filepath = os.path.join(root, file)
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Buscar TODOS los formatos posibles
            formatos = {
                'shortcode_correcto': re.findall(r'\{\{\s*youtube\(id="([a-zA-Z0-9_-]{11})"\)\s*\}\}', content),
                'shortcode_mal_formado': re.findall(r'\{\{\s*youtube\(id="([a-zA-Z0-9_-]{11})"\)\s*\}+\}', content),
                'sin_llaves': re.findall(r'youtube\(id="([a-zA-Z0-9_-]{11})"\)', content),
                'youtube_watch': re.findall(r'youtube\.com/watch\?v=([a-zA-Z0-9_-]{11})', content),
                'youtu_be': re.findall(r'youtu\.be/([a-zA-Z0-9_-]{11})', content),
                'youtube_shorts': re.findall(r'youtube\.com/shorts/([a-zA-Z0-9_-]{11})', content),
            }
            
            total_en_archivo = sum(len(v) for v in formatos.values())
            
            if total_en_archivo > 0:
                archivos_con_videos[filepath] = {
                    'total': total_en_archivo,
                    'formatos': formatos
                }
                total_videos += total_en_archivo

# Mostrar resultados
print(f"\n📊 RESUMEN:")
print(f"   Total de archivos con videos: {len(archivos_con_videos)}")
print(f"   Total de videos encontrados: {total_videos}")

print(f"\n📁 ARCHIVOS CON VIDEOS:")
print("-" * 70)

for filepath, data in sorted(archivos_con_videos.items()):
    print(f"\n📄 {filepath}")
    print(f"   Total videos: {data['total']}")
    
    for formato, videos in data['formatos'].items():
        if videos:
            print(f"   ├─ {formato}: {len(videos)}")
            for vid in videos:
                print(f"   │  └─ {vid}")

print("\n" + "=" * 70)
print("✅ Diagnóstico completado")
print("=" * 70)
