from django.urls import path

from . import views

app_name = "storeIn"
urlpatterns = [
    path('biss', views.BissView.as_view(), name='biss'),
    path('bisNew', views.BisNewView.as_view(), name='bisNew'),
    path('bisUpdate', views.BisUpdateView.as_view(), name='bisUpdate'),
    path('pOChoice', views.POChoiceView.as_view(), name='pOChoice'),
    path('bisDSave', views.BisDSaveView.as_view(), name='bisDSave'),
    path('bisDSubmit', views.BisDSubmitView.as_view(), name='bisDSubmit'),
    path('bisDelete', views.BisDeleteView.as_view(), name='bisDelete')
]
