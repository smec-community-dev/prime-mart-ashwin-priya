from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required  
from django.contrib.auth import logout
from django.contrib import messages
from django.db.models import Avg,Sum,Q
from .forms import *
from .models import *
from customer.models import*


def seller_register(request):
    if request.method == 'POST':
        user_form = SellerUserForm(request.POST)
        profile_form = SellerProfileForm(request.POST)

        if not user_form.is_valid():
            print("User Form Errors:", user_form.errors)
        if not profile_form.is_valid():
            print("Profile Form Errors:", profile_form.errors)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            user.role = 'seller'
            user.save()

            # Use get_or_create to avoid UNIQUE constraint errors
            profile, created = Seller.objects.get_or_create(user=user)
            profile.name = profile_form.cleaned_data['name']

            profile.address = profile_form.cleaned_data['address']
            profile.save()

            return redirect("seller_login")

    else:
        user_form = SellerUserForm()
        profile_form = SellerProfileForm()

    content = {
        'user_form': user_form,
        'profile_form': profile_form,
    }
    return render(request, 'seller/register.html', content)

def seller_login(request):
    if request.method == "POST":
        form = SellerLoginForm(request.POST)

        if form.is_valid():
            
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(username=username, password=password)

            if user is None:
                messages.error(request, "Invalid username or password.")
                return render(request, "seller/login.html", {"form": form})

            if user.role != "seller":
                messages.error(request, "This account is not registered as a seller.")
                return render(request, "seller/login.html", {"form": form})

            # Login seller
            login(request, user)
            messages.success(request, "Login successful!")
            return redirect("seller_dashboard")

    else:
        form = SellerLoginForm()

    return render(request, "seller/login.html", {"form": form})


@login_required
def seller_dashboard(request):
    if request.user.role != "seller":
        return redirect("seller_login")

    # Safely get seller profile
    try:
        seller = request.user.seller
    except Seller.DoesNotExist:
        messages.error(request, "You do not have a seller profile. Please register first.")
        return redirect("seller_register")

    orders = Order.objects.filter(items__product__seller=seller).distinct().order_by('-order_date')
    products = Product.objects.filter(seller=seller)
    pending_orders = orders.exclude(status='delivered').count()
    total_revenue = orders.aggregate(total=Sum('total_amount'))['total'] or 0

    context = {
        "seller": seller,
        'total_revenue': total_revenue,
        'products': products,
        'pending_orders': pending_orders
    }

    return render(request, "seller/dashboard.html", context)

def seller_logout(request):
    logout(request)
    return redirect("seller_login")


@login_required
def view_products(request):
    if request.user.role != "seller":
        return redirect("seller_login")

    seller = request.user.seller
    products = Product.objects.filter(seller=seller)

    search = request.GET.get('search')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')


    if search:
        products = products.filter(
            Q(name__icontains=search) | Q(description__icontains=search)
        )
    if min_price:
        products = products.filter(price__gte=float(min_price))
    if max_price:
        products = products.filter(price__lte=float(max_price))

    low_stock_count = products.filter(stock__lte=5, stock__gt=0).count()
    out_of_stock_count = products.filter(stock=0).count()
    total_value = sum([p.stock * p.price for p in products])

    content = {
        "products": products,
        "search": search,
        "min_price": min_price,
        "max_price": max_price,
        "low_stock_count": low_stock_count,
        "out_of_stock_count": out_of_stock_count,
        "total_value": total_value,
    }

    return render(request, "seller/products.html", content)


@login_required
def add_product(request):
    if request.user.role != "seller":
        return redirect("seller_login")

    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            product.seller = request.user.seller
            product.save()

            # Save uploaded images
            for image in request.FILES.getlist('images'):
                ProductImage.objects.create(product=product, image_file=image)

            messages.success(request, "Product added successfully!")
            return redirect("products")
    else:
        form = ProductForm()

    return render(request, "seller/add_product.html", {"form": form})


@login_required
def update_product(request, pk):
    if request.user.role != "seller":
        return redirect("seller_login")    
    
    product = get_object_or_404(Product, pk=pk)
    
    if request.method == "POST":
        form = ProductForm(request.POST, instance=product)
        images = request.FILES.getlist('images')  # multiple files

        if form.is_valid():
            form.save()
            # Save new images
            for image in images:
                ProductImage.objects.create(product=product, image_file=image)
            return redirect('products')
    else:
        form = ProductForm(instance=product)

    existing_images = product.images.all()
    return render(request, 'seller/update_product.html', {
        'form': form,
        'product': product,
        'existing_images': existing_images
    })

@login_required
def delete_product(request, pk):
    if request.user.role != "seller":
        return redirect("seller_login")
    
    product = get_object_or_404(Product, pk=pk, seller__user=request.user)
    product.delete()
    messages.success(request, "Product deleted successfully!")
    return redirect("products")

def delete_product_image(request, pk):
    img = get_object_or_404(ProductImage, pk=pk)
    product_id = img.product.id
    img.delete()
    return redirect('update_product', pk=product_id)

@login_required
def view_orders(request):
    if request.user.role != "seller":
        return redirect("seller_login")
    seller = request.user.seller  
    orders = (Order.objects.filter(items__product__seller=seller).distinct().order_by('-order_date'))
    if request.method == "POST":
        order_id = request.POST.get("order_id")
        order = get_object_or_404(Order, id=order_id)
        form = OrderStatusForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('view_orders') 
        
    total_orders = orders.count()
    completed_orders = orders.filter(status='delivered').count()  # replace with your actual status key
    pending_orders = orders.exclude(status='delivered').count()
    total_revenue = orders.aggregate(total=Sum('total_amount'))['total'] or 0

    context = {
        'orders': orders,
        'total_orders': total_orders,
        'completed_orders': completed_orders,
        'pending_orders': pending_orders,
        'total_revenue': total_revenue,
    }

    return render(request, 'seller/view_orders.html', context) 

@login_required
def product_details(request, pk):
    if request.user.role != 'seller':
        return redirect('seller_login')
    product = get_object_or_404(Product, pk=pk, seller=request.user.seller)
    reviews = product.reviews.all()
    average_rating = reviews.aggregate(Avg('rating_value'))['rating_value__avg'] if reviews.exists() else None

    context = {
        'product': product,
        'reviews': reviews,
        'average_rating': average_rating,
    }

    return render(request, 'seller/product_details.html', context)

@login_required
def manage_profile(request):
    if request.user.role != "seller":
        return redirect("seller_login")
    seller = Seller.objects.get(user=request.user) 
    
    products = Product.objects.filter(seller=seller)
    orders = (Order.objects.filter(items__product__seller=seller).distinct().order_by('-order_date'))

    context = {
            "seller": seller,
            "products": products,
            "orders": orders,
        }

    return render(request, "seller/manage_profile.html", context)

@login_required
def edit_profile(request):
    if request.user.role != "seller":
        return redirect("seller_login")

    seller = Seller.objects.get(user=request.user)

    if request.method == "POST":
        seller.name = request.POST.get("name")
        seller.address = request.POST.get("address")
        seller.phone = request.POST.get("phone")
        seller.save()

        user = request.user
        user.email = request.POST.get("email")
        user.save()

        return redirect("manage_profile")

    return render(request, "seller/edit_profile.html", {"seller": seller})