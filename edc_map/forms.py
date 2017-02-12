from django import forms

from .models import MapDivision


class MapDivisionForm(forms.ModelForm):

    class Meta:
        model = MapDivision
        fields = '__all__'
