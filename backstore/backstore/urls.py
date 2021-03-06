"""backstore URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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

urlpatterns = [
    path('admin/', admin.site.urls),
    path('base/', include(('base.urls', 'base'), namespace='base')),
    path('purchaseRequest/', include(('purchaseRequest.urls', 'purchaseRequest'), namespace='purchaseRequest')),
    path('storeManage/', include(('storeManage.urls', 'storeManage'), namespace='storeManage')),
    path('sell/', include(('sell.urls', 'sell'), namespace='sell')),
    path('purchase/', include(('purchase.urls', 'purchase'), namespace='purchase')),
    path('storeIn/', include(('storeIn.urls', 'storeIn'), namespace='storeIn')),
    path('storeAdjust/', include(('storeAdjust.urls', 'storeAdjust'), namespace='storeAdjust'))

]
