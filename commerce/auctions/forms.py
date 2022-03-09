from django.forms import ModelForm,Textarea
from django.forms.fields import FloatField, URLField
from django.forms.widgets import TextInput, NumberInput, URLInput,Select
from .models import product


class createForm(ModelForm):
    class Meta:
        model= product
        fields=["item","price","definition","creator","category","imageUrl"]
        widgets={
            "item":TextInput(attrs={"class":"form-control"}),
            "price":NumberInput(attrs={"class":"form-control"}),
            "definition":Textarea(attrs={"class":"form-control"}),
            "creator":TextInput(attrs={"class":"form-control"}),
            "category":Select(attrs={"class":"form-control"}),
            "imageUrl":URLInput(attrs={"class":"form-control"}),
                }
