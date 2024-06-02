from django.shortcuts import render
from .services import products_search_service

def index(request):
    if request.method == 'POST':
        product_name = request.POST.get('product_name')
        products = products_search_service(product_name)
        return render(request, 'priceChecker/index.html', {'products': products})
    else:
        return render(request, 'priceChecker/index.html')
