from django.contrib import admin
from .models import Trade, AptTrade

# Register your models here.

# admin 계정 : lhwn / gd16741
admin.site.register(Trade)
admin.site.register(AptTrade)