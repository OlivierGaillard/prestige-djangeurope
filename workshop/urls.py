from django.conf.urls import url
from . import views


app_name = 'workshop'

urlpatterns = [
    url(r'^products/$', views.ProductListView.as_view(), name='products'),
    url(r'^product_create/$', views.ProductCreateView.as_view(), name='product_create'),
    url(r'^product_update/(?P<pk>[0-9]+)$', views.ProductUpdateView.as_view(), name='product_update'),
    url(r'^product_categories/$', views.ProductCategoryListView.as_view(), name='product_categories'),
    url(r'^product_category_create/$', views.ProductCategoryCreateView.as_view(), name='product_category_create'),
    ]
