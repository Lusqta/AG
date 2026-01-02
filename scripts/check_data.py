
import os
import django
from django.utils import timezone
from datetime import timedelta
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dealership_crm.settings')
django.setup()

from sales.models import Sale, Vehicle, Customer

def check_data():
    print("--- Verificando Dados para Gráficos ---")
    
    # 1. Total Sales
    total_sales_count = Sale.objects.count()
    print(f"Total de Vendas no Banco: {total_sales_count}")

    if total_sales_count == 0:
        print("ALERTA: Nenhuma venda encontrada. Os gráficos ficarão vazios.")
        return

    # 2. Vendas Recentes (últimos 12 meses)
    start_date = timezone.now() - timedelta(days=365)
    recent_sales = Sale.objects.filter(sale_date__gte=start_date)
    print(f"Vendas nos últimos 12 meses: {recent_sales.count()}")

    if recent_sales.count() == 0:
        print("ALERTA: Existem vendas antigas, mas nenhuma nos últimos 12 meses.")
        
    # 3. Simular Dados da View
    from django.db.models import Sum, Count
    from django.db.models.functions import TruncMonth

    monthly_sales = Sale.objects.filter(sale_date__gte=start_date)\
        .annotate(month=TruncMonth('sale_date'))\
        .values('month')\
        .annotate(total=Sum('sale_price'))\
        .order_by('month')
    
    print("\n--- Dados Agregados (Receita) ---")
    data = [float(entry['total']) for entry in monthly_sales]
    print(f"Valores: {data}")

    sales_by_make = Sale.objects.values('vehicle__make')\
        .annotate(count=Count('id'))\
        .order_by('-count')[:5]
    
    print("\n--- Dados Agregados (Marca) ---")
    makes = [entry['vehicle__make'] for entry in sales_by_make]
    print(f"Marcas: {makes}")

if __name__ == '__main__':
    check_data()
