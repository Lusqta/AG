import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dealership_crm.settings')
django.setup()

from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from sales.models import Sale, Vehicle, Customer

def create_groups():
    # 1. Grupo Gerentes
    managers, created = Group.objects.get_or_create(name='Gerentes')
    if created:
        print("Grupo 'Gerentes' criado.")
    else:
        print("Grupo 'Gerentes' já existe.")

    # Permissions for Managers (Can delete)
    # They usually have all permissions, but specifically we want to ensure they exist
    # If we want to be specific, we can add delete permissions here.
    # For now, the check in views.py relies on group membership, which is enough.
    
    # 2. Grupo Vendedores
    salespeople, created = Group.objects.get_or_create(name='Vendedores')
    if created:
        print("Grupo 'Vendedores' criado.")
    else:
        print("Grupo 'Vendedores' já existe.")
        
    print("Grupos configurados com sucesso!")

if __name__ == '__main__':
    create_groups()
