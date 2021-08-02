from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import OrderForm, CreateUserForm, CustomerForm
from .filters import OrderFilter
from .decorators import *

# Create your views here.


def index(request):
    return render(request, 'accounts/index.html')


@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def userPage(request):
    customer = request.user
    orders = request.user.customer.order_set.all()
    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    on_the_way = orders.filter(status='On the way').count()
    pending = orders.filter(status='Pending').count()
    data = {'customer': customer, 'orders': orders,
            'total_orders': total_orders, 'delivered': delivered,
            'on_the_way': on_the_way, 'pending': pending}
    return render(request, 'accounts/user.html', data)


@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def accountSettings(request):
    customer = request.user.customer
    form = CustomerForm(instance=customer)

    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES, instance=customer)
        if form.is_valid():
            form.save()

    data = {'form': form}
    return render(request, 'accounts/account_settings.html', data)


@login_required(login_url='login')
@admin_only
def home(request):
    customers = Customer.objects.all()
    orders = Order.objects.all()
    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    on_the_way = orders.filter(status='On the way').count()
    pending = orders.filter(status='Pending').count()
    data = {'customers': customers, 'orders': orders,
            'total_orders': total_orders, 'delivered': delivered,
            'on_the_way': on_the_way, 'pending': pending}
    return render(request, 'accounts/dashboard.html', data)


@unauthenticated_user
def registerPage(request):

    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, 'Account created successfully for ' + username)

            group = Group.objects.get(name='customer')
            user.groups.add(group)
            Customer.objects.create(
                user=user,
                name=str(user.first_name + " " + user.last_name),
                email=user.email
            )

            return redirect('login')

    data = {'form': form}
    return render(request, 'accounts/register.html', data)


@unauthenticated_user
def loginPage(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid Username or Password')

    return render(request, 'accounts/login.html')


def logoutUser(request):
    logout(request)
    return redirect('index')


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def products(request):
    prods = Product.objects.all()
    return render(request, 'accounts/products.html', {'products': prods})


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def customer(request, customer_key):
    cust = Customer.objects.get(id=customer_key)
    orders = Order.objects.filter(customer=cust.id)
    total_orders = orders.count()

    order_filter = OrderFilter(request.GET, queryset=orders)
    orders = order_filter.qs

    data = {'customer': cust, 'orders': orders, 'total_orders': total_orders, 'order_filter': order_filter}
    return render(request, 'accounts/customer.html', data)


@login_required(login_url='login')
def createOrder(request):
    customer = Customer.objects.get(user=request.user)
    form = OrderForm(initial={'customer': customer, 'status': 'Pending'})

    if request.method == 'POST':
        form_data = OrderForm(request.POST)
        if form_data.is_valid():
            form_data.save()
            return redirect('home')

    data = {'form': form, 'task': 'Create'}
    return render(request, 'accounts/create_order.html', data)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def updateOrder(request, order_key):
    order = Order.objects.get(id=order_key)
    form = OrderForm(instance=order)

    if request.method == 'POST':
        form_data = OrderForm(request.POST, instance=order)
        if form_data.is_valid():
            form_data.save()
            return redirect('home')

    data = {'form': form, 'task': 'Update'}
    return render(request, 'accounts/create_order.html', data)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def deleteOrder(request, order_key):
    order = Order.objects.get(id=order_key)

    if request.method == 'POST':
        order.delete()
        return redirect('home')

    data = {'order': order}
    return render(request, 'accounts/delete_order.html', data)
