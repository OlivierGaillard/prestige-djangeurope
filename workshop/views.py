from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView
# Create your views here.
from .models import Product, ProductCategory
from .forms import ProductCreateForm, ProductCategoryCreateForm, ProductUpdateForm



class ProductCategoryCreateView(CreateView):
    model = ProductCategory
    template_name = 'workshop/product_category_create.html'
    success_url = reverse_lazy('workshop:product_categories')
    form_class = ProductCategoryCreateForm


class ProductCreateView(CreateView):
    model = Product
    template_name = 'workshop/product_create.html'
    success_url = reverse_lazy('workshop:products')
    form_class = ProductCreateForm

class ProductUpdateView(UpdateView):
    model = Product
    template_name = 'workshop/product_create.html'
    form_class = ProductUpdateForm
    success_url = reverse_lazy('workshop:products')
    #def get_success_url(self):
        #return '/workshop/products/%s' % self.object.pk




class ProductListView(ListView):
    model = Product
    template_name = 'workshop/products.html'
    context_object_name = 'products'


class ProductCategoryListView(ListView):
    model = ProductCategory
    template_name = 'workshop/product_categories.html'
    context_object_name = 'categories'
