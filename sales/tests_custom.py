from django.test import TestCase, Client
from django.contrib.auth.models import User, Group
from django.urls import reverse

class UserManagementTests(TestCase):
    def setUp(self):
        # Create groups
        self.manager_group = Group.objects.create(name='Gerentes')
        self.sales_group = Group.objects.create(name='Vendedores')

        # Create Superuser
        self.superuser = User.objects.create_superuser('admin_test', 'admin@test.com', 'password123')
        
        # Create Manager
        self.manager = User.objects.create_user('manager_test', 'manager@test.com', 'password123')
        self.manager.groups.add(self.manager_group)
        
        # Create Regular User (Salesperson)
        self.target_user = User.objects.create_user('sales_test', 'sales@test.com', 'password123')
        self.target_user.groups.add(self.sales_group)

        self.client = Client()

    def test_superuser_can_edit_user(self):
        self.client.login(username='admin_test', password='password123')
        # Try to rename sales_test to sales_updated
        # Need to provide all fields required by UserForm
        response = self.client.post(reverse('user_edit', args=[self.target_user.pk]), {
            'username': 'sales_updated',
            'email': 'sales@test.com',
            'first_name': 'Sales',
            'last_name': 'Updated',
            'group': self.sales_group.pk,
            'password': '' # Leave empty
        })
        
        # Check for redirect (success)
        if response.status_code != 302:
            print(f"Edit Form Errors: {response.context['form'].errors if 'form' in response.context else 'No form in context'}")
        
        self.assertEqual(response.status_code, 302)
        
        # Verify db
        self.target_user.refresh_from_db()
        self.assertEqual(self.target_user.username, 'sales_updated')
        self.assertEqual(self.target_user.first_name, 'Sales')

    def test_manager_cannot_delete_user(self):
        self.client.login(username='manager_test', password='password123')
        # Try to delete target_user
        response = self.client.get(reverse('user_delete', args=[self.target_user.pk]))
        
        # Should redirect to login (because user_passes_test fails and redirects to LOGIN_URL)
        self.assertEqual(response.status_code, 302)
        self.assertIn('/accounts/login/', response.url)

    def test_superuser_can_delete_user(self):
        self.client.login(username='admin_test', password='password123')
        # Try to delete target_user (GET first for confirmation page)
        response = self.client.get(reverse('user_delete', args=[self.target_user.pk]))
        self.assertEqual(response.status_code, 200)
        
        # POST to delete
        response = self.client.post(reverse('user_delete', args=[self.target_user.pk]))
        self.assertEqual(response.status_code, 302)
        
        # Verify db
        self.assertFalse(User.objects.filter(pk=self.target_user.pk).exists())

