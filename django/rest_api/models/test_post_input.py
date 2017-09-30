from django import forms
from django.core.validators import validate_email
from rest_api.models.custom_validators import validate_even

class TestPostInput(forms.Form):
    email = forms.EmailField(validators=[validate_email])
    flag = forms.IntegerField()
    even_flag = forms.IntegerField(validators=[validate_even])
