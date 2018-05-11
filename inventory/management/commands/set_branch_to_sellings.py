from django.core.management.base import BaseCommand
from django.conf import settings
from inventory.models import Branch
from cart.models import Vente



class Command(BaseCommand):
    """
    The script copy the field 'prix_total' into field 'purchasing_price'
    """
    help = 'set branch "boutique" all sellings'


    def handle(self, *args, **options):
        boutique = Branch.objects.get(name='Boutique')
        count = 0
        print("Updating branch of all sales...")

        for v in Vente.objects.all():
            v.branch = boutique
            v.save()
            count += 1
        print("Updated branch of %s sales " % count)







