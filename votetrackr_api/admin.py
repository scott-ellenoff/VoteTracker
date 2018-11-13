from django.contrib import admin
from .models import Legislator, Bill, Vote

# Register your models here.
admin.site.register(Bill)
admin.site.register(Legislator)
admin.site.register(Vote)
