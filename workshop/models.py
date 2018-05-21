from django.db import models
from django.utils.translation import ugettext_lazy as _
from cart.models import Vente, Client
from datetime import date

class ProductCategory(models.Model):
    name = models.CharField(_('Name'), max_length=100, null=True, blank=True, default=_('n.d.'), unique=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    states = (
        ('0', _('pending')),
        ('1', _('started')),
        ('2', _('working')),
        ('3', _('finished')),
    )
    deadline   = models.DateField(_('Deadline'),   null=True, blank=True)
    order_date = models.DateField(_('Date order'), null=True, blank=True, default=date.today)
    client     = models.ForeignKey(Client, null=True, blank=True)
    work_state = models.CharField(_('Work state'), max_length=1, choices=states, null=True, default='0', blank=True)
    start_date = models.DateField(_('Start date'),   null=True, blank=True)
    name = models.CharField(_('Name'), max_length=100, null=True, blank=True, default=_('n.d.'))
    product_category = models.ForeignKey(ProductCategory, on_delete=models.SET_NULL, verbose_name=_('Category'), null=True, blank=True)
    selling_price = models.DecimalField(_("Selling Price"), max_digits=10, decimal_places=2, default=0.0, blank=True)
    selling       = models.ForeignKey(Vente, on_delete=models.SET_NULL, verbose_name=_('Selling'), null=True, blank=True)
    note          = models.TextField(_("Notes"), null=True, blank=True, default=_('n.d.'))
    photo = models.ImageField(upload_to='products', null=True, blank=True)




