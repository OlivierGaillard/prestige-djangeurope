from django.test import TestCase
from datetime import date
from .models import Product, ProductCategory, Order
from inventory.models import Branch
from cart.models import Vente, Client as CartClient

class TestWorkshopModels(TestCase):

    def test_createCategory(self):
        pcat = ProductCategory.objects.create(name='retouches')
        self.assertIsNotNone(pcat)

    def test_createProduct(self):
        p1 = Product.objects.create(name='ensemble')
        self.assertIsNotNone(p1)
        self.assertEqual('ensemble', p1.name)

    def test_makeSelling(self):
        """
        To implement the selling of a workshop's product I need:
        1) the product
        2) a view which create the selling and set the foreign key 'selling' of the product.

        Normal use case: a selling of one product. Possible use case: more than one product are
        included in one selling. In this case when use click on the selling button the pending
        sellings are displayed.
        :return:
        """
        p1 = Product.objects.create()
        b  = Branch.objects.create(name='Atelier')
        client = CartClient.objects.create(nom='Gaillard', prenom='Olivier')
        order = Order.objects.create(product=p1, client=client)
        v1 = Vente.objects.create(branch=b, montant=2000)
        order.selling = v1
        order.save()
        self.assertEqual(order.selling.pk, v1.pk)

