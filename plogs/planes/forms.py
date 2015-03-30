from django.forms import ModelForm
from .models import Kit

class SimplePlaneForm(ModelForm):
    class Meta:
        model = Kit
        fields =  ('manufacturer', 'model')

