import os
import django

import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dealership_crm.settings')
django.setup()

from sales.models import Sale, Customer, Vehicle
from django.contrib.auth.models import User

def wipe_data():
    print("Iniciando limpeza de dados do CRM...")
    
    # Order matters due to foreign keys (Sale -> Customer/Vehicle)
    deleted_sales = Sale.objects.all().delete()
    print(f"Vendas removidas: {deleted_sales[0]}")
    
    deleted_customers = Customer.objects.all().delete()
    print(f"Clientes removidos: {deleted_customers[0]}")
    
    deleted_vehicles = Vehicle.objects.all().delete()
    print(f"Veículos removidos: {deleted_vehicles[0]}")
    
    # Optional: Delete non-superuser users?
    # keeping users for now to allow login.
    print("Dados de negócio limpos com sucesso!")
    print("Nota: Usuários e Grupos foram mantidos para permitir acesso.")

if __name__ == '__main__':
    wipe_data()
