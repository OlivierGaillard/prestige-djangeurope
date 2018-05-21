from django.test import TestCase
from datetime import date
from .models import Product, ProductCategory

class TestWorkshopModels(TestCase):

    def test_createCategory(self):
        pcat = ProductCategory.objects.create(name='retouches')
        self.assertIsNotNone(pcat)

    def test_createProduct(self):
        p1 = Product.objects.create()
        self.assertIsNotNone(p1)
        self.assertEqual(date.today(), p1.order_date)
