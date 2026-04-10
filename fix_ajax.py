import os

path = r'apps\registros\views.py'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace('request.is_ajax()', "request.headers.get('x-requested-with') == 'XMLHttpRequest'")

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print(f"Replaced all occurrences of is_ajax in {path}")
