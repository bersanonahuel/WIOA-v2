import os
import django
import sys

sys.path.append(r'c:\s\Sistema\wiao\wioa')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "WIOA.settings")
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()
username = 'testadmin'
password = 'Password123!'
email = 'admin@example.com'

if User.objects.filter(username=username).exists():
    u = User.objects.get(username=username)
    u.set_password(password)
    u.save()
    print("User updated")
else:
    u = User.objects.create_superuser(username, email, password)
    print("User created")

