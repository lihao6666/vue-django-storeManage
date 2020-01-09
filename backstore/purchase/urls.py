from django.urls import path
from . import views

app_name = "purchase"

urlpatterns = [

    path('pCs', views.PCsView.as_view(), name='pCs'),
    path('pCNew', views.PCNewView.as_view(), name='pCNewView'),
    path('pcUpdate', views.PcUpdateView.as_view(), name='pcUpdate'),
    path('cdDetailSave', views.CdDetailSaveView.as_view(), name='cdDetailSave'),
    path('cdDetailSubmit', views.CdDetailSubmitView.as_view(), name='cdDetailSubmit'),
    path('cdDetailNew', views.CdDetailNewView.as_view(), name='cdDetailNew'),
    path('pcDelete', views.PcDeleteView.as_view(), name='pcDelete'),

    path('pOs', views.POsView.as_view(), name='pOs'),
    path('pONewByPr', views.PONewByPrView.as_view(), name='pONewByPr'),
    path('prChoice', views.PrChoiceView.as_view(), name='prChoice'),
    path('pONewByPc', views.PONewByPcView.as_view(), name='pONewByPc'),
    path('pcChoice', views.PcChoiceView.as_view(), name='pcChoice'),
    path('pOUpdate', views.POUpdateView.as_view(), name='pOUpdate'),
    path('pOSave', views.POSaveView.as_view(), name='pOSave'),
    path('pOSubmit', views.POSubmitView.as_view(), name='pOSubmit'),
    path('pODelete', views.PODeleteView.as_view(), name='pODelete'),
]
