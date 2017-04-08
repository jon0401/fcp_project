from django import forms
from django.utils.translation import ugettext_lazy as _

from .models import Tag

class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        exclude = ()
        
        fields = ('name',)
        labels = {
            'name': _(''),
        }