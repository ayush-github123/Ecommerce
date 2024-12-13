from django.shortcuts import render, get_object_or_404, redirect
from .models import Cart, CartItem
from products.models import Product
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import HttpResponseRedirect
# Create your views here.

@login_required(login_url='login-page')
def cartView(request):
    if not request.user.is_authenticated:
        return redirect('login-page')

    cart,created = Cart.objects.get_or_create(user=request.user) # 
    return render(request, 'cart/cart.html', {"cart":cart})

@login_required(login_url='login-page')
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, created  = Cart.objects.get_or_create(user=request.user)  


    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

    if not created:  # If the item already exists, just increase the quantity
        cart_item.quantity += 1
        cart_item.save()
    else:
        cart_item.save()

    return redirect('home') # Redirect to the cart page


@login_required(login_url='login')
def remove_from_cart(request, product_id):
    cart_item = get_object_or_404(CartItem, id=product_id, cart__user=request.user)
    cart_item.delete()
    return HttpResponseRedirect(reverse('cart:cart-page'))


@login_required(login_url='login-page')
def update_cart(request, product_id):
        product = get_object_or_404(Product, id=product_id)
        cart = Cart.objects.get(user=request.user)
        cart_item = CartItem.objects.get(cart__user=request.user, product=product)  #can also be cart=cart in place cart__user=request.user 

        # Get quantity from POST request
        quantity_str = request.POST.get('quantity')
        
        if quantity_str:  # Ensure quantity exists
            new_quantity = int(quantity_str)  # Convert to integer
            if new_quantity <= 0:
                new_quantity = 1  # Set to 1 if quantity is zero or less
            cart_item.quantity = new_quantity
            cart_item.save()
        else:
            # If quantity is not valid or not provided, set to 1 by default
            cart_item.quantity = 1
            cart_item.save()
        
        return redirect('cart:cart-page')  # Redirect back to the cart page

    # except ValueError:
    #     # If conversion to int fails, it means the quantity was not a valid number
    #     return redirect('cart:cart-page')  # Redirect to cart page or handle as needed
    # except CartItem.DoesNotExist:
    #     # If the CartItem does not exist, handle the error appropriately
    #     return redirect('cart:cart-page')  # Redirect to cart page or handle as needed

