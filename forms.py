from django import forms


class AuthForm(forms.Form):
    pw = forms.CharField(label = "", widget=forms.TextInput(attrs={'class' : 'form-control'}))

class VariableForm(forms.Form):
    lines = forms.IntegerField(label = "", widget=forms.NumberInput(attrs={'class' : 'form-control'}))
    phrases = forms.IntegerField(label = "", widget=forms.NumberInput(attrs={'class' : 'form-control'}))
    offset = forms.IntegerField(label = "", widget=forms.NumberInput(attrs={'class' : 'form-control'}))
    sortKey = forms.CharField(label='sortby', widget=forms.RadioSelect(choices=[(0,'occurrences'),(1,'appearances')]))
