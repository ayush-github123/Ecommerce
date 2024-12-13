from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User 
from django.contrib import messages
from products.models import Product, Category
from cart.models import Cart, CartItem
from django.contrib.auth.decorators import login_required
# Create your views here.

def home(request):
    return render(request, 'home.html')

def cart(request):
    pass

def products(request):
    products = Product.objects.all()
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
        return render(request, 'home.html', {'products':products, 'cart':cart})
    return render(request, 'home.html', {'products':products})


def login_page(request):

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, 'Login Successfull')
            return redirect('home')
        else:
            messages.error(request, 'Invalid Credentials')
            return render(request, 'login.html')
        
    return render(request, 'login.html')


def logout_page(request):
    logout(request)
    messages.success(request, 'Logout Successfull')
    return redirect('home')


def register(request):

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists')
            return redirect('register')
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username aleardy exists')
            return redirect('register')
        
        if password != confirm_password:
            messages.error(request, "Passwords do not match")
            return redirect("register")
        else:
            user = User.objects.create_user(username = username, email = email, password = password)
            user.save()
            messages.success(request, "Registration Successfull")
            return redirect('home')
    else:
        return render(request, 'registration.html')


# @login_required(login_url='login-page')
# def cartView(request):
#     if not request.user.is_authenticated:
#         return redirect('login-page')

#     cart,created = Cart.objects.get_or_create(user=request.user) 
#     return render(request, 'cart.html', {"cart":cart})
