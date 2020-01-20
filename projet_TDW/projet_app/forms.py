from django import forms
from django.contrib.auth.validators import ASCIIUsernameValidator
from .models import TranslationCategory, Language
from django.core.validators import RegexValidator

#We define some custom validators here
password_validator = RegexValidator(regex=r".{8,}",message="Votre mot de passe doit contenir au moins 8 caractères")
file_name_pdf_validator = RegexValidator(regex=r".*pdf",message="Votre fichier doit être de format PDF")

#these two for providing the sets of choices for language and category choice fields
LANGUAGE_NAMES = tuple([(i.pk,i.name) for i in Language.objects.all()])
CATEGORY_NAMES = tuple([(i.pk,i.name) for  i in TranslationCategory.objects.all()])
RATES = [(str(i),str(i)) for i in range(1,11)]


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

    def __init__(self, *args, **kwargs):
        super(AddUserForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.error_messages = {'required': 'Ce champ est requis'.format(
                fieldname=field.label)}

class AddTranslatorForm(AddUserForm):
    languages = forms.MultipleChoiceField(choices=Language.objects.all().values_list("id", "name"), widget=forms.CheckboxSelectMultiple,required=True)
    categories = forms.MultipleChoiceField(choices=TranslationCategory.objects.all().values_list("id", "name"), widget=forms.CheckboxSelectMultiple,required=True)
    cv = forms.FileField(required=True, label="Choisir un fichier à envoyer",validators=[file_name_pdf_validator])
    assrmented_file = forms.FileField(required=False,label="Choisir un fichier à envoyer",validators=[file_name_pdf_validator])
    ref1 = forms.FileField(required=True, label="Choisir un fichier à envoyer (Ce champs est requis)",validators=[file_name_pdf_validator])
    ref2 = forms.FileField(label="Choisir un fichier à envoyer", required=False,validators=[file_name_pdf_validator])
    ref3 = forms.FileField(label="Choisir un fichier à envoyer", required=False,validators=[file_name_pdf_validator])

    def __init__(self, *args, **kwargs):
        super(AddTranslatorForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.error_messages = {'required': 'Ce champ est requis'.format(
                fieldname=field.label)}

class TranslationOfferForm(forms.Form):
    price = forms.FloatField(widget=forms.NumberInput(attrs={'class': 'col-5 m-2 form-control'}))
    accept_price = forms.FloatField(widget=forms.NumberInput(attrs={'class': 'col-5 m-2 form-control'}),required=False)
    notes = forms.CharField(widget=forms.Textarea(attrs={'class':"form-control h-25"}),required=False)

    def __init__(self, *args, **kwargs):
        super(TranslationOfferForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.error_messages = {'required': 'Ce champ est requis'.format(
                fieldname=field.label)}

class SendFileForm(forms.Form):
    file = forms.FileField(label="Choisir un fichier à envoyer",validators=[file_name_pdf_validator])
    def __init__(self, *args, **kwargs):
        super(SendFileForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.error_messages = {'required': 'Ce champ est requis'.format(
                fieldname=field.label)}

class ReportUserForm(forms.Form):
    warn = forms.CharField(widget=forms.Textarea(attrs={'class': "form-control h-25"}))

class RateForm(forms.Form):
    rate = forms.TypedChoiceField(choices=RATES,coerce=int)


