from django.contrib.auth.models import User
from django import forms
from .models import Member
from django.forms.models import model_to_dict, fields_for_model

class MemberForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username','email','password']

class MemberDetailForm(forms.ModelForm):

    class Meta:
        model = Member
        fields = ['avatar', ]

class UpdateForm(forms.ModelForm):

    class Meta:
        model = Member
        fields = ['avatar']



