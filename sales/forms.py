from django import forms
from decimal import Decimal
from django.contrib.auth.models import User, Group
from .models import Vehicle, Customer, Sale, Payment

class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = ['make', 'model', 'year', 'price', 'vin', 'license_plate', 'mileage', 'color', 'image', 'image_url', 'description', 'status']

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['first_name', 'last_name', 'email', 'phone', 'address', 'status', 'assigned_to']

from django.forms import inlineformset_factory

class SaleForm(forms.ModelForm):
    sale_price = forms.CharField(label="Preço de Venda", widget=forms.TextInput(attrs={'class': 'money-mask', 'placeholder': 'R$ 0,00'}))

    class Meta:
        model = Sale
        fields = ['vehicle', 'customer', 'salesperson', 'sale_price', 'sale_date', 'notes']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Default: only available vehicles
        qs = Vehicle.objects.filter(status='available')
        
        # If editing an existing sale, include the current vehicle so it shows up
        if self.instance and self.instance.pk:
            current_vehicle_qs = Vehicle.objects.filter(pk=self.instance.vehicle.pk)
            qs = (qs | current_vehicle_qs).distinct()
            
            # Format initial price if exists
            if self.initial.get('sale_price'):
                self.initial['sale_price'] = f"{self.initial['sale_price']:.2f}".replace('.', ',')
            
        self.fields['vehicle'].queryset = qs

    def clean_sale_price(self):
        price = self.cleaned_data['sale_price']
        if isinstance(price, str):
            # Remove thousand separators (.) and replace decimal separator (,) with (.)
            try:
                clean_price = price.replace('.', '').replace(',', '.')
                return Decimal(clean_price)
            except (ValueError, ArithmeticError):
                raise forms.ValidationError("Valor inválido.")
        return price

class PaymentForm(forms.ModelForm):
    amount = forms.CharField(label="Valor", widget=forms.TextInput(attrs={'class': 'money-mask', 'placeholder': 'R$ 0,00'}))

    class Meta:
        model = Payment
        fields = ['payment_type', 'is_down_payment', 'amount', 'payment_date', 'installments', 'bank', 'quota', 'administrator', 'status']
        widgets = {
            'payment_date': forms.DateInput(attrs={'type': 'date'}),
            'is_down_payment': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
        }
    
    def clean_amount(self):
        amount = self.cleaned_data['amount']
        if isinstance(amount, str):
            try:
                clean_amount = amount.replace('.', '').replace(',', '.')
                return Decimal(clean_amount)
            except (ValueError, ArithmeticError):
                raise forms.ValidationError("Valor inválido.")
        return amount

# Formset for Payments
PaymentFormSet = inlineformset_factory(
    Sale, Payment, form=PaymentForm,
    extra=1, can_delete=True
)

# Admin Forms
class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="Senha", required=False, help_text="Deixe em branco para manter a senha atual.")
    group = forms.ModelChoiceField(queryset=Group.objects.all(), label="Função/Cargo", required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']
        labels = {
            'username': 'Usuário',
            'first_name': 'Nome',
            'last_name': 'Sobrenome',
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get('password')
        if password:
            user.set_password(password)
        if commit:
            user.save()
            # Update Group
            user.groups.clear()
            user.groups.add(self.cleaned_data.get('group'))
        return user
