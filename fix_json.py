import json

data = json.load(open('datadump_wioa.json', encoding='utf-8'))
for item in data:
    for k, v in item['fields'].items():
        if isinstance(v, str) and len(v) > 50 and k not in ['comentario', 'password']:
            print(f"TRUNCATING {item['model']} {k}: {v}")
            item['fields'][k] = v[:50]

json.dump(data, open('datadump_wioa_fixed.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
print("Fix applied.")
