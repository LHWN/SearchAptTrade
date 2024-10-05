from django.urls import path
from .views import home, index, aptTrade
# from .createDB import selectTrade

urlpatterns = [
    path('', home, name='home'),
    # path('SearchAptTrades/', index, name='index'),
    path('SearchAptTrades/', aptTrade, name='aptTrade'),
    # path('selectTrade/', selectTrade, name='selectTrade')
]