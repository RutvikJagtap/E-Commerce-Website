from django.shortcuts import render

# Create your views here.

# catalog/views.py
from django.shortcuts import render
from .models import Product, Category

def product_list(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    return render(request, 'catalog/product_list.html', {'products': products, 'categories': categories})
