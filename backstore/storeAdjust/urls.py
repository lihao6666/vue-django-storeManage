from django.urls import path
from . import views

app_name = "storeAdjust"

urlpatterns = [
    path('trs', views.TrsView.as_view(), name='trs'),
    path('trNew', views.TrNewView.as_view(), name='trNew'),
    path('trUpdate', views.TrUpdateView.as_view(), name='trUpdate'),
    path('trdSave', views.TrdSaveView.as_view(), name='trdSave'),
    path('trdSubmit', views. TrdSubmitView.as_view(), name='trdSubmit'),
    path('trdNew', views.TrdNewView.as_view(), name='trdNew'),
    path('trDelete', views.TrDeleteView.as_view(), name='trDelete'),

    path('transfers', views.TransfersView.as_view(), name='transfers'),
    path('transferNew', views.TransferNewView.as_view(), name='transferNew'),
    path('stDetailNewByTr', views.StDetailNewByTrView.as_view(), name='stDetailNewByTr'),
    path('stDetailNew', views.StDetailNewView.as_view(), name='stDetailNew'),
    path('transferUpdate', views.TransferUpdateView.as_view(), name='transferUpdate'),
    path('stDetailSubmit', views.StDetailSubmitView.as_view(), name='stDetailSubmit'),
    path('transferDelete', views.TransferDeleteView.as_view(), name='transferDelete'),

]
