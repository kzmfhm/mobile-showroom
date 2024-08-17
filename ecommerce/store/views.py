from django.shortcuts import render, redirect,get_object_or_404
from . models import *
from django.http import JsonResponse
import json
import datetime
from django.contrib.auth import authenticate, login
from .forms import LoginForm, RegisterForm
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import logout as auth_logout
from .  utils import cookieCart,cartData,guestOrder


def logout_view(request):
    auth_logout(request)
    return redirect('store')

    
@csrf_exempt
def validate_form(request):
    form = RegisterForm(request.POST)
    field = request.POST.get('field')
    response = {}
    
    if field in form.errors:
        response[field] = form.errors[field]
    else:
        response[field] = "valid"
    
    return JsonResponse(response)

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            Customer.objects.create(user=user, name=user.username, email=user.email)
            login(request, user)
            return redirect('store')
    else:
        form = RegisterForm()
    return render(request, 'store/registration/register.html', {'form': form})

def login_view(request):
    form = LoginForm(request.POST or None)
    error_message = None
    
    if request.method == 'POST' and form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('store')
        else:
            error_message = 'Invalid username or password'
    
    context = {
        'form': form,
        'error': error_message,
       
    }
    return render(request, 'store/registration/login.html', context)


def store(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    products = Product.objects.all()
    context = {'products': products, 'cartItems': cartItems}
    return render(request, 'store/store.html', context)

def company_list(request):
    companies = Company.objects.all()
    context = {'companies': companies}
    return render(request, 'store/store.html', context)

def catalog(request, company_id):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    products = Product.objects.filter(company_id=company_id)
    context = {
        'products': products,
        'cartItems': cartItems,
        'order': order,
        'items': items,
        'shipping': False
    }
    return render(request, 'store/catalog.html', context)

def cart(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'store/cart.html', context)

def carDetail(request, product_id=None):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    product = None
    images = []

    if product_id:
        product = get_object_or_404(Product, id=product_id)
        images = product.images.all()

    context = {
        'cartItems': cartItems,
        'order': order,
        'items': items,
        'product': product,
        'images': images
    }
    return render(request, 'store/car_detail.html', context)

def checkout(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'store/checkout.html', context)

def updateItem(request):
	data = json.loads(request.body)
	productId = data['productId']
	action = data['action']
	print('Action:', action)
	print('Product:', productId)

	customer = request.user.customer
	product = Product.objects.get(id=productId)
	order, created = Order.objects.get_or_create(customer=customer, complete=False)

	orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

	if action == 'add':
		orderItem.quantity = (orderItem.quantity + 1)
	elif action == 'remove':
		orderItem.quantity = (orderItem.quantity - 1)

	orderItem.save()

	if orderItem.quantity <= 0:
		orderItem.delete()

	return JsonResponse('Item was added', safe=False)

def processOrder(request):
	transaction_id = datetime.datetime.now().timestamp()
	data = json.loads(request.body)

	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
	else:
		customer, order = guestOrder(request, data)

	total = float(data['form']['total'])
	order.transaction_id = transaction_id

	if total == order.get_cart_total:
		order.complete = True
	order.save()

	if order.shipping == True:
		ShippingAddress.objects.create(
		customer=customer,
		order=order,
		address=data['shipping']['address'],
		city=data['shipping']['city'],
		state=data['shipping']['state'],
		zipcode=data['shipping']['zipcode'],
		)

	return JsonResponse('Payment submitted..', safe=False)

