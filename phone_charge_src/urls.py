"""
URL configuration for phone_charge_src project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path

from accounts.views import RechargePhoneNumberView
from orders.views import CreditIncreaseRequestView, ApproveCreditIncreaseView
from swagger import schema_view

urlpatterns = [
    path('admin/', admin.site.urls),
path('swagger/', schema_view.with_ui('swagger',
                                         cache_timeout=0), name='schema-swagger-ui'),
    path('credit-increase-request/', CreditIncreaseRequestView.as_view(), name='credit-increase-request'),
    path('approve-credit-increase/<int:order_id>/', ApproveCreditIncreaseView.as_view(), name='approve-credit-increase'),
    path('recharge-phone-number/', RechargePhoneNumberView.as_view(), name='recharge-phone-number'),

]
