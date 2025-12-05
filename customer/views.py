from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django import forms
from .forms import *
from .models import *
from seller.models import *

def home(request):
    products = Product.objects.prefetch_related('images').all()
    context = {
        'products': products
    }
    return render(request,'customer/index.html',context)

def user_registration(request):
    if request.method == "POST":
        user_form = CustomerSignUpForm(request.POST)
        profile_form = ProfileForm(request.POST)

        if user_form.is_valid and profile_form.is_valid():
            user=user_form.save(commit=False)
            user.role='customer'
            user.save()
            profile=profile_form.save(commit=False)
            profile.user=user
            profile.save()
            return redirect('user_login')  
    else:
        user_form=CustomerSignUpForm()
        profile_form=ProfileForm()
    content = {
        'user_form':user_form,
        'profile_form':profile_form,
    }
    return render (request,'customer/signup.html',content)


def user_login(request):
    if request.method == 'POST':
        form = CustomerLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('index')   # URL name, not HTML file
            else:
                form.add_error(None, "Invalid username or password")
    else:
        form = CustomerLoginForm()

    return render(request, "customer/login.html", {"form": form})


def customer_logout(request):
    logout(request)    
    return redirect('user_login')


def product_details(request, name):
    product = get_object_or_404(Product, name=name)
    return render(request,'customer/product_details.html',{'product': product})


def add_to_cart(request, product_id):
    if not request.user.is_authenticated:
        return redirect('user_login')  
    customer = request.user.customer   
    product = get_object_or_404(Product, id=product_id)
    cart_item, created = Cart.objects.get_or_create(
        customer=customer,
        product=product
    )
    if not created:
        cart_item.quantity += 1
    cart_item.save()
    return redirect('cart_view')


def cart_view(request):
    if not request.user.is_authenticated:
        return redirect('user_login')
    customer = request.user.customer
    cart_items = Cart.objects.filter(customer=customer)
    total = sum(item.product.price * item.quantity for item in cart_items)
    return render(request,'customer/cart.html',{'cart_items': cart_items,'total': total})


def add_to_wishlist(request, product_id):
    if not request.user.is_authenticated:
        return redirect('user_login')
    customer = get_object_or_404(Customer, user=request.user)
    product = get_object_or_404(Product, id=product_id)
    if Wishlist.objects.filter(customer=customer, product=product).exists():
        return redirect('wishlist_view') 
    Wishlist.objects.create(customer=customer, product=product)
    return redirect('wishlist_view')


def wishlist_view(request):
    if not request.user.is_authenticated:
        return redirect('user_login')
    customer = request.user.customer
    wishlist_items = Wishlist.objects.filter(customer=customer)
    return render(request, "customer/wishlist.html", {"wishlist_items": wishlist_items})
