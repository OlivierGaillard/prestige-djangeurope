from django.contrib import admin
from .models import Vente, CartItem, Client, Paiement


class CartItemAdmin(admin.ModelAdmin):
    list_display = ['date_added', 'vente', 'cart_complete']
admin.site.register(CartItem, CartItemAdmin)

class VenteAdmin(admin.ModelAdmin):
    list_display = ['pk', 'date', 'montant', 'client', 'reglement_termine']

admin.site.register(Vente, VenteAdmin)

class ClientAdmin(admin.ModelAdmin):
    list_display = ['nom', 'prenom', 'tel']

admin.site.register(Client, ClientAdmin)

class PaiementAdmin(admin.ModelAdmin):
    list_display = ['date', 'payment_amount', 'vente']

admin.site.register(Paiement, PaiementAdmin)
