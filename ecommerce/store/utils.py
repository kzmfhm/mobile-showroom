import json
from .models import Product, Customer, Order, OrderItem

def cookieCart(request):
    try:
        cart = json.loads(request.COOKIES.get('cart', '{}'))
    except json.JSONDecodeError:
        cart = {}
        print('CART:', cart)

    items = []
    order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}
    cartItems = order['get_cart_items']

    for i in cart:
        try:
            if cart[i]['quantity'] > 0:
                cartItems += cart[i]['quantity']

                product = Product.objects.get(id=i)
                total = round(product.price * cart[i]['quantity'], 2)

                order['get_cart_total'] += total
                order['get_cart_items'] += cart[i]['quantity']

                item = {
                    'id': product.id,
                    'product': {
                        'id': product.id,
                        'name': product.name,
                        'price': product.price,
                        'model': product.model,
                        'year': product.year,
                        'engine_type': product.engine_type,
                        'transmission_type': product.transmission_type,
                        'imageURL': product.imageURL,
                    },
                    'quantity': cart[i]['quantity'],
                    'digital': product.digital,
                    'get_total': total,
                }
                items.append(item)

                if not product.digital:
                    order['shipping'] = True
        except Product.DoesNotExist:
            pass

    return {'cartItems': cartItems, 'order': order, 'items': items}

def cartData(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        cookieData = cookieCart(request)
        cartItems = cookieData['cartItems']
        order = cookieData['order']
        items = cookieData['items']

    return {'cartItems': cartItems, 'order': order, 'items': items}

def guestOrder(request, data):
    name = data['form']['name']
    email = data['form']['email']

    cookieData = cookieCart(request)
    items = cookieData['items']

    customer, created = Customer.objects.get_or_create(email=email)
    customer.name = name
    customer.save()
    print(customer)

    order = Order.objects.create(customer=customer, complete=False)

    for item in items:
        product = Product.objects.get(id=item['id'])
        OrderItem.objects.create(
            product=product,
            order=order,
            quantity=item['quantity'] if item['quantity'] > 0 else -item['quantity'],
        )

    return customer, order
