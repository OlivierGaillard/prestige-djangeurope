from django.test import TestCase
from cart.models import Client
from .models import Product, ProductCategory, Order
from .forms import ProductCreateForm, OrderCreateForm, OrderUpdateForm

class TestWorkshopForms(TestCase):

    def setUp(self):
        pass

    def test_product_category_create_form(self):
        data = {'name' : 'Wonderland', 'selling_price' : 2000}
        form = ProductCreateForm(data=data)
        self.assertTrue(form.is_valid(), form.errors.as_data())
        form.save()
        self.assertEqual(1, Product.objects.count())

    def test_order_create_form(self):
        pcat = ProductCategory.objects.create(name='robe')
        prod = Product.objects.create(name='robe', selling_price=25000, product_category=pcat)
        client = Client.objects.create(prenom='Olivier', nom='Gaillard')
        data = {'client': client.pk, 'product': prod.pk, 'selling_price': 15430, 'order_state' : Order.PENDING,
                'generate_selling' : 'NO'}
        form = OrderCreateForm(data=data)
        self.assertTrue(form.is_valid(), form.errors.as_data())
        form.save()
        self.assertEqual(1, Order.objects.count())

    def test_order_update_form(self):
        pcat = ProductCategory.objects.create(name='robe')
        prod = Product.objects.create(name='robe', selling_price=25000, product_category=pcat)
        client = Client.objects.create(prenom='Olivier', nom='Gaillard')
        data = {'client': client.pk, 'product': prod.pk, 'selling_price': 15430, 'order_state' : Order.PENDING, 'generate_selling' : 'NO'}
        form = OrderCreateForm(data=data)
        self.assertTrue(form.is_valid(), form.errors.as_data())
        form.save()
        self.assertEqual(1, Order.objects.count())
        # update order state
        order = Order.objects.all()[0]
        data = {'order_state' : Order.PLANNED, 'client': client.pk, 'product': prod.pk, 'generate_selling' : 'NO'}
        form = OrderUpdateForm(data=data, instance=order)
        self.assertTrue(form.is_valid(), form.errors.as_data())
        form.save()
        order = Order.objects.all()[0]
        self.assertEqual(Order.PLANNED, order.order_state)

