from django.core.management.base import BaseCommand
from django.conf import settings
from inventory.models import Article



class Command(BaseCommand):
    """
    The script copy the field 'prix_total' into field 'purchasing_price'
    """
    help = 'update english fields of inventory Article'


    def handle(self, *args, **options):
        count = 0
        articles_count = Article.objects.count()
        print("Updating purchasing prices, names and quantity of %s articles..." % articles_count)
        for a in Article.objects.all():
            a.purchasing_price = a.prix_total
            a.quantity = a.quantite
            a.name = a.nom
            a.save()
            count += 1
        print("Updated purchasing prices, quantity and name of %s articles..." % count)







