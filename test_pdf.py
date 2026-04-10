import paramiko

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect('wioav2.nserver.space', 2223, 'wioa', 'c0i1uhIPrEpu')

script = """
import os, sys, traceback
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'WIOA.settings')
import django
django.setup()

from django.test import Client
from django.contrib.auth.models import User

su = User.objects.filter(is_superuser=True).first()
c = Client(raise_request_exception=True, SERVER_NAME='wioav2.nserver.space')
c.force_login(su)

try:
    response = c.get('/registros/printPdf/1')
    print(f'STATUS: {response.status_code}')
except Exception:
    traceback.print_exc()
"""

sftp = client.open_sftp()
with sftp.file('/var/www/wioa/test_pdf.py', 'w') as f:
    f.write(script)
sftp.close()

stdin, stdout, stderr = client.exec_command(
    'cd /var/www/wioa && source venv/bin/activate && python test_pdf.py 2>&1'
)
print(stdout.read().decode('utf-8', 'ignore'))
client.close()
