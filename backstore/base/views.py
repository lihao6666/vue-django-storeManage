from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from base import models
# Create your views here.
from django.http import HttpResponse


def user_login(request):
    if request.method == 'POST':
        print(request.POST)
        print(request.POST.get('user_id'))
        user = models.UserProfile.objects.all()
        print(user)
        return HttpResponse({'user': user})
