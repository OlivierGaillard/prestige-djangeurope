from django.core.management.base import BaseCommand
from django.conf import settings
from inventory.models import Article, Branch



class Command(BaseCommand):
    """
    The script copy the field 'prix_total' into field 'purchasing_price'
    """
    help = 'set articles to branch boutique'


    def handle(self, *args, **options):
        boutique = Branch.objects.get(name='Boutique')
        count = 0
        articles_count = Article.objects.count()
        print("Updating branch of articles to boutique...")

        for a in Article.objects.all():
            a.branch = boutique
            a.save()
            count += 1
        print("Updated branch of %s articles..." % count)







