import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dealership_crm.settings')
django.setup()

from django.contrib.auth.models import User, Group

def setup_fresh_crm():
    print("Clean setup initiating...")
    
    # 1. Create Groups
    print("Creating groups...")
    managers_group, _ = Group.objects.get_or_create(name='Gerentes')
    sales_group, _ = Group.objects.get_or_create(name='Vendedores')
    
    # 2. Create Admin User
    print("Creating admin user...")
    if not User.objects.filter(username='admin').exists():
        admin_user = User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
        # Add admin to managers group just in case logic checks group
        admin_user.groups.add(managers_group)
        admin_user.save()
        print("Admin user created (admin/admin123).")
    else:
        print("Admin user already exists.")

    print("System reset complete. No sample data (vehicles/customers) added.")

if __name__ == '__main__':
    setup_fresh_crm()
