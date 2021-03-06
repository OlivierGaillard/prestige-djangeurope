from django.test import TestCase
from .models import Enterprise, Category, Costs
from cart.models import Vente
from inventory.models import Article, Arrivage, Branch, Marque, Enterprise as EnterpriseOwner
from datetime import date, timedelta
from django.utils import timezone

class TestModels(TestCase):

    def setUp(self):
        self.e3 = Enterprise.objects.create(name='Zorro')
        self.e1 = Enterprise.objects.create(name='Cosas de Casa')
        self.e2 = Enterprise.objects.create(name='Métacohérence')

        self.c5 = Category.objects.create(name='zeta')
        self.c1 = Category.objects.create(name='entretien')
        self.c2 = Category.objects.create(name='salaires')
        self.c3 = Category.objects.create(name='location')
        self.c4 = Category.objects.create(name='électricité')

        self.marque_m = Marque.objects.create(nom='3M')
        self.enterpriseOwner = EnterpriseOwner.objects.create(name='OGAnoGAFA')
        self.arrivage_a = Arrivage.objects.create(nom='bigA', date_arrivee=date.today())



    def test_cost_one_can_be_created(self):
        cos1 = Costs.objects.create(category=self.c1, amount=100)
        self.assertIsNotNone(cos1)

    def test_cost_one_amount(self):
        cos1 = Costs.objects.create(category=self.c1, amount=100)
        self.assertEqual(100, cos1.amount)


    def test_cost_one_print(self):
        cos1 = Costs.objects.create(category=self.c1, amount=100)
        s = "Amount: % s / Category: % s / Date: % s " % (cos1.amount, cos1.category, cos1.creation_date)
        self.assertEqual(s, str(cos1))

    def test_enterprise_ordered(self):
        li = Enterprise.objects.all()
        self.assertEqual('Cosas de Casa', li[0].name)

    def test_categories_ordered(self):
        li = Category.objects.all()
        self.assertEqual('électricité', li[0].name)

    def test_cost_dates(self):
        billing_date = date(year=2018, month=3, day=16)
        cost1 = Costs.objects.create(category=self.c1, amount=100, billing_date=billing_date)
        self.assertEqual(billing_date, cost1.billing_date)

    def test_total_costs_for_no_costs(self):
        self.assertEqual(0, Costs.objects.total_costs())

    def test_total_costs_for_one_cost(self):
        c = Costs.objects.create(category=self.c1, amount=100)
        self.assertEqual(100, Costs.objects.total_costs())
        self.assertEqual(100, Costs.objects.total_costs(branch='MAIN'))

    def test_total_costs_for_one_cost_with_dates(self):
        today = date.today()
        yesterday = today - timedelta(days=2)
        c = Costs.objects.create(category=self.c1, amount=100, billing_date=today)
        c2 = Costs.objects.create(category=self.c1, amount=50, billing_date=yesterday)
        self.assertEqual(150, Costs.objects.total_costs())
        self.assertEqual(150, Costs.objects.total_costs(branch='MAIN'))
        self.assertEqual(50, Costs.objects.total_costs(branch='MAIN', end_date=yesterday))
        self.assertEqual(50, Costs.objects.total_costs(end_date=yesterday))
        b1 = Branch.objects.create(name='b1')
        c2 = Costs.objects.create(category=self.c1, amount=10, billing_date=yesterday, branch=b1)
        self.assertEqual(10, Costs.objects.total_costs(end_date=yesterday, branch=b1))
        self.assertEqual(60, Costs.objects.total_costs(end_date=yesterday))

    def test_total_costs_for_two_costs(self):
        Costs.objects.create(category=self.c1, amount=100)
        Costs.objects.create(category=self.c1, amount=100.50)
        self.assertEqual(200.5, Costs.objects.total_costs())

    def test_balance_without_purchases(self):
        v1 = Vente.objects.create(montant=10.50, reglement_termine=True)
        v2 = Vente.objects.create(montant=20.50, reglement_termine=True)

        Costs.objects.create(category=self.c1, amount=10)
        Costs.objects.create(category=self.c1, amount=5.50)
        # 31 - 15.50 = 15.5
        self.assertEqual(15.5, Costs.objects.get_balance())

    def test_balance_with_purchases(self):
        Article.objects.create(name='a', purchasing_price=10, marque=self.marque_m, entreprise=self.enterpriseOwner, arrivage=self.arrivage_a)
        Article.objects.create(name='b', purchasing_price=5.5, marque=self.marque_m, entreprise=self.enterpriseOwner, arrivage=self.arrivage_a)
        Vente.objects.create(montant=20.50, reglement_termine=True)
        Vente.objects.create(montant=20.50, reglement_termine=True)
        Costs.objects.create(category=self.c1, amount=10)
        Costs.objects.create(category=self.c1, amount=5.50)
        self.assertEqual(15.5, Article.objects.total_purchasing_price())
        self.assertEqual(15.5, Costs.objects.total_costs())
        self.assertEqual(41, Vente.objects.total_sellings())
        self.assertEqual(10.0, Costs.objects.get_balance())



    def test_grand_total_last_year(self):
        last_year = date.today()-timedelta(days=365)
        Article.objects.create(name='a', purchasing_price=10, date_ajout=last_year, marque=self.marque_m, entreprise=self.enterpriseOwner,
                               arrivage=self.arrivage_a)
        Costs.objects.create(category=self.c1, billing_date=last_year, amount=10)
        Article.objects.create(name='b', purchasing_price=10, date_ajout=date.today(), marque=self.marque_m, entreprise=self.enterpriseOwner,
                               arrivage=self.arrivage_a)
        self.assertEqual(20, Costs.objects.grand_total(year=last_year.year))
        self.assertEqual(10, Costs.objects.grand_total(year=date.today().year))


    def test_costs_date_interval(self):

        d1mars = date(year=2018, month=3, day=1)
        d31mars = date(year=2018, month=3, day=31)
        d15april = date(year=2018, month=4, day=15)
        arrival = Arrivage.objects.create(nom="test", date_arrivee=d1mars)
        # Out of range
        # If article is added the
        Article.objects.create(name='alast', arrivage=arrival, purchasing_price=200,
                               date_ajout=d1mars, marque=self.marque_m, entreprise=self.enterpriseOwner)

        # Then its purchasing cannot appear if the start date starts after the article was added,
        # because only the start period is taken into account.

        self.assertEqual(0, Article.objects.total_purchasing_price(start_date=d15april))




