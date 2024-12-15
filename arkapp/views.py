from django.shortcuts import render
from arkapp.models import Product
from django.http import JsonResponse
from math import ceil
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

def home(request):
    allProds = []
    catprods = Product.objects.values('category', 'id')  # Get categories and product IDs
    cats = {item['category'] for item in catprods}  # Get distinct categories

    items_per_slide = 4  # Number of products to display per slide

    # Loop through categories and calculate the number of slides needed
    for cat in cats:
        prod = Product.objects.filter(category=cat)  # Filter products by category
        n = len(prod)  # Number of products in the category
        nSlides = n // items_per_slide + ceil((n / items_per_slide) - (n // items_per_slide))  # Calculate number of slides
        allProds.append([prod, range(1, nSlides), nSlides])  # Store products, slides, and slide count
    
    params = {'allProds': allProds}
    return render(request, 'index.html', params)  # Render 'index.html' template with the data


def purchase(request):
    allProds = []
    catprods = Product.objects.values('category', 'id')
    cats = {item['category'] for item in catprods}

    for cat in cats:
        prod = Product.objects.filter(category=cat)
        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        allProds.append([prod, range(1, nSlides), nSlides])

    params = {'allProds': allProds}
    return render(request, 'purchase.html', params)



def checkout(request):
    # Retrieve the cart from the session (session-based cart)
    cart = request.session.get('cart', [])
    
    # If you're using a database model like Cart for storing the cart, you can use it here:
    # cart = Cart.objects.filter(user=request.user)  # Uncomment this if you're using a database model
    
    # Calculate the total cost of items in the cart (if session-based)
    total = sum(item['price'] * item['quantity'] for item in cart)

    # Handle the form submission for order processing
    if request.method == 'POST':
        shipping_address = request.POST.get('shipping_address')  # Get shipping address
        payment_method = request.POST.get('payment_method')  # Get payment method

        # Save order details (you may want to store the order in a model here)
        
        # Clear the cart after checkout
        request.session['cart'] = []  
        
        # Show confirmation page with order details
        return render(request, 'order_confirmation.html', {
            'shipping_address': shipping_address,
            'payment_method': payment_method,
            'total': total
        }) 

    # Render 'checkout.html' with cart details and total price
    return render(request, 'checkout.html', {'cart': cart, 'total': total})

@login_required
def add_to_cart(request, product_id):
    product = Product.objects.get(id=product_id)  # Get the product by its ID
    cart = request.session.get('cart', [])  # Retrieve the cart from the session
    
    # Check if the product is already in the cart
    for item in cart:
        if item['id'] == product.id:
            item['quantity'] += 1  # Increase the quantity if the product is already in the cart
            break
    else:
        cart.append({'id': product.id, 'name': product.name, 'price': product.price, 'quantity': 1})  # Add new product to the cart
    
    request.session['cart'] = cart  # Update the session with the new cart
    return JsonResponse({'message': 'Product added to cart successfully!'})  # Return a success message in JSON format


from django import template

register = template.Library()

@register.filter
def multiply(value, arg):
    """Multiplies value by arg."""
    try:
        return value * arg
    except (TypeError, ValueError):
        return 0  # Return 0 if multiplication fails (e.g., non-numeric types)