from django.forms import ModelForm
from .models import Dreamer

class DreamerForm(ModelForm):
    class Meta:
        model = Dreamer
        fields = ['firstname', 'lastname']