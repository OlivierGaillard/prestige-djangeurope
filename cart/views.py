from django.shortcuts import render, reverse, get_object_or_404
from django.contrib.auth.decorators import login_required
import datetime
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from crispy_forms.bootstrap import PrependedText
from crispy_forms.bootstrap import TabHolder, Tab, FormActions
from crispy_forms.layout import Submit, Layout, Fieldset, Field
from .models import CartItem, Vente, Client, Paiement
from .forms import VenteCreateForm, ClientCreateForm, PaiementCreateForm, VenteDeleteForm, VenteUpdateForm, ClientUpdateForm
from inventory.models import Article
from .cartutils import is_cart_id_session_set, _set_or_get_session_id, get_cart_items, get_cart_id_session
from .cartutils import  get_cart_item_of_book, article_already_in_cart, get_cart_counter, _remove_cart_item, cart_not_complete
from .cartutils import remove_cart_id_from_session
import logging

logger = logging.getLogger('django')



def add_cart_counter_to_context(request, ctx):
    ctx['cart_counter'] = get_cart_counter(request)
    return ctx

def add_cart_item(request, pk):
    if request.method == 'POST':
        article = Article.objects.get(pk=pk)
        cart_items = get_cart_items(request)
        if article_already_in_cart(cart_items, article):
            cart_item = get_cart_item_of_book(cart_items, article)
            cart_item.augment_quantity(1)
            cart_item.save()
        else:
            if article.quantity > 0:
                cart_item = CartItem()
                cart_item.cart_id = _set_or_get_session_id(request)
                cart_item.article = article
                cart_item.quantity = 1
                cart_item.save()
            else:
                return HttpResponse("Quantite en stock insuffisante!")
        url_redirect = reverse('cart:cart_content')
        return HttpResponseRedirect(url_redirect)
    else:
        print('not a POST?')
        pass

def remove_cart_item(request, pk):
    if request.method == 'POST':
        cart_items = get_cart_items(request)
        vente = cart_items[0].vente
        article = Article.objects.get(pk=pk)
        _remove_cart_item(request, article)
        url_redirect = reverse('cart:cart_content')
        return HttpResponseRedirect(url_redirect)
    else:
        raise ValueError('Should not be called with GET')


def remove_article_from_vente_and_update_article_quantity(request, pk):
    """pk is the one of cart_item, its ID."""
    if request.method == 'GET':
        cart_item = CartItem.objects.get(pk=pk)
        vente = cart_item.vente
        article = Article.objects.get(pk=cart_item.article.pk)
        article.quantity += cart_item.quantity
        article.save()
        cart_item.delete()
#        url_redirect = reverse('cart:vente_update', kwargs={'pk':vente.pk})
        return HttpResponseRedirect("/cart/vente_update/%s" % vente.pk)


def edit_price(request, pk):
    if request.method == 'POST':
        cart_item = CartItem.objects.get(pk=pk)
        price = request.POST.get('new_price', '')
        if len(price) == 0:
            # assuming zero
            price = "0"
        cart_item.prix = float(price)
        cart_item.save()
        if cart_item.prix == 0:
            return render(request, 'cart/cart_content.html',
                          {'error_message' : "Le montant de l'article est zéro!",
                           'cart' : get_cart_items(request), 'new_price' : price,
                           })
        cart_item.save()
        url_redirect = reverse('cart:cart_content')
        return HttpResponseRedirect(url_redirect)
    else:
        raise ValueError('cart:views:edit_price: should not be called with GET')

# This import must be defined here, after the functions definition and not before,
# otherwise it fails.


class CartView(ListView):
    """When the cart is validated the cart_items have the status
    'cart_complete' = True. It is better to remove the 'session_id'
    from the request?
    """
    model = CartItem
    template_name = 'cart/cart_content.html'
    context_object_name = 'cart'

    def get_queryset(self):
        if is_cart_id_session_set(self.request):
            qs = CartItem.objects.filter(cart_id = get_cart_id_session(self.request))
            qs = qs.exclude(cart_complete=True)
            return qs #CartItem.objects.filter(cart_id = get_cart_id_session(self.request))
        else:
            return []

    def get_context_data(self, **kwargs):
        ctx = super(CartView, self).get_context_data(**kwargs)
        if  is_cart_id_session_set(self.request): # and not cart_not_complete(self.request):
            cart_id = get_cart_id_session(self.request)
            ctx['cart_total'] = CartItem.get_total_of_cart(cart_id)
            ctx['cart'] = get_cart_items(self.request)
            return ctx
        else:
            return ctx


class CheckoutView(CreateView):
    """Crée le formulaire de la vente avec la liste des articles mis dans le panier.
    Le montant est pré-renseigné. """
    model = Vente
    template_name = 'cart/checkout.html'
    context_object_name = 'cart'
    form_class = VenteCreateForm

    def get_context_data(self, **kwargs):
        ctx = super(CheckoutView, self).get_context_data(**kwargs)

        if is_cart_id_session_set(self.request):
            cart_id = get_cart_id_session(self.request)
            ctx['cart_total'] = CartItem.get_total_of_cart(cart_id)
            #ctx['vente_pk'] = CartItem.get_vente_id(cart_id)
            ctx['cart'] = get_cart_items(self.request)
            return ctx
        else:
            return ctx

    def get_initial(self):
        initial = super(CheckoutView, self).get_initial()
        session_id = get_cart_id_session(self.request)
        initial['montant'] = CartItem.get_total_of_cart(session_id)
        return  initial

    def form_valid(self, form):
        self.object = form.save()
        cart_items = get_cart_items(request=self.request)
        for cart in cart_items:
            cart.cart_complete = True
            cart.vente = self.object
            cart.save()
            cart.update_article_quantity()
        remove_cart_id_from_session(self.request)
        return super(CheckoutView, self).form_valid(form)


class VenteDetail(DetailView):
    model = Vente
    template_name = 'cart/vente.html'
    context_object_name = 'vente'

class VenteUpdateView(UpdateView):
    model = Vente
    template_name = 'cart/vente_update.html'
    context_object_name = 'vente'
    form_class = VenteUpdateForm

class VenteCreateView(CreateView):
    """
    Primary usage is for branch workshop. It is not used
    to enter a selling by using the cart process.

    A user of the workshop will select a product of the workshop
    and it to the cart, why not?

    """
    model = Vente
    template_name = 'cart/vente_create.html'
    context_object_name = 'vente'
    form_class = VenteCreateForm
    success_url = 'cart/ventes_workshop'



class VenteListView(ListView):
    model = Vente
    template_name = 'cart/ventes.html'
    context_object_name = 'ventes'

    def get_context_data(self, **kwargs):
        ctx = super(VenteListView, self).get_context_data(**kwargs)
        li = Vente.objects.all()
        total = 0
        for v in li:
            total += v.montant
        ctx['total'] = total
        return ctx

class VenteWorkshopListView(ListView):
    model = Vente
    template_name = 'cart/ventes_workshop.html'
    context_object_name = 'ventes'

    def get_context_data(self, **kwargs):
        ctx = super(VenteWorkshopListView, self).get_context_data(**kwargs)
        li = Vente.objects.filter(branch__name='Atelier')
        total = 0
        for v in li:
            total += v.montant
        ctx['total'] = total
        return ctx

    def get_queryset(self):
        qs = super(VenteWorkshopListView, self).get_queryset()
        qs = qs.filter(branch__name='Atelier')
        return qs


def vente_delete(request, pk):
    if request.method == "GET":
        vente = Vente.objects.get(pk=pk)
        vente.delete()
        return HttpResponseRedirect("/cart/ventes/")
    else:
        print('POST? strange')



class ClientListView(ListView):
    model = Client
    template_name = 'cart/clients.html'
    context_object_name = 'clients'

class ClientDetailView(DetailView):
    model = Client
    template_name = 'cart/client.html'
    context_object_name = 'client'

class ClientCreateView(CreateView):
    model = Client
    template_name = 'cart/client_create.html'
    form_class = ClientCreateForm


class ClientUpdateView(UpdateView):
    model = Client
    template_name = 'cart/client_update.html'
    form_class = ClientUpdateForm


class PaiementListView(ListView):
    model = Paiement
    template_name = 'cart/paiements.html'
    context_object_name = 'paiements'

class PaiementCreateView(CreateView):
    model = Paiement
    template_name = 'cart/paiement_create.html'
    form_class = PaiementCreateForm

login_required()
def add_paiement(request, vente_pk):
    """Add a paiement to a vente.
    return render(request, 'polls/detail.html', {'question': question})

    return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

    """
    logger.debug('In add_paiement')
    template_name = 'cart/paiement_add.html'
    vente = get_object_or_404(Vente, pk=vente_pk)
    logger.debug('Vente instance retrieved.')
    logger.debug('Amount of this "Vente": ', vente.montant)

    if request.method == 'POST':
        logger.debug('in POST')
        form = PaiementCreateForm(request.POST)
        logger.debug('before calling form.is_valid()')
        if form.is_valid():
            logger.debug('IS valid.')
            logger.debug('Setting the "Vente" instance to the payment...')
            montant = form.cleaned_data['payment_amount']
            p = Paiement.objects.create(payment_amount=montant, date=form.cleaned_data['date'], vente=vente)
            logger.debug('Payment-ID [%s] created.' % p.pk)
            logger.debug('Payment amount: [%s]' % p.payment_amount)
            vente.save() # the save method will update if the selling is finished or not
            # the save method will update the selling amount too.
            logger.debug('Vente: %s' % vente)
            url_redirect = reverse('cart:vente', args=[vente.pk])
            return HttpResponseRedirect(url_redirect)
        else:
            logger.debug('IS NOT valid.')
            logger.debug(form.errors.as_data())
            return render(request=request, template_name=template_name, context={'form': form,
                                                                             'solde': vente.solde_paiements()})
    else:
        logger.debug('in GET.')
        logger.debug('Vente ID: %s' % vente.pk)
        vente_solde = vente.solde_paiements()
        logger.debug('Solde: [%s}' % vente_solde)
        date_vente = datetime.datetime(year=vente.date.year, month=vente.date.month, day=vente.date.day,
                                       hour=vente.date.hour, minute=vente.date.minute)
        form = PaiementCreateForm(initial={'date' : date_vente, 'payment_amount' : vente_solde, 'vente' : vente})
        # add prepended text here
        #form.helper.layout.append(PrependedText('payment_amount', 'Max: ' + str(vente_solde)))
        return render(request=request, template_name=template_name, context={'form': form,
                                                                             'solde': vente_solde})


# def add_paiement(request, vente_pk):
#     """Add a paiement to a vente.
#     return render(request, 'polls/detail.html', {'question': question})
#
#     return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
#     """
#     logger.info('In add_paiement')
#     template_name = 'cart/paiement_add.html'
#     if request.method == 'POST':
#         logger.info('In add_paiement POST')
#         form = PaiementCreateForm(request.POST)
#         montant = float(request.POST.get('montant', ''))
#         vente = Vente.objects.get(pk=vente_pk)
#         form.helper.layout.append(PrependedText('montant', 'Max: ' + str(vente.solde_paiements())))
#         form.helper.layout.append(
#             FormActions(
#                 Submit('save', 'Submit'),
#             )
#         )
#
#
#         if form.is_valid():
#             form.save()
#             if vente.solde_paiements() == 0:
#                 vente.reglement_termine = True
#             else:
#                 vente.reglement_termine = False
#             vente.save()
#             url_redirect = reverse('cart:vente', args=[vente.pk])
#             return HttpResponseRedirect(url_redirect)
#         else:
#             return render(request=request, template_name=template_name, context={'form': form,
#                                                                              'solde': vente.solde_paiements()})
#     else:
#         # initial data = vente.pk
#         vente = Vente.objects.get(pk=vente_pk)
#         vente_solde = vente.solde_paiements()
#
#         date_vente = datetime.datetime(year=vente.date.year, month=vente.date.month, day=vente.date.day,
#                                        hour=vente.date.hour, minute=vente.date.minute)
#         form = PaiementCreateForm(initial={'vente': vente, 'date' : date_vente, 'montant' : vente_solde})
#         # add prepended text here
#         form.helper.layout.append(PrependedText('montant', 'Max: ' + str(vente_solde)))
#         form.helper.layout.append(
#             FormActions(
#                 Submit('save', 'Submit'),
#             )
#         )
#
#         return render(request=request, template_name=template_name, context={'form': form,
#                                                                              'solde': vente_solde})
#


class PaiementDetailView(DetailView):
    model = Paiement
    template_name = 'cart/paiement.html'
    context_object_name = 'paiement'



