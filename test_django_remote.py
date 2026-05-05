import paramiko
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect('wioav2.nserver.space', port=2223, username='wioa', password='c0i1uhIPrEpu')

test_script = """
import os
import django
from django.test import Client

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'WIOA.settings')
django.setup()

c = Client(HTTP_HOST='wioav2.nserver.space')
try:
    response = c.get('/')
    print('STATUS:', response.status_code)
except Exception as e:
    print('ERROR:', e)
"""

cmd = f"cd /var/www/wioa && cat << 'EOF' > test_django.py\n{test_script}\nEOF\n/var/www/wioa/venv/bin/python test_django.py"
stdin, stdout, stderr = client.exec_command(cmd)

out = stdout.read().decode('utf-8', errors='ignore')
print("OUT:", out)
