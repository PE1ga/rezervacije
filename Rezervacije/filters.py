import django_filters
from django import forms
from .models import *

class RezervacijeFilter(django_filters.FilterSet):
    unikatneVrednosti= VnosGostov.objects.filter(RNA="ExpColl", status_rez="rezervirano").order_by("agencija").values_list("agencija", flat=True).distinct()
    CHOICES= [(value, str(value)) for value in unikatneVrednosti]   # Izdela LIST CHOICESOV ZA ChoiceField !!!!!
    CHOICES_TIP = [("c","c"),("s","s"),("g","g"),("f","f"),("x","x"),("y","y"),("q","q"),("d","d")]
    
    
    
    imestranke = django_filters.CharFilter(lookup_expr='icontains', label="Ime",
        widget=forms.TextInput(attrs={'class': 'form-control', 'style':"width:200px", 'placeholder': 'Ime'}) )
    
    agencija = django_filters.ChoiceFilter(choices=CHOICES, label="Agencija", widget=forms.Select(attrs={'class': 'form-control'}))
    
    tip = django_filters.ChoiceFilter(choices=CHOICES_TIP, label="Tip", widget=forms.Select(attrs={'class': 'form-control'}))
    
    start_date = django_filters.DateFilter(field_name='od_dt', lookup_expr='gte', label= "Od:",
        widget=forms.DateInput(attrs={'type': 'date', 'style':"width:200px", 'class': 'form-control', 'placeholder': 'Od'}) )
    
    end_date = django_filters.DateFilter(field_name='od_dt', lookup_expr='lte', label="Do:",
        widget=forms.DateInput(attrs={'type': 'date', 'style':"width:200px", 'class': 'form-control', 'placeholder': 'Do'}) )
    class Meta:
        model= VnosGostov
        fields = ["imestranke", "agencija"]
        
          

  