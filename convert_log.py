import io
try:
    with io.open('C:/s/Sistema/wiao/wioa/import_log.txt', encoding='utf-16le') as f:
        content = f.read()
    with io.open('C:/s/Sistema/wiao/wioa/import_log_utf8.txt', 'w', encoding='utf-8') as f:
        f.write(content)
except Exception as e:
    print(e)
