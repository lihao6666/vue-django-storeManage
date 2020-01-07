from django.urls import path
from . import views

app_name = "purchase"

urlpatterns = [
    path('prs', views.PrsView.as_view(), name='prs'),
    # path('prEdit', views.PrEditView.as_view(), name='prEdit'),
    path('prNew', views.PrdNewView.as_view(), name='prNew'),
    path('prUpdate', views.PrUpdateView.as_view(), name='prUpdate'),
    path('prdSave', views.PrdSaveView.as_view(), name='prdSave'),
    path('prdSubmit', views.PrdSubmitView.as_view(), name='prdSubmit'),
    path('prdNew', views.PrdNewView.as_view(), name='prdNew'),
    path('prdNewSave', views.PrdNewSaveView.as_view(), name='prdNewSave'),
    path('prdDelete', views.PrdDeleteView.as_view(), name='prdDelete'),
    path('prDelete', views.PrDeleteView.as_view(), name='prDelete'),
    path('prClose', views.PrCloseView.as_view(), name='prClose')
]
