from django.test import TestCase, Client, RequestFactory
from django.contrib.auth.models import User
from django.shortcuts import reverse
from .models import Product, ProductCategory

class TestWorkshopViews(TestCase):

    def setUp(self):
        User.objects.create_user(username='golivier', password='gogol')


    def test_create_one_product(self):
        #pcat = ProductCategory.objects.create(name='retouches')
        c = Client()
        c.post('/login/', {'username': 'golivier', 'password': 'gogol'})
        c.post(reverse('workshop:product_create'), data={'name' : 'robe'}) #, 'product_category' : pcat.pk})
        c.logout()
        self.assertEqual(1, Product.objects.count())
