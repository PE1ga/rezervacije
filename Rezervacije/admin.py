from django.contrib import admin

# Register your models here.
from .models import VnosGostov

@admin.register(VnosGostov)
class VnosGostovAdmin(admin.ModelAdmin): #.register(VnosGostov)
    list_display = ['imestranke', 'agencija', 'SO']
    list_filter = ["imestranke"]
    search_fields = ["imestranke"]
