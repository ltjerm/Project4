
from calendar import firstweekday
import email
import json
import re
from django.shortcuts import render, redirect
from django.views import View
from .models import MenuItem, Category, OrderModel
from django.core.mail import send_mail
from django.http import HttpResponse
from django.contrib.auth import authenticate, logout, login
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.models import User
from django.views.generic.edit import CreateView, UpdateView, DeleteView


# Create your views here.



class Index(View):
    def get(self, request):
        return render(request, 'munch/index.html')


class About(View):
    def get(self, request):
        return render(request, 'munch/about.html')

class Account(View):
    def get(self, request):
        return render(request, 'munch/account.html')

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        myuser = User.objects.create_user(username, email, password1)
      

        myuser.save()

        messages.success(request, 'User created')

        return redirect('/login')

    return render(request, 'munch/register.html')

def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password1 = request.POST['password1']
        if (username == ''): return HttpResponse("No Username!")
        if (password1 == ''): return HttpResponse("No Password!")
        user = authenticate(username=username, password=password1)

        if user is not None: 
            login(request, user) 
            username = user.username
            return redirect('/order', {'username': username})
        else:
            messages.error(request, "Invalid username or password")
            return redirect('/login')
        # return HttpResponse('Your username is ' + username)

    return render(request, "munch/login.html")

def logout_user(request):
    logout(request)
    messages.success(request, 'Logged out')
    return redirect('/')

class Order(View):
    def get(self, request, *args, **kwargs):
        # get every item from each category
        
        entres = MenuItem.objects.filter(category__name__contains='Entre')
        sides = MenuItem.objects.filter(category__name__contains='Side')
        drinks = MenuItem.objects.filter(category__name__contains='Drink')

        # pass into context
        context = {
            'entres': entres,
            'sides': sides,
            'drinks': drinks,
        }

        # render the template
        return render(request, 'munch/order.html', context)

    def post(self, request):
        name = request.POST.get('name')
        email = request.POST.get('email')
        street = request.POST.get('street')
        city = request.POST.get('city')
        state = request.POST.get('state')
        zip = request.POST.get('zip')

        order_items = {
            'items': []
        }

        items = request.POST.getlist('items[]')

        for item in items:
            menu_item = MenuItem.objects.get(pk__contains=int(item))
            item_data = {
                'id': menu_item.pk,
                'name': menu_item.name,
                'price': menu_item.price
            }

            order_items['items'].append(item_data)

            price = 0
            item_ids = []

        for item in order_items['items']:
            price += item['price']
            item_ids.append(item['id'])

        order = OrderModel.objects.create(
            price=price,
            name=name,
            email=email,
            street=street,
            city=city,
            state=state,
            zip=zip
        )
        order.items.add(*item_ids)

        
        body = ('Your food is being made and will be delivered soon!\n'
                f'Your total: {price}\n'
                'Thank you again for your order!')

        send_mail(
            'Thankyou',
            body,
            'example@example.com',
            [email],
            fail_silently=False
        )

        context = {
            'items': order_items['items'],
            'price': price
        }

        return redirect('order-confirmation', pk=order.pk)

class OrderConfirmation(View):
    def get(self, request, pk):
        order = OrderModel.objects.get(pk=pk)

        context = {
            'pk': order.pk,
            'items': order.items,
            'price': order.price,
        }

        return render(request, 'munch/order_confirm.html', context)

    def post(self, request, pk, *args, **kwargs):
        data = json.loads(request.body)

        if data['isPaid']:
            order = OrderModel.objects.get(pk=pk)
            order.is_paid = True
            order.save()

        return redirect('payment-confirmation')




class OrderDetails(View):
    def get(self, request, pk):
        order = OrderModel.objects.get(pk=pk)
        context = {
            'order': order
        }

        return render(request, 'munch/order-details.html', context)







