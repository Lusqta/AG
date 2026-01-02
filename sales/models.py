from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Customer(models.Model):
    STATUS_CHOICES = [
        ('lead', 'Lead (Potencial)'),
        ('contacted', 'Contatado'),
        ('interested', 'Interessado'),
        ('purchased', 'Comprou'),
        ('lost', 'Perdido'),
    ]

    first_name = models.CharField("Nome", max_length=50)
    last_name = models.CharField("Sobrenome", max_length=50)
    email = models.EmailField("E-mail", unique=True)
    phone = models.CharField("Telefone", max_length=20)
    address = models.TextField("Endereço", blank=True)
    status = models.CharField("Status", max_length=20, choices=STATUS_CHOICES, default='lead')
    created_at = models.DateTimeField("Criado em", auto_now_add=True)
    assigned_to = models.ForeignKey(User, verbose_name="Atribuído a", on_delete=models.SET_NULL, null=True, blank=True, related_name='customers')

    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Vehicle(models.Model):
    STATUS_CHOICES = [
        ('available', 'Disponível'),
        ('sold', 'Vendido'),
        ('maintenance', 'Em Manutenção'),
    ]

    make = models.CharField("Marca", max_length=50)
    model = models.CharField("Modelo", max_length=50)
    year = models.PositiveIntegerField("Ano")
    price = models.DecimalField("Preço", max_digits=10, decimal_places=2)
    vin = models.CharField("Chassi (VIN)", max_length=17, unique=True)
    mileage = models.PositiveIntegerField("Quilometragem")
    color = models.CharField("Cor", max_length=30)
    status = models.CharField("Status", max_length=20, choices=STATUS_CHOICES, default='available')
    image = models.ImageField("Imagem do Veículo", upload_to='vehicles/', blank=True, null=True)
    image_url = models.TextField("URL ou Base64 da Imagem", blank=True, help_text="Link para a imagem ou código Base64")
    description = models.TextField("Descrição", blank=True)
    created_at = models.DateTimeField("Adicionado em", auto_now_add=True)

    class Meta:
        verbose_name = "Veículo"
        verbose_name_plural = "Veículos"

    def __str__(self):
        return f"{self.year} {self.make} {self.model}"

class Sale(models.Model):
    vehicle = models.OneToOneField(Vehicle, verbose_name="Veículo", on_delete=models.PROTECT, related_name='sale')
    customer = models.ForeignKey(Customer, verbose_name="Cliente", on_delete=models.PROTECT, related_name='purchases')
    salesperson = models.ForeignKey(User, verbose_name="Vendedor", on_delete=models.PROTECT, related_name='sales')
    sale_price = models.DecimalField("Preço de Venda", max_digits=10, decimal_places=2)
    sale_date = models.DateField("Data da Venda", default=timezone.now)
    notes = models.TextField("Observações", blank=True)

    class Meta:
        verbose_name = "Venda"
        verbose_name_plural = "Vendas"

    def save(self, *args, **kwargs):
        from django.db import transaction
        with transaction.atomic():
            # Automatically mark vehicle as sold
            self.vehicle.status = 'sold'
            self.vehicle.save()
            # Update customer status
            self.customer.status = 'purchased'
            self.customer.save()
            super().save(*args, **kwargs)

    def __str__(self):
        return f"Venda de {self.vehicle} para {self.customer}"
