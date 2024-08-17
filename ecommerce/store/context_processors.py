from .models import Order, Customer
from django.contrib.auth.models import User

def cart_items(request):
    cartItems = 0
    if request.user.is_authenticated:
        try:
            customer = request.user.customer
        except User.customer.RelatedObjectDoesNotExist:
            customer = Customer.objects.create(user=request.user)
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        cartItems = order.get_cart_items
    return {'cartItems': cartItems}
