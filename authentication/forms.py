from django import forms

class EmailForm(forms.Form):
	email = forms.EmailField(max_length=200)

class SignupForm(forms.Form):
	username = forms.CharField(max_length=32)
	password = forms.CharField(max_length=32, widget=forms.PasswordInput())
	fullname = forms.CharField(max_length=64)
	email = forms.CharField(max_length=200, widget=forms.HiddenInput())

class TwitterSignupForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(max_length=32, widget=forms.PasswordInput())

class PasswordSetForm(forms.Form):
    password = forms.CharField(max_length = 64, widget=forms.PasswordInput())