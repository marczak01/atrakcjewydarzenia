from django import forms

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class RegisterForm(forms.Form):
    username = forms.CharField()
    user_email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)