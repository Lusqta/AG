import os
import django
import random
from datetime import timedelta, date
from django.utils import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dealership_crm.settings')
django.setup()

from django.contrib.auth.models import User, Group
from sales.models import Customer, Vehicle, Sale

def populate_rich():
    print("Populating rich data for charts...")
    
    # Ensure users exist
    admin = User.objects.get(username='admin')
    
    # Get or Create Salespeople
    salespeople = []
    for i in range(1, 4):
        u, _ = User.objects.get_or_create(username=f'vendedor{i}')
        if _:
            u.set_password('123456')
            u.first_name = 'João'
            u.last_name = f'Vendedor {i}'
            u.save()
            group = Group.objects.get(name='Vendedores')
            u.groups.add(group)
        salespeople.append(u)
    
    # Makes and Models
    car_db = {
        "Toyota": ["Corolla", "Hilux", "Yaris"],
        "Honda": ["Civic", "HR-V", "City"],
        "Ford": ["Ranger", "Mustang", "Territory"],
        "BMW": ["320i", "X1", "X5"],
        "Mercedes": ["C180", "GLA", "A200"],
    }
    
    colors = ["Branco", "Preto", "Prata", "Cinza", "Azul", "Vermelho"]
    
    # Generate 50 Past Sales (distributed over 12 months)
    today = timezone.now().date()
    
    for i in range(50):
        # Random Date in last 12 months
        days_ago = random.randint(0, 365)
        sale_date = today - timedelta(days=days_ago)
        
        make = random.choice(list(car_db.keys()))
        model = random.choice(car_db[make])
        
        # Create Vehicle (Sold)
        vehicle = Vehicle.objects.create(
            make=make,
            model=model,
            year=random.randint(2018, 2025),
            price=random.randint(60000, 300000),
            vin=f"VIN{random.randint(1000000, 9999999)}",
            mileage=random.randint(0, 50000),
            color=random.choice(colors),
            status='sold' # It's a past sale
        )
        
        # Create Customer
        customer, created = Customer.objects.get_or_create(
            email=f"cliente{i}@test.com",
            defaults={
                'first_name': f"Cliente{i}",
                'last_name': f"Sobrenome{i}",
                'phone': f"1199999{i:04d}",
                'status': 'purchased',
                'assigned_to': random.choice(salespeople)
            }
        )
        
        # Create Sale
        Sale.objects.create(
            vehicle=vehicle,
            customer=customer,
            salesperson=customer.assigned_to,
            sale_price=vehicle.price, # sold at list price
            sale_date=sale_date
        )

    # Generate some Available Inventory (10 cars)
    for i in range(10):
        make = random.choice(list(car_db.keys()))
        model = random.choice(car_db[make])
        Vehicle.objects.create(
            make=make,
            model=model,
            year=random.randint(2023, 2025),
            price=random.randint(70000, 350000),
            vin=f"NEW{random.randint(1000000, 9999999)}",
            mileage=0,
            color=random.choice(colors),
            status='available'
        )

    print("Data populated: 50 sales, 10 inventory items.")

if __name__ == '__main__':
    populate_rich()
