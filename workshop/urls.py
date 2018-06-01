from django.conf.urls import url
from . import views


app_name = 'workshop'

urlpatterns = [
    url(r'^products/$', views.ProductListView.as_view(), name='products'),
    url(r'^product_create/$', views.ProductCreateView.as_view(), name='product_create'),
    url(r'^product_update/(?P<pk>[0-9]+)$', views.ProductUpdateView.as_view(), name='product_update'),
    url(r'^product_detail/(?P<pk>[0-9]+)$', views.ProductDetailView.as_view(), name='product_detail'),
    url(r'^product_categories/$', views.ProductCategoryListView.as_view(), name='product_categories'),
    url(r'^product_category_create/$', views.ProductCategoryCreateView.as_view(), name='product_category_create'),
    url(r'^sell_product/(?P<pk>[0-9]+)$', views.ProductUpdateView.as_view(), name='sell_product'),
    url(r'^order_create/$', views.OrderCreateView.as_view(), name='order_create'),
    url(r'^orders/$', views.OrderListView.as_view(), name='orders'),
    url(r'^order_update/(?P<pk>[0-9]+)$', views.OrderUpdateView.as_view(), name='order_update'),
    ]
