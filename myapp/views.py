from django.shortcuts import render
from .models import AptTrade

# Create your views here.

def home(request):
    return render(request, 'myapp/home.html')

def index(request):
    return render(request, 'myapp/index.html')

def aptTrade(request):
    aptTrades = AptTrade.objects.all()
    return render(request, 'myapp/viewAptTrades.html', {'aptTrades': aptTrades})
