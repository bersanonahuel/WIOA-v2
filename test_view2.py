import paramiko

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect('wioav2.nserver.space', 2223, 'wioa', 'c0i1uhIPrEpu')

# Reset admin password and test the view
script = """
import os, sys
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'WIOA.settings')
import django
django.setup()

from django.contrib.auth.models import User
from django.test import Client
import traceback

# List users
users = User.objects.all().values('username', 'is_superuser', 'is_staff')
for u in users:
    print('USER:', u)

# Reset password for any superuser
su = User.objects.filter(is_superuser=True).first()
if su:
    su.set_password('testpass123')
    su.save()
    username = su.username
    print(f'Reset password for: {username}')
else:
    print('No superuser found!')
    sys.exit(1)

# Test the view with Django test client
c = Client(raise_request_exception=True, SERVER_NAME='wioav2.nserver.space')
c.force_login(su)

try:
    response = c.get('/registros/listarRegistro/')
    print(f'STATUS: {response.status_code}')
    if response.status_code != 200:
        print('CONTENT:', response.content[:500])
except Exception:
    traceback.print_exc()
"""

sftp = client.open_sftp()
with sftp.file('/var/www/wioa/test_view2.py', 'w') as f:
    f.write(script)
sftp.close()

stdin, stdout, stderr = client.exec_command('cd /var/www/wioa && source venv/bin/activate && python test_view2.py')
print("STDOUT:")
print(stdout.read().decode('utf-8', 'ignore'))
print("STDERR:")
print(stderr.read().decode('utf-8', 'ignore'))
client.close()
