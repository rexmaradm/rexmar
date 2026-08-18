import pathlib
import re
import sys
from datetime import date

CONTENT_DIR = pathlib.Path("content")
TODAY = date.today().isoformat()

# Lista de archivos problemáticos (puedes copiarla del warning)
problem_files = [
    "home/recetas/cocinar1.md",
    "home/formas-de-uso-y-tips/sarna.md",
    "home/formas-de-uso-y-tips/hemorroides.md",
    "home/formas-de-uso-y-tips/calculadora-isotonica.md",
    "home/formas-de-uso-y-tips/prueba.md",
    "home/formas-de-uso-y-tips/homocisteina.md",
    "home/formas-de-uso-y-tips/trans-IV-hemorr.md",
    "home/formas-de-uso-y-tips/carcinoma.md",
    "home/formas-de-uso-y-tips/iv.md",
    "home/formas-de-uso-y-tips/ateromatosis.md",
    "home/formas-de-uso-y-tips/melanoma.md",
    "home/formas-de-uso-y-tips/osteocalcina.md",
    "home/formas-de-uso-y-tips/bebidaenergetica.md",
    "home/formas-de-uso-y-tips/oxidonitrico.md",
    "home/formas-de-uso-y-tips/permeabilidad.md",
    "sociales/donaciones.md"
]

for rel_path in problem_files:
    file_path = CONTENT_DIR / rel_path
    if not file_path.exists():
        print(f"⚠️ No encontrado: {file_path}")
        continue

    content = file_path.read_text(encoding="utf-8")
    
    # Verifica si ya tiene una fecha válida en el front-matter TOML
    # Busca líneas como: date = 2024-01-01
    if re.search(r'^date\s*=\s*\d{4}-\d{2}-\d{2}', content, re.MULTILINE):
        print(f"✓ OK (ya tiene fecha): {rel_path}")
        continue

    # Si no tiene fecha, la insertamos después del título
    # Buscamos la línea title = "..."
    match = re.search(r'^(title\s*=\s*".*")', content, re.MULTILINE)
    if match:
        insert_pos = match.end()
        # Insertar nueva línea de fecha
        new_content = content[:insert_pos] + f'\ndate = {TODAY}' + content[insert_pos:]
        file_path.write_text(new_content, encoding="utf-8")
        print(f"🔧 Arreglado (fecha añadida): {rel_path}")
    else:
        print(f"❌ Error: No se encontró título en {rel_path}")

print("\n¡Reparación completada! Reinicia Zola.")   
