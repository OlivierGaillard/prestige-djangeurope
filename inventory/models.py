from django.db import models
from django.shortcuts import reverse
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from dashboard.utils import TimeSliceHelper
from datetime import date

class Enterprise(models.Model):
    name = models.CharField(max_length=80)

    def __str__(self):
        return self.name


class Employee(models.Model):
    """
    Every user is an employee of one enterprise.

    The articles tables (derived from Product: Accessory, Clothes and Shoe)
     are bound to one enterprise with the help of the foreign key 'Product.product_owner'

    One user may work only with the articles belonging to his/her enterprise.

    The belonging of this user to the enterprise is expressed with the
    foreign key 'Employee.enterprise'.

    Conclusion: the employee has access permission only to the articles of her enterprise.

    Process to create one employee:

    a) create one user
    b) create one enterprise
    c) create one Employee with foreign keys to user and enterprise
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    enterprise = models.ForeignKey(Enterprise, related_name="employees")

    def get_enterprise_of_current_user(user):
        """
        A class helper method used by the abstract products.forms.ProductCreateForm.
        :param user: the request.user used to retrieve one Employee instance.
        :return: the Enterprise instance of the Employee instance.
        """
        if Employee.objects.filter(user=user).exists():
            employee = Employee.objects.get(user=user)
            return employee.enterprise

    def is_current_user_employee(user):
        if Employee.objects.filter(user=user).exists():
            employee = Employee.objects.get(user=user)
            return employee.enterprise != None
        else:
            return False


    def __str__(self):
        if self.enterprise is not None:
            return self.user.username + ': ' + str(self.enterprise)
        else:
            return self.user.username


class Arrivage(models.Model):
    nom = models.CharField(_("Name"), max_length=50, unique=True)
    date_arrivee = models.DateField(_("Arrival Date"))
    proprietaire = models.ForeignKey(Enterprise, null=True)

    def __str__(self):
        return self.nom

    def get_absolute_url(self):
        return reverse('inventory:arrival_detail', kwargs={'pk': self.pk})



class Branch(models.Model):
    """One enterprise can have multiple branches.
    For sample one shop and one production unit.
    """
    name = models.CharField(_('Name'), max_length=100, unique=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('inventory:branch_detail', kwargs={'pk' : self.pk})

    class Meta:
        ordering = ['name']
        verbose_name = _('Branch')



class Marque(models.Model):
    nom = models.CharField(_('Brand Name'), max_length=80, unique=True)

    def __str__(self):
        return self.nom

    class Meta:
        ordering = ['nom']




class Category(models.Model):
    name = models.CharField(_('Category'), max_length=100, unique=True)

    def get_absolute_url(self):
        return reverse('inventory:category_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.name


class ArticleManager(models.Manager):


    def total_purchasing_price(self, branch=None, year=None, start_date=None, end_date=None):
        total = 0
        helper = TimeSliceHelper(Article)
        articles = helper.get_objects(year=year, branch=branch, start_date=start_date, end_date=end_date)
        total = sum(a.purchasing_price for a in articles)
        return total

    def total_losses(self, branch=None, year=None, start_date=None, end_date=None):
        """Return how much money was lost because broken articles or other cause."""
        helper = TimeSliceHelper(Article)
        articles = helper.get_objects(year=year, branch=branch, start_date=start_date, end_date=end_date)
        total = sum(a.get_amount_losses for a in articles)
        return total



class Article(models.Model):
    clients_choices = (
        ('H', _('Homme')),
        ('F', _('Femme')),
        ('M', _('Mixte')),
        ('E', _('Enfant')),
    )
    genre_choices = (
        ('A', 'Accessoire'),
        ('V', 'Vêtement'),
        ('C', 'Chaussure'),
        ('S', 'Sous-vêtement'),
    )

    tailles_choices = (
        ('1', 'S'),
        ('2', 'M'),
        ('3', 'L'),
        ('4', 'XL'),
        ('5', 'XXL'),
        ('6', 'XXXL'),
        ('7', 'XXXXL'),
        ('8', '5XL'),
        ('9', '6XL'),
        ('10', '7XL'),
        ('11', '8XL'),
    )
    solde_choices = (
        ('N', _('-')),
        ('S', _('en solde')),
    )
    type_taille = (
        ('1', 'EUR'),
        ('2', 'US'),
        ('3', 'UK')
    )

    ######################

    # zulma
    # photo = models.ImageField(upload_to='articles', null=True, blank=True, unique=True)
    # purchasing_price = models.DecimalField(_('Purchasing price'), max_digits=10, decimal_places=2, null=True, blank=True,
    #                                        default=0)
    name  = models.CharField(_('Name'), max_length=100, null=True, blank=True, default=_('n.d.'))
    # description = models.TextField(_('Description'), null=True, blank=True, default=_('n.d.'))
    # date_added  = models.DateField(default=date.today, null=True)
    # # initial quantity when article is added to the inventory
    # initial_quantity = models.IntegerField(_('Initial quantity'), default=1, null=True)
    quantity = models.PositiveSmallIntegerField(_('Quantity'), default=1)
    #arrival = models.ForeignKey(Arrivage, null=True, on_delete=models.SET_NULL)
    # notes = models.TextField(_("Notes"), null=True, blank=True, default=_('n.d.'))
    #




    ######################

    objects = ArticleManager()

    branch = models.ForeignKey(Branch, null=True, blank=True, on_delete=models.SET_NULL)
    category = models.ForeignKey(Category, null=True, blank=True, verbose_name=_('Category'))
    type_client = models.CharField(_("Client Type"), max_length=1, choices=clients_choices, default='F', )
    genre_article = models.CharField(_("Article Type"), max_length=1, choices=genre_choices, default='S')
    nom = models.CharField(_('Name'), max_length=100, default="ensemble")
    marque = models.ForeignKey(Marque)
    entreprise = models.ForeignKey(Enterprise)
    quantite   = models.IntegerField(default=1)
    prix_unitaire = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    # new name
    purchasing_price = models.DecimalField(_('Purchasing price'), max_digits=10, decimal_places=2, null=True,
                                            blank=True, default=0)

    prix_total    = models.DecimalField(max_digits=10, decimal_places=2, default=0.0, help_text=_("Purchasing Price"))
    selling_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0, help_text=_("Selling Price"))
    remise     = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, default=0.0)
    date_ajout = models.DateField(default=date.today, null=True)
    arrivage   = models.ForeignKey(Arrivage, null=True, blank=True, default=3, verbose_name=_('Arrival'))
    couleurs_quantites = models.CharField(max_length=200, null=True, blank=True)
    motifs = models.CharField(max_length=200, null=True, blank=True)
    notes  = models.CharField(max_length=200, null=True, blank=True)
    type_taille = models.CharField(max_length=1, choices=type_taille, default='1', null=True, blank=True)
    taille = models.CharField(max_length=2, choices=tailles_choices, null=True, blank=True)
    taille_nombre = models.PositiveSmallIntegerField(null=True, blank=True)
    local = models.CharField(max_length=20, default='bas')
    solde = models.CharField(_("soldé"), max_length=1, choices=solde_choices, default='N')
    ventes = models.CharField(max_length=200, null=True, blank=True, help_text="25000, 35000")
    tailles_vendues = models.CharField(max_length=200, null=True, blank=True, help_text="(XL, 1), (M, 2)")

    def __str__(self):
        return self.nom + ' ID ' + str(self.pk)

    class Meta:
        ordering = ['pk',]

    def get_absolute_url(self):
        return reverse('inventory:article_detail', kwargs={'pk' : self.pk})



class Photo(models.Model):
    photo = models.ImageField(upload_to='articles', null=True, blank=True)
    article = models.ForeignKey(Article)

    def __str__(self):
        msg = "Photo de l'article %s" % self.article.nom + ' ID: ' + str(self.article.pk)
        return msg

    @property
    def article_ID(self):
        return str(self.article.id)

class LossesManager(models.Manager):

    def total_costs(self, branch=None, year=None, start_date=None, end_date=None):
        """Return how much money was lost because broken articles or other cause."""
        helper = TimeSliceHelper(Losses)
        losses = helper.get_objects(branch=branch, year=year, start_date=start_date, end_date=end_date)
        total = sum(a.amount_losses for a in losses)
        return total

    def total_quantity(self, branch=None, year=None, start_date=None, end_date=None):
        helper = TimeSliceHelper(Losses)
        losses = helper.get_objects(branch=branch, year=year, start_date=start_date, end_date=end_date)
        total = sum(a.losses for a in losses)
        return total

    def total_losses_for_article(self, article):
        """
        :param article:
        :return: total of money lost in losses for this article
        """
        qs = Losses.objects.filter(article=article)
        total = sum(a.amount_losses for a in qs)
        return total

    def total_losses_quantity_for_article(self, article):
        """

        :param article:
        :return: total quantity of losses for this article
        """
        qs = Losses.objects.filter(article=article)
        total = sum(a.losses for a in qs)
        return total



class Losses(models.Model):
    """Losses of one article because article was broken, stolen or other cause, event not sold.
    More: it can be losses not related to articles or even to a branch.
    """
    losses  = models.PositiveSmallIntegerField(_('Losses'), default=0)
    amount_losses = models.DecimalField(_('Money lost'), max_digits=10, decimal_places=2, null=True, blank=True,
                                           default=0)
    date = models.DateField(default=date.today, null=True, blank=True)
    article = models.ForeignKey(Article, on_delete=models.SET_NULL, null=True, related_name='Pertes')
    loss_type    = models.CharField(_("Type of loss"), max_length=100, help_text=_("Cause of the loss: not sold, broken, etc."),
                                    null=True, blank=True)

    branch = models.ForeignKey(Branch, null=True, blank=True, on_delete=models.SET_NULL)
    note = models.TextField(_('Note'), blank=True, null=True)
    objects = LossesManager()

    def delete(self):
        if self.article:
            self.article.quantity += self.losses
            self.article.save()
        super(Losses, self).delete()

    class Meta:
        ordering = ['-date']


