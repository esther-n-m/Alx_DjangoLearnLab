from django import forms

class ExampleForm(forms.Form):
    input_field = forms.CharField(max_length=100, required=True)
