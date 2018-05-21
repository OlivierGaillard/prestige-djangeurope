from django.test import TestCase
from .models import Product, ProductCategory
from .forms import ProductCreateForm

class TestWorkshopForms(TestCase):

    def setUp(self):
        pass

    def test_product_category_create_form(self):
        data = {'name' : 'Wonderland'}
        form = ProductCreateForm(data=data)
        self.assertTrue(form.is_valid(), form.errors.as_data())
        form.save()
        self.assertEqual(1, Product.objects.count())

