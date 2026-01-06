
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
    print("Iniciando população de dados aprimorada...")
    
    # --- 1. Usuários e Grupos ---
    
    # Garante que grupos existem
    group_vendedores, _ = Group.objects.get_or_create(name='Vendedores')
    group_gerentes, _ = Group.objects.get_or_create(name='Gerentes')
    
    # Admin (Superuser)
    if not User.objects.filter(username='admin').exists():
         User.objects.create_superuser('admin', 'admin@example.com', 'admin1234')

    # Dados de Funcionários
    staff_data = [
        # (username, first_name, last_name, group_obj, password)
        ('ricardo_gerente', 'Ricardo', 'Almeida', group_gerentes, 'senha123'),
        ('juliana_vendas', 'Juliana', 'Costa', group_vendedores, 'senha123'),
        ('marcos_vendas', 'Marcos', 'Oliveira', group_vendedores, 'senha123'),
        ('fernanda_vendas', 'Fernanda', 'Lima', group_vendedores, 'senha123'),
        ('pedro_vendas', 'Pedro', 'Santos', group_vendedores, 'senha123'),
        ('camila_vendas', 'Camila', 'Rocha', group_vendedores, 'senha123'),
    ]
    
    staff_users = []
    
    for username, first, last, group, pwd in staff_data:
        u, created = User.objects.get_or_create(username=username)
        if created:
            u.set_password(pwd)
            print(f"Usuário criado: {username}")
        
        # Atualiza dados para garantir consistência
        u.first_name = first
        u.last_name = last
        u.save()
        
        u.groups.add(group)
        staff_users.append(u)

    # Filtra apenas vendedores para atribuir leads/vendas
    salesforce = [u for u in staff_users if group_vendedores in u.groups.all()]
    if not salesforce: # Fallback se não criou ninguém
        salesforce = [User.objects.get(username='admin')]

    # --- 2. Listas de Dados para Geração Aleatória ---
    
    first_names = [
        "Ana", "Bruno", "Carlos", "Daniela", "Eduardo", "Fabiana", "Gabriel", "Helena", 
        "Igor", "Julia", "Lucas", "Mariana", "Nicolas", "Olivia", "Paulo", "Rafael", 
        "Sabrina", "Thiago", "Vitoria", "Wagner", "Amanda", "Beatriz", "Diego", "Larissa"
    ]
    
    last_names = [
        "Silva", "Santos", "Oliveira", "Souza", "Rodrigues", "Ferreira", "Alves", 
        "Pereira", "Lima", "Gomes", "Costa", "Ribeiro", "Martins", "Carvalho", 
        "Almeida", "Lopes", "Soares", "Fernandes", "Vieira", "Moreira"
    ]
    
    car_db = {
        "Toyota": ["Corolla XEI", "Corolla Altis", "Hilux SRV", "Hilux SW4", "Yaris XLS", "Corolla Cross"],
        "Honda": ["Civic Touring", "Civic EXL", "HR-V EXL", "HR-V Touring", "City Touring", "ZR-V"],
        "Volkswagen": ["T-Cross Highline", "Nivus Highline", "Polo GTS", "Taos Highline", "Jetta GLI", "Amarok V6"],
        "Jeep": ["Renegade Longitude", "Compass Limited", "Compass Serie S", "Commander Overland"],
        "Chevrolet": ["Onix Premier", "Tracker Premier", "S10 High Country", "Equinox Premier"],
        "BMW": ["320i M Sport", "X1 sDrive20i", "X3 xDrive30e", "X5 xDrive45e"],
        "Mercedes-Benz": ["C300 AMG Line", "GLA 200 AMG Line", "A200 Advance", "GLC 300 Coupe"],
        "Hyundai": ["Creta Ultimate", "HB20 Platinum Plus", "Tucson GLS"],
        "Fiat": ["Toro Ultra", "Toro Volcano", "Pulse Abarth", "Fastback Limited"],
        "Ford": ["Ranger Limited", "Maverick Lariat", "Bronco Sport", "Mustang Mach 1"],
    }
    
    colors = ["Branco Pérola", "Preto Eclipse", "Prata Metálico", "Cinza Grafite", "Azul Safira", "Vermelho Tornado", "Verde Militar", "Branco Sólido"]

    # --- 3. Gerar Clientes e Vendas (Histórico) ---
    
    today = timezone.now().date()
    
    # Vamos gerar 80 vendas históricas nos últimos 15 meses para ter gráficos bonitos
    print("Gerando histórico de vendas...")
    
    for i in range(80):
        # Data aleatória
        days_ago = random.randint(1, 450)
        sale_date = today - timedelta(days=days_ago)
        
        # Dados do Veículo
        make = random.choice(list(car_db.keys()))
        model = random.choice(car_db[make])
        base_price = 80000 + (len(model) * 5000) # Preço base "fake" baseado no nome pra variar
        if make in ["BMW", "Mercedes-Benz", "Ford"]: # Marcas mais caras
            base_price *= 2.5
            
        real_price = base_price + random.randint(-5000, 15000)
        
        # Cria Veículo (VENDIDO)
        vehicle = Vehicle.objects.create(
            make=make,
            model=model,
            year=random.randint(2019, 2024),
            price=real_price,
            vin=f"{make[:3].upper()}{random.randint(10000, 99999)}BR{random.randint(100,999)}",
            license_plate=f"{''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ', k=3))}{random.randint(1,9)}{random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')}{random.randint(10,99)}",
            mileage=random.randint(1000, 80000),
            color=random.choice(colors),
            status='sold',
            image_url=f"https://loremflickr.com/640/480/{make},{model.split()[0]}" # Imagem genérica
        )
        
        # Cria Cliente
        f_name = random.choice(first_names)
        l_name = random.choice(last_names)
        
        customer, _ = Customer.objects.get_or_create(
            email=f"{f_name.lower()}.{l_name.lower()}{random.randint(1,999)}@email.com",
            defaults={
                'first_name': f_name,
                'last_name': l_name,
                'phone': f"(11) 9{random.randint(1000, 9999)}-{random.randint(1000, 9999)}",
                'status': 'purchased',
                'assigned_to': random.choice(salesforce)
            }
        )
        
        # Registra Venda
        sale = Sale.objects.create(
            vehicle=vehicle,
            customer=customer,
            salesperson=customer.assigned_to,
            sale_price=real_price, 
            sale_date=sale_date
        )
        
        # --- Create Payment for Sale ---
        from sales.models import Payment
        
        payment_type = random.choice(['debit', 'credit_spot', 'credit_installment', 'pix'])
        installments = 1
        
        if payment_type == 'credit_installment':
            installments = random.randint(2, 12)
        elif payment_type == 'pix':
            if random.random() > 0.8: # 20% chance of scheduled/split pix
                 installments = random.randint(2, 4)
        
        payment_date_final = sale_date
        if payment_type == 'pix' and random.random() > 0.7:
             # Simula um pix agendado levemente pro futuro (1 dia) ou mesmo dia
             payment_date_final = sale_date + timedelta(days=random.randint(0, 1))

        Payment.objects.create(
            sale=sale,
            payment_type=payment_type,
            amount=real_price,
            payment_date=payment_date_final,
            status='confirmed', # Historical sales are confirmed
            installments=installments,
            bank="Banco Exemplo S.A." if payment_type == 'credit_installment' else ""
        )
        
    print("Populado com 80 vendas históricas.")

    # --- 4. Gerar Estoque Disponível (Inventory) ---
    print("Gerando estoque atual...")
    
    for i in range(25): # 25 carros no estoque
        make = random.choice(list(car_db.keys()))
        model = random.choice(car_db[make])
        
        base_price = 90000 + (len(model) * 5000)
        if make in ["BMW", "Mercedes-Benz"]:
            base_price *= 2.2
            
        final_price = base_price + random.randint(-2000, 10000)
        
        year_veh = random.randint(2021, 2025)
        mileage_veh = 0 if year_veh == 2025 else random.randint(5000, 60000)
        
        Vehicle.objects.create(
            make=make,
            model=model,
            year=year_veh,
            price=final_price,
            vin=f"NEW{random.randint(10000, 99999)}stock",
            license_plate=f"{''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ', k=3))}{random.randint(1,9)}{random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')}{random.randint(10,99)}",
            mileage=mileage_veh,
            color=random.choice(colors),
            status='available',
            image_url=f"https://loremflickr.com/640/480/{make},{model.split()[0]}"
        )

    # --- 5. Gerar Leads (Clientes interessados, sem compra) ---
    print("Gerando leads...")
    
    for i in range(15):
        f_name = random.choice(first_names)
        l_name = random.choice(last_names)
        
        Customer.objects.create(
            first_name=f_name,
            last_name=l_name,
            email=f"lead.{f_name.lower()}{i}@provedor.com",
            phone=f"(21) 9{random.randint(1000, 9999)}-{random.randint(1000, 9999)}",
            status='lead',
            assigned_to=random.choice(salesforce)
        )

    print("=== POPULAÇÃO DE DADOS CONCLUÍDA ===")
    print("Usuários criados (senha padrao: senha123):")
    for u in staff_users:
        print(f" - {u.username} ({u.groups.first().name})")

if __name__ == '__main__':
    populate_rich()
