from django.contrib import admin

from .models import Vehicle, Customer, Sale, Payment

class PaymentInline(admin.TabularInline):
    model = Payment
    extra = 1
    classes = ('collapse',)
    fields = ('payment_type', 'amount', 'payment_date', 'status', 'bank', 'installments')

@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ('id', 'vehicle', 'customer', 'sale_price', 'sale_date')
    search_fields = ('customer__first_name', 'vehicle__model')
    inlines = [PaymentInline]

@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ('make', 'model', 'year', 'price', 'status')
    list_filter = ('status', 'make')

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'status')
    list_filter = ('status',)
