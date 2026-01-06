from django.shortcuts import render, redirect, get_object_or_404
import os
from django.core.paginator import Paginator
from django.db.models import Sum, Count, ProtectedError, Q
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.contrib import messages
from datetime import timedelta
from django.utils import timezone
from .models import Vehicle, Customer, Sale
from .forms import VehicleForm, CustomerForm, SaleForm, UserForm
from django.db import transaction

def is_manager_or_superuser(user):
    return user.is_superuser or user.groups.filter(name='Gerentes').exists()

def is_superuser(user):
    return user.is_superuser

from django.db.models.functions import TruncMonth
import json


@login_required
def dashboard(request):
    # KPIs Básicos
    total_sales = Sale.objects.aggregate(total=Sum('sale_price'))['total'] or 0
    vehicles_sold = Vehicle.objects.filter(status='sold').count()
    vehicles_available = Vehicle.objects.filter(status='available').count()
    active_leads = Customer.objects.filter(status='lead').count()
    recent_sales = Sale.objects.select_related('vehicle', 'customer', 'salesperson').order_by('-sale_date')[:5]

    # Gráfico 1: Evolução do Faturamento Mensal (Últimos 12 meses)
    start_date = timezone.now() - timedelta(days=365)
    monthly_sales = Sale.objects.filter(sale_date__gte=start_date)\
        .annotate(month=TruncMonth('sale_date'))\
        .values('month')\
        .annotate(total=Sum('sale_price'))\
        .order_by('month')
    
    # --- Prepare Data for Chart.js (Frontend) ---
    
    # Chart 1: Revenue data
    rev_labels = [entry['month'].strftime('%b/%Y') for entry in monthly_sales]
    rev_data = [float(entry['total']) for entry in monthly_sales]

    # Chart 2: Sales by Make data
    sales_by_make = Sale.objects.values('vehicle__make').annotate(count=Count('id')).order_by('-count')[:5]
    make_labels = [entry['vehicle__make'] for entry in sales_by_make]
    make_data = [entry['count'] for entry in sales_by_make]

    # Chart 3: Top Salesperson data
    sales_by_person = Sale.objects.values('salesperson__username', 'salesperson__first_name').annotate(total=Sum('sale_price')).order_by('-total')[:5]
    person_labels = [entry['salesperson__first_name'] or entry['salesperson__username'] for entry in sales_by_person]
    person_data = [float(entry['total']) for entry in sales_by_person]

    context = {
        'total_sales': total_sales,
        'vehicles_sold': vehicles_sold,
        'vehicles_available': vehicles_available,
        'active_leads': active_leads,
        'recent_sales': recent_sales,
        'active_tab': 'dashboard',
        'available_months': Sale.objects.dates('sale_date', 'month', order='DESC'),
        # JSON Data for JS Charts
        'rev_labels': json.dumps(rev_labels),
        'rev_data': json.dumps(rev_data),
        'make_labels': json.dumps(make_labels),
        'make_data': json.dumps(make_data),
        'person_labels': json.dumps(person_labels),
        'person_data': json.dumps(person_data),
    }
    return render(request, 'sales/dashboard.html', context)

@login_required
def vehicle_list(request):
    query = request.GET.get('q', '')
    vehicles_list = Vehicle.objects.all().order_by('-year')

    if query:
        vehicles_list = vehicles_list.filter(
            Q(make__icontains=query) | 
            Q(model__icontains=query) |
            Q(vin__icontains=query)
        )

    paginator = Paginator(vehicles_list, 9)  # Show 9 vehicles per page (3x3 grid).
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'sales/vehicle_list.html', {
        'vehicles': page_obj, 
        'active_tab': 'vehicles',
        'query': query,
        'can_delete': is_manager_or_superuser(request.user)
    })

@login_required
def add_vehicle(request):
    if request.method == 'POST':
        form = VehicleForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Veículo adicionado com sucesso.')
            return redirect('vehicle_list')
    else:
        form = VehicleForm()
    return render(request, 'sales/form.html', {'form': form, 'title': 'Adicionar Veículo', 'active_tab': 'vehicles'})

@login_required
def edit_vehicle(request, pk):
    vehicle = get_object_or_404(Vehicle, pk=pk)
    if request.method == 'POST':
        form = VehicleForm(request.POST, request.FILES, instance=vehicle)
        if form.is_valid():
            form.save()
            messages.success(request, 'Veículo atualizado com sucesso.')
            return redirect('vehicle_list')
    else:
        form = VehicleForm(instance=vehicle)
    return render(request, 'sales/form.html', {'form': form, 'title': f'Editar {vehicle}', 'active_tab': 'vehicles'})

@login_required
@user_passes_test(is_manager_or_superuser)
def delete_vehicle(request, pk):
    vehicle = get_object_or_404(Vehicle, pk=pk)
    if vehicle.status == 'sold':
        messages.error(request, "Não é possível excluir um veículo que já foi vendido.")
        return redirect('vehicle_list')
        
    if request.method == 'POST':
        vehicle.delete()
        messages.success(request, 'Veículo removido do estoque.')
        return redirect('vehicle_list')
    return render(request, 'sales/confirm_delete.html', {'obj': vehicle, 'title': 'Deletar Veículo'})

@login_required
def customer_list(request):
    query = request.GET.get('q', '')
    customers_list = Customer.objects.select_related('assigned_to').all().order_by('-created_at')

    if query:
        customers_list = customers_list.filter(
            Q(first_name__icontains=query) | 
            Q(last_name__icontains=query) |
            Q(email__icontains=query) |
            Q(phone__icontains=query)
        )

    paginator = Paginator(customers_list, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'sales/customer_list.html', {
        'customers': page_obj, 
        'active_tab': 'customers',
        'query': query,
        'can_delete': is_manager_or_superuser(request.user)
    })

@login_required
def add_customer(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            customer = form.save(commit=False)
            if not customer.assigned_to:
                customer.assigned_to = request.user
            customer.save()
            
            # Check for 'next' parameter to redirect back
            next_url = request.GET.get('next') or request.POST.get('next')
            if next_url:
                messages.success(request, 'Cliente adicionado. Continue sua venda.')
                return redirect(next_url)
            
            return redirect('customer_list')
    else:
        form = CustomerForm(initial={'assigned_to': request.user})
    
    context = {
        'form': form, 
        'title': 'Adicionar Cliente', 
        'active_tab': 'customers',
        'next_url': request.GET.get('next')
    }
    return render(request, 'sales/form.html', context)

@login_required
def customer_detail(request, pk):
    customer = get_object_or_404(Customer.objects.prefetch_related('purchases__vehicle'), pk=pk)
    return render(request, 'sales/customer_detail.html', {'customer': customer, 'active_tab': 'customers'})

from .forms import VehicleForm, CustomerForm, SaleForm, UserForm, PaymentFormSet

@login_required
def create_sale(request):
    if request.method == 'POST':
        form = SaleForm(request.POST)
        formset = PaymentFormSet(request.POST)
        
        if form.is_valid() and formset.is_valid():
            with transaction.atomic():
                sale = form.save(commit=False)
                if not sale.salesperson_id: 
                    sale.salesperson = request.user 
                sale.save()
                
                # Save Formset
                formset.instance = sale
                formset.save()
                
                messages.success(request, 'Venda registrada com sucesso!')
                return redirect('dashboard')
    else:
        initial = {'salesperson': request.user}
        vehicle_id = request.GET.get('vehicle')
        if vehicle_id:
            initial['vehicle'] = vehicle_id
            # Try to pre-fill price
            try:
                v = Vehicle.objects.get(pk=vehicle_id)
                # Format for the mask input
                initial['sale_price'] = f"{v.price:.2f}".replace('.', ',')
            except Vehicle.DoesNotExist:
                pass
                
        form = SaleForm(initial=initial)
        formset = PaymentFormSet()
        
    return render(request, 'sales/sale_form.html', {
        'form': form, 
        'formset': formset,
        'title': 'Registrar Venda', 
        'active_tab': 'sales'
    })

@login_required
def edit_sale(request, pk):
    sale = get_object_or_404(Sale, pk=pk)
    old_vehicle = sale.vehicle 
    
    if request.method == 'POST':
        form = SaleForm(request.POST, instance=sale)
        formset = PaymentFormSet(request.POST, instance=sale)
        
        if form.is_valid() and formset.is_valid():
            with transaction.atomic():
                new_sale = form.save(commit=False)
                
                if new_sale.vehicle != old_vehicle:
                    old_vehicle.status = 'available'
                    old_vehicle.save()
                    
                new_sale.save()
                formset.save()
                
                messages.success(request, 'Venda atualizada com sucesso!')
                return redirect('sale_list')
    else:
        form = SaleForm(instance=sale)
        formset = PaymentFormSet(instance=sale)
    
    return render(request, 'sales/sale_form.html', {
        'form': form, 
        'formset': formset,
        'title': f'Editar Venda #{sale.id}', 
        'active_tab': 'sales'
    })

@login_required
@user_passes_test(is_manager_or_superuser)
def delete_sale(request, pk):
    sale = get_object_or_404(Sale, pk=pk)
    
    if request.method == 'POST':
        with transaction.atomic():
            # Revert vehicle status to available
            sale.vehicle.status = 'available'
            sale.vehicle.save()
            
            # We do NOT revert customer status automatically as they might have other purchases
            
            sale.delete()
            messages.success(request, 'Venda excluída e veículo retornado ao estoque.')
            return redirect('sale_list')
    
    return render(request, 'sales/confirm_delete.html', {
        'obj': sale, 
        'title': 'Excluir Venda'
    })

@login_required
@login_required
def sale_list(request):
    sales = Sale.objects.select_related('vehicle', 'customer', 'salesperson').all().order_by('-sale_date')
    users = User.objects.all()

    # Filtering
    search_query = request.GET.get('search', '')
    date_min = request.GET.get('date_min', '')
    date_max = request.GET.get('date_max', '')
    salesperson_id = request.GET.get('salesperson', '')

    if search_query:
        sales = sales.filter(
            Q(customer__first_name__icontains=search_query) | 
            Q(customer__last_name__icontains=search_query) |
            Q(vehicle__make__icontains=search_query) |
            Q(vehicle__model__icontains=search_query)
        )
    
    if date_min:
        sales = sales.filter(sale_date__gte=date_min)
    
    if date_max:
        sales = sales.filter(sale_date__lte=date_max)
        
    if salesperson_id:
        sales = sales.filter(salesperson_id=salesperson_id)

    # Get available months for export
    available_months = Sale.objects.dates('sale_date', 'month', order='DESC')

    paginator = Paginator(sales, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'sales': page_obj, 
        'active_tab': 'sales_history',
        'users': users,
        'available_months': available_months,
        'search_query': search_query,
        'date_min': date_min,
        'date_max': date_max,
        'selected_salesperson': int(salesperson_id) if salesperson_id else '',
        'can_delete': is_manager_or_superuser(request.user)
    }
    return render(request, 'sales/sale_list.html', context)

# --- User Management Views (Admin/Manager Only) ---

@login_required
@user_passes_test(is_manager_or_superuser)
def user_list(request):
    users = User.objects.prefetch_related('groups').all().order_by('username')
    return render(request, 'sales/user_list.html', {'users': users, 'active_tab': 'users'})

@login_required
@user_passes_test(is_manager_or_superuser)
def user_add(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Usuário criado com sucesso.')
            return redirect('user_list')
    else:
        form = UserForm()
    return render(request, 'sales/form.html', {'form': form, 'title': 'Adicionar Usuário', 'active_tab': 'users'})

@login_required
@user_passes_test(is_manager_or_superuser)
def user_edit(request, pk):
    user = get_object_or_404(User, pk=pk)
    
    # Proteção: Não permite editar superusuários (Admin)
    if user.is_superuser:
        messages.error(request, "O usuário administrador não pode ser editado pelo sistema por questões de segurança.")
        return redirect('user_list')
        
    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Usuário atualizado com sucesso.')
            return redirect('user_list')
    else:
        initial = {}
        if user.groups.exists():
            initial['group'] = user.groups.first()
        form = UserForm(instance=user, initial=initial)
    return render(request, 'sales/form.html', {'form': form, 'title': f'Editar {user.username}', 'active_tab': 'users'})



@login_required
@user_passes_test(is_superuser)
def user_delete(request, pk):
    user = get_object_or_404(User, pk=pk)
    
    if user.is_superuser:
        messages.error(request, "O usuário administrador (Superuser) não pode ser removido.")
        return redirect('user_list')
        
    if user == request.user:
        messages.error(request, "Você não pode deletar a si mesmo.")
        return redirect('user_list')
    
    if request.method == 'POST':
        try:
            user.delete()
            messages.success(request, 'Usuário removido.')
        except ProtectedError:
            messages.error(request, "Não é possível apagar este usuário pois existem registros (vendas/clientes) vinculados a ele. Transfira os registros antes de apagar.")
        return redirect('user_list')
    
    return render(request, 'sales/confirm_delete.html', {'obj': user, 'title': 'Deletar Usuário'})

@login_required
@user_passes_test(is_manager_or_superuser)
def customer_delete(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    if request.method == 'POST':
        try:
            customer.delete()
            messages.success(request, 'Cliente removido com sucesso.')
            return redirect('customer_list')
        except ProtectedError:
             messages.error(request, "Erro: Este cliente possui vendas registradas e não pode ser removido.")
             return redirect('customer_detail', pk=pk)
    
import xlsxwriter
from django.http import HttpResponse
from io import BytesIO

@login_required
def export_sales_report(request):
    export_type = request.GET.get('type', 'complete')
    # Get list of selected months (format: 'YYYY-MM')
    month_list = request.GET.getlist('month')
    
    # Filter Data
    sales_qs = Sale.objects.select_related('vehicle', 'customer', 'salesperson').prefetch_related('payments').all().order_by('-sale_date')
    
    selected_months_str = "Geral"
    is_single_month = False
    
    # Filter logic: If 'all' is not present and list is not empty, filter by selected months
    if month_list and 'all' not in month_list:
        from django.db.models import Q
        date_filters = Q()
        valid_months = []
        
        for m_str in month_list:
            try:
                year, month = map(int, m_str.split('-'))
                date_filters |= Q(sale_date__year=year, sale_date__month=month)
                valid_months.append(m_str)
            except ValueError:
                continue
                
        if date_filters:
            sales_qs = sales_qs.filter(date_filters)
            
            # Format filename string
            if len(valid_months) == 1:
                selected_months_str = valid_months[0]
                is_single_month = True
            else:
                selected_months_str = f"Multiplo_{len(valid_months)}Meses"

    # Create an in-memory output file for the new workbook.
    output = BytesIO()
    workbook = xlsxwriter.Workbook(output, {'in_memory': True})
    
    # --- Estilos Globais ---
    # Cores (Paleta Profissional)
    primary_color = '#1E3A8A'  # Azul Escuro
    secondary_color = '#F3F4F6' # Cinza Claro
    accent_color = '#10B981'   # Verde Sucesso
    text_color = '#111827'
    
    # Formatos
    fmt_title = workbook.add_format({
        'bold': True, 'font_size': 18, 'color': primary_color, 'align': 'left'
    })
    
    fmt_header = workbook.add_format({
        'bold': True,
        'font_color': 'white',
        'bg_color': primary_color,
        'align': 'center',
        'valign': 'vcenter',
        'border': 1,
        'font_size': 11
    })
    
    fmt_cell = workbook.add_format({
        'font_color': text_color,
        'align': 'left',
        'valign': 'vcenter',
        'border': 1,
        'font_size': 10
    })
    
    fmt_cell_center = workbook.add_format({
        'font_color': text_color,
        'align': 'center',
        'valign': 'vcenter',
        'border': 1,
        'font_size': 10
    })
    
    fmt_date = workbook.add_format({
        'num_format': 'dd/mm/yyyy',
        'font_color': text_color,
        'align': 'center',
        'valign': 'vcenter',
        'border': 1,
        'font_size': 10
    })
    
    fmt_money = workbook.add_format({
        'num_format': 'R$ #,##0.00',
        'font_color': text_color,
        'align': 'right',
        'valign': 'vcenter',
        'border': 1,
        'font_size': 10
    })

    fmt_money_bold = workbook.add_format({
        'num_format': 'R$ #,##0.00',
        'bold': True,
        'font_color': text_color,
        'align': 'right',
        'valign': 'vcenter',
        'border': 1,
        'font_size': 11,
        'bg_color': '#E5E7EB'
    })

    # --- PLANILHA DE DADOS (Comum aos dois tipos ou específica para simples) ---
    sheet_name = 'Vendas' if export_type == 'simple' else 'Detalhamento'
    ws_list = workbook.add_worksheet(sheet_name)
    
    # Branding
    ws_list.merge_range('A1:D1', 'PRESTIGE AUTO - Relatório de Vendas', fmt_title)
    ws_list.write('A2', f'Gerado em: {timezone.now().strftime("%d/%m/%Y %H:%M")}', fmt_cell)
    
    # Configurações de Tabela
    headers = ['ID', 'Data', 'Cliente', 'CPF/CNPJ', 'Veículo', 'Marca', 'Modelo', 'Ano', 'Placa/VIN', 'Vendedor', 'Forma(s) Pagto', 'Preço Venda', 'Status']
    start_row = 3
    
    for col, h in enumerate(headers):
        ws_list.write(start_row, col, h, fmt_header)
        
    for row, sale in enumerate(sales_qs, start_row + 1):
        # Process Payment Types
        payment_types = [p.get_payment_type_display() for p in sale.payments.all()]
        payment_str = ", ".join(set(payment_types)) if payment_types else "-"
        
        ws_list.write(row, 0, sale.id, fmt_cell_center)
        ws_list.write(row, 1, sale.sale_date, fmt_date)
        ws_list.write(row, 2, f"{sale.customer.first_name} {sale.customer.last_name}", fmt_cell)
        ws_list.write(row, 3, "N/A", fmt_cell)
        ws_list.write(row, 4, str(sale.vehicle), fmt_cell)
        ws_list.write(row, 5, sale.vehicle.make, fmt_cell)
        ws_list.write(row, 6, sale.vehicle.model, fmt_cell)
        ws_list.write(row, 7, sale.vehicle.year, fmt_cell_center)
        ws_list.write(row, 8, sale.vehicle.vin, fmt_cell)
        ws_list.write(row, 9, sale.salesperson.get_full_name() or sale.salesperson.username, fmt_cell)
        ws_list.write(row, 10, payment_str, fmt_cell)
        ws_list.write(row, 11, sale.sale_price, fmt_money)
        ws_list.write(row, 12, "Concluída", fmt_cell_center)
    
    # Total Row
    total_rev = sales_qs.aggregate(Sum('sale_price'))['sale_price__sum'] or 0
    end_row = start_row + len(sales_qs) + 1
    ws_list.write(end_row, 10, "TOTAL", fmt_header)
    ws_list.write(end_row, 11, total_rev, fmt_money_bold)

    # Layout Improvements
    # ws_list.autofilter(start_row, 0, end_row, len(headers)-1) # Removed as per user request
    ws_list.freeze_panes(start_row + 1, 0)
    
    # Column Widths
    widths = [6, 12, 25, 15, 25, 12, 12, 8, 18, 20, 20, 15, 12]
    for i, w in enumerate(widths):
        ws_list.set_column(i, i, w)


    if export_type == 'complete':
        # --- DASHBOARD SHEET ---
        ws_dash = workbook.add_worksheet('Visão Geral')
        ws_dash.hide_gridlines(2)
        ws_dash.set_tab_color(primary_color)
        ws_list.set_tab_color('#64748b')
        ws_dash.activate() # Make it the default tab

        subtitle_fmt = workbook.add_format({'font_size': 12, 'italic': True, 'color': '#6B7280'})
        
        ws_dash.write('B2', 'Relatório Executivo de Vendas', fmt_title)
        ws_dash.write('B3', f'Período: {selected_months_str}', subtitle_fmt)
        
        # KPIs
        count_sales = sales_qs.count()
        avg_ticket = total_rev / count_sales if count_sales > 0 else 0
        
        kpi_label_fmt = workbook.add_format({'font_size': 10, 'color': '#6B7280', 'align': 'center', 'border': 1, 'border_color': '#E5E7EB'})
        kpi_value_fmt = workbook.add_format({'font_size': 14, 'bold': True, 'color': text_color, 'align': 'center', 'border': 1, 'border_color': '#E5E7EB'})
        
        # Draw KPIs
        ws_dash.merge_range('B5:C5', 'Faturamento Total', kpi_label_fmt)
        ws_dash.merge_range('B6:C6', f'R$ {total_rev:,.2f}', kpi_value_fmt)
        
        ws_dash.merge_range('E5:F5', 'Qtd. Vendas', kpi_label_fmt)
        ws_dash.merge_range('E6:F6', count_sales, kpi_value_fmt)
        
        ws_dash.merge_range('H5:I5', 'Ticket Médio', kpi_label_fmt)
        ws_dash.merge_range('H6:I6', f'R$ {avg_ticket:,.2f}', kpi_value_fmt)
        
        # --- SMART CHART ---
        ws_data = workbook.add_worksheet('Data_Source')
        ws_data.hide()
        
        # Logic: If Single Month -> Daily View. If Multiple/All -> Monthly View.
        if is_single_month:
            from django.db.models.functions import TruncDay
            trunc_func = TruncDay('sale_date')
            date_format = '%d/%m'
            chart_xlabel = 'Dia'
            chart_title = f'Evolução Diária ({selected_months_str})'
        else:
            trunc_func = TruncMonth('sale_date')
            date_format = '%b/%Y'
            chart_xlabel = 'Mês'
            chart_title = 'Evolução Mensal (Faturamento)'

        timeline_data = sales_qs.annotate(period=trunc_func).values('period').annotate(total=Sum('sale_price')).order_by('period')
        
        ws_data.write('A1', 'Período')
        ws_data.write('B1', 'Valor')
        
        row_idx = 1
        for item in timeline_data:
            ws_data.write(row_idx, 0, item['period'].strftime(date_format))
            ws_data.write(row_idx, 1, float(item['total']))
            row_idx += 1
            
        # Create Chart
        chart = workbook.add_chart({'type': 'column'})
        chart.add_series({
            'name': 'Faturamento',
            'categories': ['Data_Source', 1, 0, max(1, row_idx-1), 0],
            'values':     ['Data_Source', 1, 1, max(1, row_idx-1), 1],
            'fill':       {'color': primary_color},
            # Improve accessibility
            'data_labels': {'value': False} 
        })
        
        chart.set_title({'name': chart_title})
        chart.set_x_axis({
            'name': chart_xlabel,
            'name_font': {'size': 10, 'bold': False},
        })
        # Currency Format on Axis
        chart.set_y_axis({
            'name': 'Faturamento (R$)',
            'num_format': 'R$ #,##0',
            'major_gridlines': {'visible': True, 'line': {'color': '#f1f5f9'}}
        })
        chart.set_legend({'position': 'none'})
        chart.set_size({'width': 800, 'height': 400})
        
        ws_dash.insert_chart('B9', chart)

    workbook.close()
    output.seek(0)
    
    filename = f"Relatorio_Vendas_{selected_months_str}.xlsx"
    response = HttpResponse(
        output,
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    return response

# --- Database Backup Logic ---

from django.core.management import call_command
import sys

from io import StringIO

@login_required
@user_passes_test(is_superuser)
def export_database(request):
    """Exports the database as a JSON file."""
    output = StringIO()
    # Using 'dumpdata' command
    # Exclude contenttypes and auth.permission to avoid conflicts on import if needed, 
    # but for full backup usually we want everything or specifically our app data.
    # Let's dump everything for simplicity of "clone" behavior.
    call_command('dumpdata', stdout=output, format='json', indent=2)
    
    response_content = output.getvalue()
    response = HttpResponse(response_content, content_type='application/json')
    response['Content-Disposition'] = f'attachment; filename="backup_db_{timezone.now().strftime("%Y-%m-%d_%H%M")}.json"'
    return response

@login_required
@user_passes_test(is_superuser)
def import_database(request):
    """Imports a JSON database backup."""
    if request.method == 'POST' and request.FILES.get('backup_file'):
        backup_file = request.FILES['backup_file']
        
        # Save temp file
        import tempfile
        with tempfile.NamedTemporaryFile(delete=False, suffix='.json') as tmp:
            for chunk in backup_file.chunks():
                tmp.write(chunk)
            tmp_path = tmp.name
            
        try:
            # Run loaddata
            call_command('loaddata', tmp_path)
            messages.success(request, "Banco de dados restaurado com sucesso!")
        except Exception as e:
            messages.error(request, f"Erro ao importar banco de dados: {str(e)}")
        finally:
            os.remove(tmp_path)
            
        return redirect('dashboard')
    
    return redirect('dashboard')
