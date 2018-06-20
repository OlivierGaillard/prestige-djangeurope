from django.db import models
from django.utils.translation import ugettext_lazy as _
from cart.models import Vente, Client
from datetime import date

class ProductCategory(models.Model):
    name = models.CharField(_('Name'), max_length=100, null=True, blank=True, default=_('n.d.'), unique=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(_('Name'), max_length=100, null=True, blank=True, default=_('n.d.'))
    product_category = models.ForeignKey(ProductCategory, on_delete=models.SET_NULL, verbose_name=_('Category'), null=True, blank=True)
    selling_price = models.DecimalField(_("Selling Price"), max_digits=10, decimal_places=2, default=0.0)
    note          = models.TextField(_("Notes"), null=True, blank=True, default=_('n.d.'))
    photo = models.ImageField(upload_to='products', null=True, blank=True)

    def __str__(self):
        return self.name

class Order(models.Model):
    """
    When client Martin orders 2 products, the table contains 2 entries with 2 distinct product-ID.
    It can be the case where the products have not equal delivery dates.
    """
    PENDING   = 'pending'
    PLANNED   = 'planned'
    WORKING   = 'working'
    FINISHED  = 'finished'
    TESTED    = 'tested'
    DELIVERED = 'delivered'
    STATES_CHOICES = (
        (PENDING,   _('pending')),
        (PLANNED,   _('planned')),
        (WORKING,   _('working')),
        (FINISHED,  _('finished')),
        (TESTED,    _('tested')),
        (DELIVERED, _('delivered')),
    )

    client      = models.ForeignKey(Client, null=True)
    product     = models.ForeignKey(Product)
    order_date  = models.DateField(_('Date order'), null=True, blank=True, default=date.today)
    deadline    = models.DateField(_('Deadline'),   null=True, blank=True, default=date.today)
    start_date  = models.DateField(_('Start date'), null=True, blank=True, default=date.today)
    order_state = models.CharField(_('Order state'), max_length=9, choices=STATES_CHOICES, default=PENDING)
    selling     = models.ForeignKey(Vente, on_delete=models.CASCADE, verbose_name=_('Selling'), null=True, blank=True)

    class Meta:
        ordering = ['deadline']






# class Work(models.Model):
#     states = (
#         ('0', _('pending')),
#         ('1', _('working')),
#         ('3', _('finished')),
#         ('4', _('tested')),
#         ('5', _('delivered')),
#     )
#
#     work_state = models.CharField(_('Work state'), max_length=1, choices=states, null=True, default='0', blank=True)
#     start_date = models.DateField(_('Work start date'),   null=True, blank=True)
#
