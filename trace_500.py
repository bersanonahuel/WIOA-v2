import paramiko
client=paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect('wioav2.nserver.space',2223,'wioa','c0i1uhIPrEpu')
script = '''import os
import sys
import django
os.environ.setdefault(\'DJANGO_SETTINGS_MODULE\', \'WIOA.settings\')
django.setup()
from django.test import Client
from django.contrib.auth.models import User
import traceback
c = Client(raise_request_exception=True)
user = User.objects.filter(is_superuser=True).first()
if not user:
    user = User.objects.first()
c.force_login(user)
try:
    response = c.get(\'/registros/listarRegistro/\', SERVER_NAME=\'localhost\')
    print(f\'Success: {response.status_code}\')
except Exception:
    traceback.print_exc()
'''
sftp = client.open_sftp()
with sftp.file('/var/www/wioa/test_view.py', 'w') as f:
    f.write(script)
sftp.close()
stdin,stdout,stderr=client.exec_command('cd /var/www/wioa && source venv/bin/activate && python test_view.py')
print(stdout.read().decode())
print(stderr.read().decode())
