from django.urls import path

from . import views

app_name = "sell"
urlpatterns = [
    # path('totalStock', views.TotalStockView.as_view(), name='totalStock')
    path('sellOrders', views.SellOrdersView.as_view(), name='sellOrders'),
    path('sellOrderNew', views.SellOrderNewView.as_view(), name='sellOrderNew'),
    path('sellOrderUpdate', views.SellOrderUpdateView.as_view(), name='sellOrderUpdate'),
    path('soDetailSubmit', views.SoDetailSubmitView.as_view(), name='soDetailSubmit'),
    path('soDetailSave', views.SoDetailSaveView.as_view(), name='soDetailSave'),
    path('soDetailNew', views.SoDetailNewView.as_view(), name='soDetailNew'),
    # path('soDetailNewSave', views.SoDetailNewSaveView.as_view(), name='soDetailNewSave'),
    # path('soDetailDelete', views.SoDetailDeleteView.as_view(), name='soDetailDelete'),
    path('sellOrderDelete', views.SellOrderDeleteView.as_view(), name='sellOrderDelete'),
]
