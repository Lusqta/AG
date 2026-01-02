import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dealership_crm.settings')
django.setup()

from django.contrib.auth.models import User

try:
    u = User.objects.get(username='admin')
    u.set_password('admin123')
    u.save()
    print("Password set for admin.")
except User.DoesNotExist:
    print("User admin does not exist.")
