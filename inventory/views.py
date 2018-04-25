from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required, permission_required
#from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from django.urls import reverse
from django_filters import FilterSet, CharFilter, ChoiceFilter, NumberFilter
from django_filters.views import FilterView
from django.views.generic import ListView, TemplateView, CreateView, DetailView, UpdateView
from django.contrib.auth.models import User
from .models import Article, Employee, Photo
from .forms import  ArticleCreateForm, AddPhotoForm, ArticleUpdateForm
from cart.cartutils import article_already_in_cart, get_cart_items

class ArticleFilter(FilterSet):
    genre_choices = (
        ('A', _('Accessoire')),
        ('V', _('Vêtement')),
        ('C', _('Chaussure')),
        ('S', _('Sous-vêtement')),
    )

    clients_choices = (
        ('H', _('Homme')),
        ('F', _('Femme')),
        ('M', _('Mixte')),
        ('E', _('Enfant')),
    )

    solde_choices = (
        ('S', _('en solde')),
    )

    genre_article = ChoiceFilter(choices=genre_choices, label=_(u"Genre d'article"))
    type_client = ChoiceFilter(choices=clients_choices, label=_('type de client'))
    solde = ChoiceFilter(choices=solde_choices)
    quantite__gt = NumberFilter(name='quantite', lookup_expr='gt', label=_('quantité supérieure à'))
    # selling_price__gte = NumberFilter(name='selling_price', lookup_expr='gte',
    #                                  label=_('prix de vente plus grand ou égal'))


    class Meta:
        model = Article
        fields = {'marque__nom' : ['icontains'],
                  'nom': ['icontains'],
                  'id' : ['exact'],
                  'quantite' : ['exact'],
                  'selling_price' : ['exact'],
                  'prix_total' : ['exact']
                  }



@login_required()
def articles(request):
    enterprise_of_current_user = Employee.get_enterprise_of_current_user(request.user)
    qs = Article.objects.filter(entreprise=enterprise_of_current_user)
    get_query = request.GET.copy()
    if 'quantite__gt' not in get_query:
        get_query['quantite__gt'] = '0'


    article_filter = ArticleFilter(get_query,
                                   queryset=qs)
    context = {}
    # Extracting the filter parameters
    meta = request.META
    q = meta['QUERY_STRING']
    # the whole url is .e.g. "marque__nom__icontains=&nom__icontains=&id=&genre_article=&type_client=H&solde=S&page=2"
    if q.find('nom') > 0: # checking if a filter param exist?
        # it contains a filter
         try:
            idx = q.index('page')
            q = q[:idx-1] # removing the page part of the url:
            #print('filter part:', q)
            context['q'] = q
         except ValueError:
            #print('no page or page 1, setting the filter')
            context['q'] = q

    paginator = Paginator(article_filter.qs, 25)
    page = request.GET.get('page')
    start_index = 1
    try:
        articles = paginator.page(page)
        start_index = articles.start_index()
    except PageNotAnInteger:
        articles = paginator.page(1)
    except EmptyPage:
        articles = paginator.page(paginator.num_pages) # last page
        start_index = articles.start_index()
    context['articles'] = articles
    context['count'] = article_filter.qs.count()
    context['filter'] = article_filter
    context['start_index'] = start_index
    return render(request, 'inventory/articles.html', context)





@method_decorator(login_required, name='dispatch')
class ArticleDetailView(DetailView):
    context_object_name = 'article'
    template_name = 'inventory/article.html'
    model = Article
    fields = ['arrivage', 'nom', 'marque', ]

    def get_context_data(self, **kwargs):
        ctx = super(ArticleDetailView, self).get_context_data(**kwargs)
        #ctx = add_cart_counter_to_context(self.request, ctx)
        #ctx = add_total_books(ctx)
        cart_items = get_cart_items(self.request)
        ctx['article_in_cart'] = article_already_in_cart(cart_items, self.object)
        #return add_categories_to_context(ctx)
        return ctx

@method_decorator(login_required, name='dispatch')
class ArticleUpdateView(UpdateView):
    template_name = 'inventory/article_update.html'
    context_object_name = 'article'
    model = Article
    form_class = ArticleUpdateForm

    def get_success_url(self):
        return reverse('inventory:articles')


class SoldeUpdateView(ArticleUpdateView):

    def get_success_url(self):
        return reverse('inventory:soldes')




@method_decorator(login_required, name='dispatch')
class ArticlesListView(ListView):
    context_object_name = 'articles'
    template_name = 'inventory/articles.html'
    model = Article

    def get_queryset(self):
        enterprise_of_current_user = Employee.get_enterprise_of_current_user(self.request.user)
        qs = Article.objects.filter(entreprise=enterprise_of_current_user)
        return qs

@method_decorator(login_required, name='dispatch')
class SoldesListView(ListView):
    context_object_name = 'articles'
    template_name = 'inventory/soldes.html'
    model = Article

    def get_queryset(self):
        enterprise_of_current_user = Employee.get_enterprise_of_current_user(self.request.user)
        qs = Article.objects.filter(entreprise=enterprise_of_current_user)
        qs = qs.filter(solde='S')
        qs = qs.filter(prix_total=0.0)
        return qs

    def get_context_data(self, **kwargs):
        context = super(SoldesListView, self).get_context_data()
        articles = qs = self.get_queryset()
        summary = {}
        summary['count'] = len(Article.objects.filter(solde='S'))

        paginator = Paginator(articles, 25)
        page = self.request.GET.get('page')
        start_index = 1
        try:
            articles = paginator.page(page)
            start_index = articles.start_index()
        except PageNotAnInteger:
            articles = paginator.page(1)
        except EmptyPage:
            articles = paginator.page(paginator.num_pages)  # last page
            start_index = articles.start_index()
        context['articles'] = articles


        no_selling_prices = qs.filter(prix_total = 0.0)
        summary['selling_price_zero'] = no_selling_prices_count = len(no_selling_prices)
        summary['no_selling_price_percent'] = int((no_selling_prices_count / summary['count']) * 100)

        context['summary'] = summary
        context['start_index'] = start_index
        return context




@method_decorator(login_required, name='dispatch')
class ArticleCreateView(CreateView):
    model = Article
    template_name = "inventory/article_create.html"
    #success_url = "inventory/articles.html"
    form_class = ArticleCreateForm

    def form_valid(self, form):
        if form.is_valid():
            print('Form is valid')
            self.object = form.save()
            #return HttpResponseRedirect(self.success_url)
            return HttpResponseRedirect(self.get_success_url())
        else:

            print('Form is NOT valid')


    def get_success_url(self):
        return reverse('inventory:articles')

    # def form_valid(self, form):
    #     #self.object = form.save()
    #     print("inside form_valid")
    #     #self.object.update_marque_ref(form['marque'].value(), form['marque_ref'].value())
    #     return HttpResponseRedirect('inventory/articles.html')

    # Todo: filtrer les arrivages de l'utilisateur


    # def get_form_kwargs(self):
    #     kwargs = super(ArticleCreateView, self).get_form_kwargs()
    #     kwargs['user'] = self.request.user
    #     return kwargs


def upload_pic(request, pk):
    "pk is Article ID"
    if request.method == 'POST':
        form = AddPhotoForm(request.POST, request.FILES)
        if form.is_valid():
            article = Article.objects.get(pk=pk)
            photo = Photo()
            photo.photo = form.cleaned_data['image']
            photo.article = article
            photo.save()
            return HttpResponseRedirect("/inventory/article_detail/" + str(article.pk))
        else:
            article = Article.objects.get(pk=pk)
            return render(request, "inventory/photo_add.html", {'article': article, 'form': form})

    else:
        article = Article.objects.get(pk=pk)
        return render(request, "inventory/photo_add.html", {'article': article})

