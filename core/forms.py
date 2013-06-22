from django import forms

class PostingForm(forms.Form):
	content = forms.CharField(max_length=250, widget=forms.Textarea())