import os
import sys
import django

base_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(base_dir)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'WIOA.settings')
django.setup()

from django.contrib.auth.models import User

if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin')
    print("Superuser 'admin' created with password 'admin'")
else:
    u = User.objects.get(username='admin')
    u.set_password('admin')
    u.save()
    print("Superuser 'admin' password reset to 'admin'")
