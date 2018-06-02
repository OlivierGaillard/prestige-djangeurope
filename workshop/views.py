from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, DetailView
# Create your views here.
from cart.models import Vente
from inventory.models import Branch
from .models import Product, ProductCategory, Order
from .forms import ProductCreateForm, ProductCategoryCreateForm, ProductUpdateForm, OrderCreateForm, OrderUpdateForm



class ProductCategoryCreateView(CreateView):
    model = ProductCategory
    template_name = 'workshop/product_category_create.html'
    success_url = reverse_lazy('workshop:product_categories')
    form_class = ProductCategoryCreateForm

class ProductDetailView(DetailView):
    model = Product
    template_name = 'workshop/product_detail.html'
    context_object_name = 'product'

class ProductCreateView(CreateView):
    model = Product
    template_name = 'workshop/product_create.html'
    success_url = reverse_lazy('workshop:products')
    form_class = ProductCreateForm

class ProductUpdateView(UpdateView):
    model = Product
    template_name = 'workshop/product_update.html'
    form_class = ProductUpdateForm
    success_url = reverse_lazy('workshop:products')

class ProductListView(ListView):
    model = Product
    template_name = 'workshop/products.html'
    context_object_name = 'products'

class ProductCategoryListView(ListView):
    model = ProductCategory
    template_name = 'workshop/product_categories.html'
    context_object_name = 'categories'


class OrderCreateView(CreateView):
    model = Order
    form_class = OrderCreateForm
    success_url = reverse_lazy('workshop:orders')
    template_name = 'workshop/order_create.html'

class OrderListView(ListView):
    model = Order
    template_name = 'workshop/orders.html'
    context_object_name = 'orders'

class OrderUpdateView(UpdateView):
    model = Order
    form_class = OrderUpdateForm
    success_url = reverse_lazy('workshop:orders')
    template_name = 'workshop/order_update.html'

    def form_valid(self, form):
        generate_selling = form.cleaned_data['generate_selling']
        if (generate_selling == 'YES' and self.object.selling == None):
            selling_price = self.object.product.selling_price
            branch_atelier = None
            if Branch.objects.filter(name='Atelier').count() == 0:
                branch_atelier = Branch.objects.create(name='Atelier')
            else:
                branch_atelier = Branch.objects.get(name='Atelier')

            vente = Vente.objects.create(branch=branch_atelier, montant=selling_price, client=self.object.client)
            self.object.selling = vente
        return super(OrderUpdateView, self).form_valid(form)
