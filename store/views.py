from django.shortcuts import render, redirect
from .models import Product, Cart, Order

def home(request):
    products = Product.objects.all()
    return render(request, 'home.html', {'products': products})
 

def add_to_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    Cart.objects.create(product=product)
    return redirect('/')
def cart(request):
    cart_items = Cart.objects.all()

    total = 0
    for item in cart_items:
        total += item.product.price * item.quantity

    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'total': total
    })
def remove_from_cart(request, cart_id):
    item = Cart.objects.get(id=cart_id)
    item.delete()
    return redirect('cart')
def increase_quantity(request, cart_id):
    item = Cart.objects.get(id=cart_id)
    item.quantity += 1
    item.save()
    return redirect('cart')

def decrease_quantity(request, cart_id):
    item = Cart.objects.get(id=cart_id)

    if item.quantity > 1:
        item.quantity -= 1
        item.save()
    else:
        item.delete()

    return redirect('cart')
def checkout(request):
    cart_items = Cart.objects.all()

    total = 0
    for item in cart_items:
        total += item.product.price * item.quantity

    if request.method == "POST":
        name = request.POST["name"]
        address = request.POST["address"]
        phone = request.POST["phone"]

        Order.objects.create(
            name=name,
            address=address,
            phone=phone,
            total_price=total
        )

        Cart.objects.all().delete()

        return render(request, "success.html")

    return render(request, "checkout.html", {"total": total})