from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.shortcuts import reverse
from datetime import date
from .models import Vente, Client as Aclient, Paiement
from .forms import VenteCreateForm, PaiementCreateForm
from inventory.models import Branch




class TestCostsViews(TestCase):

    def setUp(self):
        User.objects.create_user(username='golivier', password='fleurdelys')
        self.atelier = Branch.objects.create(name='Atelier')
        self.maja = Aclient.objects.create(prenom='Maja', nom='Jamar')

    def test_form(self):
        data = {'montant' : 15000, 'branch': self.atelier.pk, 'date': date.today()}
        f = VenteCreateForm(data=data)
        self.assertTrue(f.is_valid(), f.errors.as_data())

    def test_create_one_selling(self):
        c = Client()
        c.post('/login/', {'username': 'golivier', 'password': 'fleurdelys'})
        c.post(reverse('cart:vente_create'), data = {'date': date.today(), 'montant' : 15000, 'branch': self.atelier.pk})
        c.logout()
        self.assertEqual(1, Vente.objects.count())

    def test_paymentCreate(self):
        vente = Vente.objects.create(montant=200)
        data = {'payment_amount' : 100, 'date' : date.today(), 'vente' : vente.pk}
        f = PaiementCreateForm(data=data)
        self.assertTrue(f.is_valid(), f.errors.as_data())

    def test_paymentCreate_initial(self):
        vente = Vente.objects.create(montant=200)
        initial_data = {'selling_amount': 40, 'date': '2018-04-01 9:45:00', 'vente' : vente.pk}
        new_data = {'payment_amount': 40, 'date': '2018-04-02 9:45:00', 'vente' : vente.pk }
        f = PaiementCreateForm(data=new_data, initial=initial_data)
        self.assertTrue(f.has_changed())
        self.assertTrue(f.is_valid(), f.errors.as_data())


    def test_add_payment_payments_not_finished(self):
        c = Client()
        c.post('/login/', {'username': 'golivier', 'password': 'fleurdelys'})
        c.post(reverse('cart:vente_create'), data={'date': date.today(), 'montant': 15000, 'branch': self.atelier.pk})
        vente = Vente.objects.all()[0]
        data = {'payment_amount' : 100, 'date' : date.today(), 'vente' : vente.pk}
        c.post(reverse('cart:paiement_add', args=[vente.pk]), data=data)
        self.assertEqual(1, Paiement.objects.count())
        self.assertFalse(vente.reglement_termine)

    def test_add_payment_payments_finished(self):
        c = Client()
        c.post('/login/', {'username': 'golivier', 'password': 'fleurdelys'})
        c.post(reverse('cart:vente_create'), data={'date': date.today(), 'montant': 15000, 'branch': self.atelier.pk})
        vente = Vente.objects.all()[0]
        data = {'payment_amount' : 15000, 'date' : date.today(), 'vente' : vente.pk}
        c.post(reverse('cart:paiement_add', args=[vente.pk]), data=data)
        self.assertEqual(1, Paiement.objects.count())
        vente = Vente.objects.all()[0] # new request is neeed to get updated values
        self.assertTrue(vente.reglement_termine)


    def test_add_payment_selling_price_greater_greater_than_defined(self):
        """
        When a product / article is sold to a price greater than the article's or
        product's (workshop) selling price, the balance should be zero too.
        :return:
        """
        c = Client()
        c.post('/login/', {'username': 'golivier', 'password': 'fleurdelys'})
        c.post(reverse('cart:vente_create'), data={'date': date.today(), 'montant': 15000, 'branch': self.atelier.pk})
        vente = Vente.objects.all()[0]
        data = {'payment_amount': 25000, 'date': date.today(), 'vente': vente.pk}
        c.post(reverse('cart:paiement_add', args=[vente.pk]), data=data)
        self.assertEqual(1, Paiement.objects.count())
        vente = Vente.objects.all()[0]
        self.assertTrue(vente.reglement_termine)
        self.assertEqual(25000, vente.montant)


    def test_list(self):
        c = Client()
        c.post('/login/', {'username': 'golivier', 'password': 'fleurdelys'})
        c.post(reverse('cart:vente_create'), data={'date': date.today(), 'montant': 15000, 'branch': self.atelier.pk})
        response = c.get(reverse('cart:ventes_workshop'))
        self.assertEqual(200, response.status_code)
