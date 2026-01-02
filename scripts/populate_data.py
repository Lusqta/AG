import os
import django
import random
from datetime import timedelta
from django.utils import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dealership_crm.settings')
django.setup()

from django.contrib.auth.models import User, Group, Permission
from sales.models import Customer, Vehicle, Sale

def populate():
    print("Setting up groups and users...")
    
    # Create Groups
    managers_group, _ = Group.objects.get_or_create(name='Gerentes')
    sales_group, _ = Group.objects.get_or_create(name='Vendedores')
    
    # Create Admin User
    admin_user, _ = User.objects.get_or_create(username='admin', email='admin@example.com')
    admin_user.set_password('admin123')
    admin_user.is_superuser = True
    admin_user.is_staff = True
    admin_user.save()
    admin_user.groups.add(managers_group) # Also a manager

    # Create Manager User
    manager, _ = User.objects.get_or_create(username='gerente', email='gerente@example.com', first_name='Carlos', last_name='Gerente')
    manager.set_password('123456')
    manager.save()
    manager.groups.add(managers_group)

    # Create Salespeople
    sales_users = []
    for i in range(1, 4):
        u, _ = User.objects.get_or_create(username=f'vendedor{i}', email=f'vendedor{i}@example.com', first_name='João', last_name=f'Vendedor {i}')
        u.set_password('123456')
        u.save()
        u.groups.add(sales_group)
        sales_users.append(u)

    print("Populating initial data...")

    # Create Vehicles
    makes = ["Toyota", "Honda", "Ford", "BMW", "Mercedes", "Audi", "Fiat", "Chevrolet"]
    models = ["Corolla", "Civic", "Ranger", "X1", "C180", "A3", "Toro", "S10"]
    colors = ["Preto", "Branco", "Prata", "Azul", "Vermelho"]
    
    vehicles = []
    for i in range(12):
        v = Vehicle.objects.create(
            make=random.choice(makes),
            model=random.choice(models),
            year=random.randint(2019, 2025),
            price=random.randint(45000, 150000),
            vin=f"VIN{random.randint(100000, 999999)}",
            mileage=random.randint(0, 60000),
            color=random.choice(colors),
            status='available'
        )
        vehicles.append(v)

    # Create Customers
    customers = []
    names = [("Ana", "Silva"), ("Bruno", "Santos"), ("Carla", "Oliveira"), ("Daniel", "Souza")]
    for first, last in names:
        c = Customer.objects.create(
            first_name=first,
            last_name=last,
            email=f"{first.lower()}.{last.lower()}@email.com",
            phone=f"11 99999-000{len(customers)}",
            status='lead',
            assigned_to=random.choice(sales_users)
        )
        customers.append(c)

    # Create a Sale
    v_sold = vehicles[0]
    c_buyer = customers[0]
    s_person = sales_users[0]
    
    Sale.objects.create(
        vehicle=v_sold,
        customer=c_buyer,
        salesperson=s_person,
        sale_price=v_sold.price,
        sale_date=timezone.now().date(),
        notes="Venda realizada com sucesso."
    )
    
    print("Database populated successfully!")

if __name__ == '__main__':
    populate()
