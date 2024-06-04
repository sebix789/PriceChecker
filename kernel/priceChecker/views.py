from django.shortcuts import render, redirect
from .services import products_search_service, shop_filter_service

def index(request):
    if request.method == 'POST':
        product_name = request.POST.get('product_name')
        products = products_search_service(product_name)
        request.session['products'] = products
        return redirect('priceChecker:results')
    else:
        return render(request, 'priceChecker/index.html')

def results(request):
    products = request.session.get('products', [])
    if request.method == 'POST':
        shop_name = request.POST.get('data_type')
        if shop_name:
            products = shop_filter_service(shop_name)
    return render(request, 'priceChecker/results.html', {'products': products})
    
    