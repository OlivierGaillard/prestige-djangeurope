from django.contrib import admin
from .models import Enterprise, Employee, Arrivage, Article, Marque, Photo

# class FraisAdmin(admin.ModelAdmin):
#     list_display = ['date', 'montant', 'objet', 'entreprise']
#
# admin.site.register(Frais, FraisAdmin)

class EnterpriseAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
admin.site.register(Enterprise, EnterpriseAdmin)

admin.site.register(Employee)
class ArrivageAdmin(admin.ModelAdmin):
    list_display = ['id', 'nom', 'proprietaire']
admin.site.register(Arrivage, ArrivageAdmin)

class ArticleAdmin(admin.ModelAdmin):
    list_display = ['id', 'entreprise', 'type_client', 'name', 'marque', 'quantity', 'type_taille', 'taille',
                    'solde', 'motifs', 'notes']

admin.site.register(Article, ArticleAdmin)
#admin.site.register(Photo)
class MarqueAdmin(admin.ModelAdmin):
    list_display = ['id', 'nom']
admin.site.register(Marque, MarqueAdmin)

class PhotoAdmin(admin.ModelAdmin):
    list_display = ['article', 'article_ID']
admin.site.register(Photo, PhotoAdmin)

