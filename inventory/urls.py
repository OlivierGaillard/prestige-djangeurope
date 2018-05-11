"""myproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf.urls import url
from .views import ArticleCreateView, ArticleDetailView, upload_pic, articles, ArticleUpdateView, articleDeleteView
from .views import SoldesListView, SoldeUpdateView
from .views import BranchEditView, BranchDeleteView, BranchDetailView, BranchListView, BranchCreateView
from .views import CategoryDeleteView, CategoryUpdateView, CategoryDetailView, CategoryListView, CategoryCreateView
from .views import ArrivalListView, ArrivalUpdateView, ArrivalDetailView, ArrivalCreateView, ArrivalDeleteView
from .views import LossDetailView, LossesListView, LossUpdateView, LossDeleteView, add_one_loss
from .views import ArrivalDeleteView

app_name = 'inventory'


urlpatterns = [
    url('articles/', articles, name='articles'),
    url('soldes/', SoldesListView.as_view(), name='soldes'),
    url('article_create', ArticleCreateView.as_view(), name='article_create'),
    url(r'article_update/(?P<pk>[0-9]+)$', ArticleUpdateView.as_view(), name='article_update'),
    url(r'solde_update/(?P<pk>[0-9]+)$', SoldeUpdateView.as_view(), name='solde_update'),
    url(r'^article_detail/(?P<pk>[0-9]+)$', ArticleDetailView.as_view(), name='article_detail'),
    url(r'^upload_pic/(?P<pk>[0-9]+)$', upload_pic, name='upload_pic'),

    url(r'article_losses/(?P<pk>[0-9]+)$', add_one_loss, name='article_losses'),
    # url(r'add_one_loss/(?P<pk>[0-9]+)$', AddOneLossView.as_view(), name='add_one_loss'),
    url(r'^article_detail/(?P<pk>[0-9]+)$', ArticleDetailView.as_view(), name='article_detail'),
    url(r'^article_delete/(?P<pk>[0-9]+)$', articleDeleteView, name='article_delete'),

    url(r'^loss_delete/(?P<pk>[0-9]+)$', LossDeleteView.as_view(), name='loss_delete'),
    url(r'^loss_update/(?P<pk>[0-9]+)$', LossUpdateView.as_view(), name='loss_update'),
    url(r'^loss_detail/(?P<pk>[0-9]+)$', LossDetailView.as_view(), name='loss_detail'),
    url(r'^losses/$', LossesListView.as_view(), name='losses'),

    url(r'^arrival_create/$', ArrivalCreateView.as_view(), name='arrival_create'),
    url(r'^arrival_detail/(?P<pk>[0-9]+)$', ArrivalDetailView.as_view(), name='arrival_detail'),
    url(r'^arrival_update/(?P<pk>[0-9]+)$', ArrivalUpdateView.as_view(), name='arrival_update'),
    url(r'^arrival_delete/(?P<pk>[0-9]+)$', ArrivalDeleteView.as_view(), name='arrival_delete'),
    url(r'^arrivals/$', ArrivalListView.as_view(), name='arrivals'),

    url(r'^categories/$', CategoryListView.as_view(), name='categories'),
    url(r'^category_update/(?P<pk>[0-9]+)$', CategoryUpdateView.as_view(), name='category_update'),
    url(r'^category_create/$', CategoryCreateView.as_view(), name='category_create'),
    url(r'^category_detail/(?P<pk>[0-9]+)$', CategoryDetailView.as_view(), name='category_detail'),
    url(r'^category_delete/(?P<pk>[0-9]+)$', CategoryDeleteView.as_view(), name='category_delete'),

    url('branches/', BranchListView.as_view(), name='branches'),
    url('branch_create/$', BranchCreateView.as_view(), name='branch_create'),
    url('branch_detail/(?P<pk>[0-9]+)$', BranchDetailView.as_view(), name='branch_detail'),
    url('branch_delete/(?P<pk>[0-9]+)$', BranchDeleteView.as_view(), name='branch_delete'),
    url('branch_update/(?P<pk>[0-9]+)$', BranchEditView.as_view(), name='branch_update'),

]

