from django.urls import reverse
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.test.utils import isolate_apps
from .forms import ArticleCreateForm
from .models import Article, Enterprise, Arrivage, Marque, Employee



# Create your tests here.
class TestInventory(TestCase):

    def setUp(self):

        self.enterprise = Enterprise.objects.create(name='Gogol')
        self.arrivage   = Arrivage.objects.create(nom='Sebastopol', date_arrivee="2017-12-12",
                                             proprietaire=self.enterprise)
        self.marque_Supra = Marque.objects.create(nom='Supra')
        self.user_oga = User.objects.create_user(username='golivier', password='mikacherie')
        self.employe = Employee.objects.create(user=self.user_oga, enterprise=self.enterprise)

        self.article1 = Article.objects.create(name='Article-1', marque=self.marque_Supra,
                                          entreprise=self.enterprise, quantity=5,
                                          arrivage=self.arrivage, selling_price=2000)


    #@isolate_apps('inventory')

    # def test_create_two_articles_with_same_name_but_two_branches(self):
    #     # test uniqueness too? One article could have the same name if it belongs to different branches.
    #     # todo: validate this business case with client
    #
    #     boutique = Branch.objects.create(name="Boutique")
    #     atelier  = Branch.objects.create(name="Atelier")
    #     a1 = Article.objects.create(branch=atelier, name='aa1', quantity=10, purchasing_price=20, photo='aa')
    #     a2 = Article.objects.create(branch=boutique, name='aa1', quantity=10, purchasing_price=20, photo='aaa' )
    #     self.assertIsNotNone(a2)


    def test_createForm(self):
        data = {'type_client': 'F',
                'genre_article' : 'V',
                'name': 'Test-1', 'marque': 'Babar',
                'marque' : self.marque_Supra.pk,
                'entreprise' : self.enterprise.pk,
                'quantity': 5,
                'arrivage': self.arrivage.pk,
                'selling_price' : 5000,
                'remise' : 5.0,
                }
        form = ArticleCreateForm(data)
        self.assertTrue(form.is_valid(), form.errors.as_data())

    def test_get_article1(self):
        article = Article.objects.get(pk=self.article1.pk)
        self.assertIsNotNone(article)

