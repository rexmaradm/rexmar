import os
import re

pattern = re.compile(r'<footer[^>]*>.*?</footer>', re.IGNORECASE | re.DOTALL)

for root, dirs, files in os.walk('content'):
    for file in files:
        if file.endswith('.md'):
            filepath = os.path.join(root, file)
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            new_content, num_subs = pattern.subn('', content)
            
            if num_subs > 0:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print(f"✅ Footer eliminado de: {filepath}")
