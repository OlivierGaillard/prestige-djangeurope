from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse_lazy
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required, permission_required
#from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from django.urls import reverse
from django_filters import FilterSet, CharFilter, ChoiceFilter, NumberFilter
from django_filters.views import FilterView
from django.views.generic import ListView, TemplateView, CreateView, DetailView, UpdateView, DeleteView
from django.contrib.auth.models import User
from .models import Branch, Article, Employee, Photo, Category, Arrivage, Losses
from .forms import  ArticleCreateForm, AddPhotoForm, ArticleUpdateForm, BranchCreateForm, BranchUpdateForm
from .forms import CategoryFormDelete, CategoryFormUpdate, CategoryFormCreate
from .forms import ArrivalUpdateForm, ArrivalCreateForm
from cart.cartutils import article_already_in_cart, get_cart_items
import logging
from django.core.exceptions import ValidationError
from .forms import ArticleLossesForm
from .forms import ArticleLossesUpdateForm, ArticleDeleteForm
from costs.models import Category as CostsCategory, Costs


logger = logging.getLogger('django')

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

    genre_article = ChoiceFilter(choices=genre_choices, label=_(u"Article Type"))
    type_client = ChoiceFilter(choices=clients_choices, label=_('Client Type'))
    solde = ChoiceFilter(choices=solde_choices)
    quantite__gt = NumberFilter(name='quantite', lookup_expr='gt', label=_('quantity greater than'))
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


@login_required()
def articleDeleteView(request, pk):

    article = get_object_or_404(Article, pk=pk)
    if request.method == 'POST':
        form = ArticleDeleteForm(request.POST)
        if form.is_valid():
            if not form.cleaned_data['delete_purchasing_costs']:
                logger.debug('Deleting article without its purchasing price.')
                # The purchasing price of the article will be saved in a Costs.
                # Create a Cost with the purchasing price
                cat = None
                if len(Category.objects.filter(name='Purchasing Price')) == 0:
                    cat =  CostsCategory.objects.create(name='Purchasing Price')
                else:
                    cat = CostsCategory.objects.filter(name='Purchasing Price')[0]
                logger.debug('Costs Category {0} created or used.'.format(cat.name))
                cost = Costs.objects.create(category=cat,
                                     amount=article.purchasing_price,
                                     name='Generated when article was deleted',
                                            branch=article.branch,
                                      )
                logger.info('Purchasing price {0} saved in  Cost-ID {1}.'.format(article.purchasing_price, cost.pk))
            else:
                logger.info('Deleting article without saving its purchasing price.')

            article.delete()
            return HttpResponseRedirect(reverse('inventory:articles'))
        else:
            return render(request, context={'article': article, 'form': form},
                          template_name='inventory/article_delete.html')

    else:
        form = ArticleDeleteForm()
        return render(request, context={'article': article, 'form': form},
                      template_name='inventory/article_delete.html')



@method_decorator(login_required, name='dispatch')
class ArticleCreateView(CreateView):
    model = Article
    template_name = "inventory/article_create.html"
    #success_url = "inventory/articles.html"
    form_class = ArticleCreateForm

    def form_valid(self, form):
        if form.is_valid():
            self.object = form.save()
            return HttpResponseRedirect(self.get_success_url())
        else:
            pass

    def get_success_url(self):
        return reverse('inventory:articles')



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

@method_decorator(login_required, name='dispatch')
class BranchListView(ListView):
    model = Branch
    template_name = 'inventory/branches.html'
    context_object_name = 'branches'

@method_decorator(login_required, name='dispatch')
class BranchCreateView(CreateView):
    model = Branch
    template_name = 'inventory/branch_create.html'
    form_class = BranchCreateForm


@method_decorator(login_required, name='dispatch')
class BranchDetailView(DetailView):
    model = Branch
    template_name = 'inventory/branch_detail.html'
    context_object_name = 'branch'

@method_decorator(login_required, name='dispatch')
class BranchDeleteView(DeleteView):
    model = Branch
    template_name = 'inventory/branch_delete.html'
    success_url = 'inventory/branches'
    context_object_name = 'branch'

@method_decorator(login_required, name='dispatch')
class BranchEditView(UpdateView):
    model = Branch
    template_name = 'inventory/branch_update.html'
    context_object_name = 'branch'
    form_class = BranchUpdateForm

@method_decorator(login_required, name='dispatch')
class CategoryCreateView(CreateView):
    model = Category
    template_name = 'inventory/category_create.html'
    form_class = CategoryFormCreate
    context_object_name = 'category'

@method_decorator(login_required, name='dispatch')
class CategoryDetailView(DetailView):
    model = Category
    template_name = 'inventory/category_detail.html'
    context_object_name = 'category'

@method_decorator(login_required, name='dispatch')
class CategoryUpdateView(UpdateView):
    model = Category
    template_name = 'inventory/category_update.html'
    form_class = CategoryFormUpdate
    context_object_name = 'category'

@method_decorator(login_required, name='dispatch')
class CategoryListView(ListView):
    model = Category
    template_name = 'inventory/categories.html'
    context_object_name = 'categories'

@method_decorator(login_required, name='dispatch')
class CategoryDeleteView(DeleteView):
    model = Category
    template_name = 'inventory/category_delete.html'
    context_object_name = 'category'
    success_url = reverse_lazy('inventory:categories')


@method_decorator(login_required, name='dispatch')
class ArrivalCreateView(CreateView):
    model = Arrivage
    template_name = 'inventory/arrival_create.html'
    form_class = ArrivalCreateForm
    context_object_name = 'arrival'

@method_decorator(login_required, name='dispatch')
class ArrivalDetailView(DetailView):
    model = Arrivage
    template_name = 'inventory/arrival_detail.html'
    context_object_name = 'arrival'

@method_decorator(login_required, name='dispatch')
class ArrivalUpdateView(UpdateView):
    model = Arrivage
    template_name = 'inventory/arrival_update.html'
    context_object_name = 'arrival'
    form_class = ArrivalUpdateForm

@method_decorator(login_required, name='dispatch')
class ArrivalListView(ListView):
    model = Arrivage
    template_name = 'inventory/arrivals.html'
    context_object_name = 'arrivals'

@method_decorator(login_required, name='dispatch')
class ArrivalDeleteView(DeleteView):
    model = Arrivage
    template_name = 'inventory/arrival_delete.html'
    success_url = '/inventory/arrivals'
    context_object_name = 'arrival'

def quantities_of_article_and_form_are_valid(article, form):
    """Check if article quantity and losses in form are valid."""
    new_losses = form.cleaned_data['losses']
    if article.quantity > 0 and article.quantity >= new_losses and new_losses > 0:
        logger.debug("Previous losses of article: %s" % article.losses)
        logger.debug("Losses of form: %s" % form.cleaned_data['losses'])
        logger.debug("Article quantity >= new_losses: %s >= %s" % (article.quantity, new_losses))
        return True
    else:
        if article.quantity < new_losses:
            logger.debug("Article quantity < new losses. We add error msg: %s < %s" % (article.quantity, new_losses))
            error = ValidationError(_("Losses cannot exceed quantity.") )
            form.add_error(error=error, field='losses')
        return False

def update_article_stock_quantity(article, form):
    """Add losses to article losses and substract to quantity."""
    logger.debug("Updated stock quantity of article: %s" % article.quantity)
    article.quantity -= form.cleaned_data['losses']
    article.save()


def create_lost(article, form):
    loss = Losses.objects.create(article=article, amount_losses=form.cleaned_data['amount_losses'],
                                 losses=form.cleaned_data['losses'], branch=article.branch,
                                 )


@login_required()
def add_one_loss(request, pk):
    logger.warning("add_one_loss function.")
    article = get_object_or_404(Article, pk=pk)
    logger.debug("Article-ID [%s]. Losses: %s" % (article.pk, article.losses))
    if request.method == 'POST':
        form = ArticleLossesForm(request.POST)

        if form.is_valid():
            logger.debug('form is valid')
            logger.debug('checking if losses value is compatible with quantity of article...')

            if quantities_of_article_and_form_are_valid(article, form):
                logger.debug('Losses and article values seem OK.')
                update_article_stock_quantity(article, form)
                create_lost(article, form)
                return HttpResponseRedirect("/inventory/article_detail/%s" % article.pk)
            else:
                logger.warning('Losses and articles values seem NOT ok.')
        else:
            logger.warning('form is NOT valid for article-ID %s' % article.pk)
            logger.warning(form.errors.as_data())
    else: # GET
        form = ArticleLossesForm()

    return render(request, "inventory/losses_form.html", {'form' : form, 'article' : article })

@method_decorator(login_required, name='dispatch')
class LossesListView(ListView):
    model = Losses
    template_name = 'inventory/losses.html'
    context_object_name = 'losses'

    def get_context_data(self, q=None):
        ctx = super(LossesListView, self).get_context_data()
        ctx['total_money'] = Losses.objects.total_costs()
        ctx['total_quantity'] = Losses.objects.count()
        return ctx

@method_decorator(login_required, name='dispatch')
class LossDeleteView(DeleteView):
    model = Losses
    template_name = 'inventory/loss_delete.html'
    context_object_name = 'loss'
    success_url = reverse_lazy('inventory:losses')


@method_decorator(login_required, name='dispatch')
class LossUpdateView(UpdateView):
    model = Losses
    template_name = 'inventory/losses_update.html'
    context_object_name = 'loss'
    form_class = ArticleLossesUpdateForm
    success_url = reverse_lazy('inventory:losses')

@method_decorator(login_required, name='dispatch')
class LossDetailView(DetailView):
    model = Losses
    template_name = 'inventory/loss_detail.html'
    context_object_name = 'loss'

