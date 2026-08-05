import os
import re

# Patrón que busca:
# 1. <iframe ... drive.google.com/file/d/ ... ></iframe>
# 2. Seguido de espacios o saltos de línea opcionales (\s*)
# 3. Seguido de **Escuchar y cualquier texto hasta el cierre **
pattern = re.compile(
    r'<iframe[^>]*drive\.google\.com/file/d/[^>]*></iframe>\s*\*\*Escuchar.*?\*\*', 
    re.IGNORECASE | re.DOTALL
)

archivos_modificados = 0
total_eliminaciones = 0

print("🔍 Buscando y eliminando iframes de Drive y leyendas 'Escuchar'...\n")

for root, dirs, files in os.walk('content'):
    for file in files:
        if file.endswith('.md'):
            filepath = os.path.join(root, file)
            
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Reemplazar el patrón por una cadena vacía (borrarlo)
            new_content, num_subs = pattern.subn('', content)
            
            if num_subs > 0:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                archivos_modificados += 1
                total_eliminaciones += num_subs
                print(f"✅ Limpio: {filepath} ({num_subs} bloques eliminados)")

print(f"\n🎉 ¡Proceso terminado!")
print(f"   - Archivos modificados: {archivos_modificados}")
print(f"   - Total de bloques eliminados: {total_eliminaciones}")
