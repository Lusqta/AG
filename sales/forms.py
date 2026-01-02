from django import forms
from django.contrib.auth.models import User, Group
from .models import Vehicle, Customer, Sale

class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = ['make', 'model', 'year', 'price', 'vin', 'mileage', 'color', 'image', 'image_url', 'description', 'status']

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['first_name', 'last_name', 'email', 'phone', 'address', 'status', 'assigned_to']

class SaleForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields = ['vehicle', 'customer', 'salesperson', 'sale_price', 'sale_date', 'notes']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['vehicle'].queryset = Vehicle.objects.filter(status='available')

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
