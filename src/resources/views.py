from django.shortcuts import render
from django.core.paginator import Paginator
from accounts.models import UserProfileInfo
        
# Create your views here.

def resources(request):
    return render(request, 'resources/resources.html')

def ctf42(request):
    return render(request, 'resources/42ctf.html')

def tools(request):
    return render(request, 'resources/tools.html')

def create_challenge(request):
    return render(request, 'resources/create_challenge.html')

def translate(request):
    return render(request, 'resources/translate.html')

def edit(request):
    return render(request, 'resources/edit.html')

def donate(request):
    return render(request, 'resources/donate.html')