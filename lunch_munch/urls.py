"""lunch_munch URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from munch.views import Index, About, Order, OrderConfirmation, register, login_user, OrderDetails, Account, logout_user

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('', Index.as_view(), name='index'),
    path('about/', About.as_view(), name='about'),
    path('accounts/', Account.as_view(), name='accounts'),
    path('order/', Order.as_view(), name='order'),
    path('order-confirmation/<int:pk>', OrderConfirmation.as_view(), name='order-confirmation'),
    # path('payment-confirmation/', OrderPayConfirmation.as_view(), name='payment-submitted'),
    path('login/', login_user),
    path('register/', register),
    path('logout/', logout_user),
    path('order-details/', OrderDetails.as_view(), name='order-details'),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)