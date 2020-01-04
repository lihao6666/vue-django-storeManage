from django.urls import path

from . import views

app_name = "storeManage"
urlpatterns = [
    path('totalStock', views.TotalStockView.as_view(), name='totalStock')
]
