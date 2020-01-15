from django import forms
from django.contrib.auth.validators import ASCIIUsernameValidator
from django.core.validators import RegexValidator

#We define some custom validators here
password_validator = RegexValidator(regex=r".{8,}",message="Votre mot de passe doit contenir au moins 8 caractères")

class AddUserForm(forms.Form):
    family_name = forms.CharField(label='',max_length=30,widget=forms.TextInput(  attrs= {'placeholder': 'Prenom','class': 'col-5 m-2 form-control'}))
    first_name = forms.CharField(label='',max_length=30,widget=forms.TextInput( attrs={'placeholder': 'Nom','class': 'col-5 m-2 form-control'}))
    email = forms.CharField(label='',max_length=30,widget=forms.TextInput( attrs={'placeholder': 'Email','class': 'col-5 m-2 form-control'}),
                            validators=[ASCIIUsernameValidator()])
    password = forms.CharField(label='',widget=forms.PasswordInput( attrs={'placeholder': 'Mot de passe','class': 'col-5 m-2 form-control'}),
                                   validators=[password_validator])
    phone = forms.CharField(label='',max_length=15,widget=forms.TextInput( attrs={'placeholder': 'Numéro de téléphone','class': 'col-5 m-2 form-control'}))
    address = forms.CharField(label='',max_length=30,widget=forms.TextInput( attrs={'placeholder': 'Adresse','class': 'col-5 m-2 form-control'}))
    wilaya = forms.CharField(label='', max_length=15, widget=forms.TextInput(
        attrs={'placeholder': 'Wilaya', 'class': 'col-5 m-2 form-control'}))
    commune = forms.CharField(label='', max_length=15, widget=forms.TextInput(
        attrs={'placeholder': 'Commune', 'class': 'col-5 m-2 form-control'}))
