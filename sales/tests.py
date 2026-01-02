from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Vehicle, Customer, Sale
from decimal import Decimal

class SaleInventoryTests(TestCase):
    def setUp(self):
        # Create User
        self.user = User.objects.create_user(username='testuser', password='password')
        
        # Create Vehicle
        self.vehicle_a = Vehicle.objects.create(
            make='TestMake', model='ModelA', year=2020, price=50000, 
            vin='VIN001', mileage=1000, color='Black', status='available'
        )
        self.vehicle_b = Vehicle.objects.create(
            make='TestMake', model='ModelB', year=2021, price=60000, 
            vin='VIN002', mileage=2000, color='White', status='available'
        )
        
        # Create Customer
        self.customer = Customer.objects.create(
            first_name='John', last_name='Doe', email='john@example.com', 
            phone='1234567890', status='lead'
        )
        
        self.client = Client()
        self.client.login(username='testuser', password='password')

    def test_create_sale_marks_vehicle_sold(self):
        """Test creating a sale marks vehicle as sold"""
        self.assertEqual(self.vehicle_a.status, 'available')
        
        response = self.client.post(reverse('create_sale'), {
            'vehicle': self.vehicle_a.id,
            'customer': self.customer.id,
            'salesperson': self.user.id,
            'sale_price': 50000,
            'sale_date': '2023-01-01'
        })
        
        self.vehicle_a.refresh_from_db()
        self.assertEqual(self.vehicle_a.status, 'sold')

    def test_delete_sale_reverts_vehicle_status(self):
        """Test deleting a sale reverts vehicle to available"""
        # Create Sale
        sale = Sale.objects.create(
            vehicle=self.vehicle_a, customer=self.customer, 
            salesperson=self.user, sale_price=50000
        )
        self.vehicle_a.refresh_from_db()
        self.assertEqual(self.vehicle_a.status, 'sold')
        
        # Delete Sale
        response = self.client.post(reverse('delete_sale', args=[sale.id]))
        
        self.vehicle_a.refresh_from_db()
        self.assertEqual(self.vehicle_a.status, 'available')

    def test_edit_sale_swap_vehicle(self):
        """Test editing a sale to swap vehicle updates both vehicles"""
        # Sell Vehicle A
        sale = Sale.objects.create(
            vehicle=self.vehicle_a, customer=self.customer, 
            salesperson=self.user, sale_price=50000
        )
        
        # Edit to Sell Vehicle B instead
        response = self.client.post(reverse('edit_sale', args=[sale.id]), {
            'vehicle': self.vehicle_b.id,
            'customer': self.customer.id,
            'salesperson': self.user.id,
            'sale_price': 60000,
            'sale_date': '2023-01-01'
        })
        
        self.vehicle_a.refresh_from_db()
        self.vehicle_b.refresh_from_db()
        
        # A should be available again, B should be sold
        self.assertEqual(self.vehicle_a.status, 'available')
        self.assertEqual(self.vehicle_b.status, 'sold')
