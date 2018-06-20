from django.test import TestCase, Client, RequestFactory
from django.contrib.auth.models import User
from django.shortcuts import reverse
from .models import Product, ProductCategory, Order
from cart.models import Client as CartClient, Vente
from inventory.models import Branch

class TestWorkshopViews(TestCase):

    def setUp(self):
        User.objects.create_user(username='golivier', password='gogol')


    def test_create_one_product(self):
        #pcat = ProductCategory.objects.create(name='retouches')
        c = Client()
        c.post('/login/', {'username': 'golivier', 'password': 'gogol'})
        c.post(reverse('workshop:product_create'), data={'name' : 'robe', 'selling_price' : 3444}) #, 'product_category' : pcat.pk})
        c.logout()
        self.assertEqual(1, Product.objects.count())

    def test_create_one_order(self):
        pcat = ProductCategory.objects.create(name='robe')
        prod = Product.objects.create(name='robe', selling_price=25000, product_category=pcat)
        client = CartClient.objects.create(prenom='Olivier', nom='Gaillard')
        c = Client()
        c.post('/login/', {'username': 'golivier', 'password': 'gogol'})
        data = {'client': client.pk, 'product': prod.pk, 'selling_price': 15430, 'order_state': Order.PENDING,
                'generate_selling' : 'NO'}
        c.post(reverse('workshop:order_create'), data=data)
        c.logout()
        self.assertEqual(1, Order.objects.count())

    def test_update_one_order(self):
        pcat = ProductCategory.objects.create(name='robe')
        prod = Product.objects.create(name='robe', selling_price=25000, product_category=pcat)
        client = CartClient.objects.create(prenom='Olivier', nom='Gaillard')
        c = Client()
        c.post('/login/', {'username': 'golivier', 'password': 'gogol'})
        data = {'client': client.pk, 'product': prod.pk, 'selling_price': 15430, 'order_state': Order.PENDING,
                'generate_selling': 'NO'}
        c.post(reverse('workshop:order_create'), data=data)
        self.assertEqual(1, Order.objects.count())
        # updating order state to "planned"
        updated_data = {'order_state' : Order.PLANNED, 'client': client.pk, 'product': prod.pk, 'generate_selling' : 'NO'}
        order = Order.objects.all()[0]
        c.post(reverse('workshop:order_update', args=[order.pk]), data=updated_data)
        updated_order = Order.objects.all()[0]
        self.assertEqual(Order.PLANNED, updated_order.order_state)
        c.logout()

    def test_generate_selling(self):
        """
        When an order has the state "tested" and the radio button "Generate selling" is selected, a new
        selling should be created and this order contains a foreign key to this selling.
        :return:
        """
        pcat = ProductCategory.objects.create(name='robe')
        prod = Product.objects.create(name='robe', selling_price=25000, product_category=pcat)
        client = CartClient.objects.create(prenom='Olivier', nom='Gaillard')
        c = Client()
        c.post('/login/', {'username': 'golivier', 'password': 'gogol'})
        data = {'client': client.pk, 'product': prod.pk, 'selling_price': 15430, 'order_state': Order.PENDING,
                'generate_selling': 'NO'}
        c.post(reverse('workshop:order_create'), data=data)
        self.assertEqual(1, Order.objects.count())
        # updating order state to "planned"
        updated_data = {'order_state': Order.TESTED, 'client': client.pk, 'product': prod.pk, 'generate_selling': 'YES'}
        order = Order.objects.all()[0]
        c.post(reverse('workshop:order_update', args=[order.pk]), data=updated_data)
        updated_order = Order.objects.all()[0]
        self.assertEqual(Order.TESTED, updated_order.order_state)
        self.assertEqual(1, Vente.objects.count())
        vente = Vente.objects.all()[0]
        branch = Branch.objects.all()[0]
        self.assertEqual(branch.name, vente.branch.name)
        c.logout()


