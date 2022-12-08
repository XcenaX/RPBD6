from django import forms

class LoginForm(forms.Form):
    login = forms.CharField(min_length=3, max_length=100)
    password = forms.CharField(min_length=3, max_length=100)


class RegisterForm(forms.Form):
    login = forms.CharField(min_length=3, max_length=100)
    password = forms.CharField(min_length=3, max_length=100)
    age = forms.IntegerField(min_value=0, max_value=120)
    fullname = forms.CharField(min_length=5, max_length=200)
    role = forms.CharField(min_length=2, max_length=200)

