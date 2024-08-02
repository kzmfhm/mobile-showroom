from django.shortcuts import render, get_object_or_404
from .models import *

def store(request):
    companies = Company.objects.all()
    context = {'companies': companies}
    return render(request, 'store/store.html', context)

def catalog(request, company_id):
    company = get_object_or_404(Company, id=company_id)
    products = Product.objects.filter(company=company)
    context = {'company': company, 'products': products}
    return render(request, 'store/catalog.html', context)

def car_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    images = product.images.all()
    context = {'product': product, 'images': images}
    return render(request, 'store/car_detail.html', context)
