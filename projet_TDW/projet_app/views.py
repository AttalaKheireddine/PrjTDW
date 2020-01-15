from django.shortcuts import render,redirect
from .models import TranslationCategory,Language,TranslatorProfile,UserProfile
from .forms import AddUserForm
from django.http import JsonResponse
from django.views.generic import View
from django.db.models import Q
from django.core.serializers import serialize
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.models import User
import json
# Create your views here.

ALL_CATEGORIES = TranslationCategory.objects.all()
ALL_LANGUAGES = Language.objects.all()
EMPTY_USER_FORM = AddUserForm(auto_id=False)

class HomeView(View):
    def get(self,request):
        return render(request, "home.html", {"categories": ALL_CATEGORIES, "languages": ALL_LANGUAGES,"form":EMPTY_USER_FORM})


class TranslatorsSelect(View):
    def get(self,request):
        filters = Q()
        filters &= Q(languages__name = request.GET['src_language'])
        filters &= Q(languages__name = request.GET['dest_language'])
        filters &= Q(categories__name = request.GET['category'])

        translators = TranslatorProfile.objects.filter(filters).order_by("-global_rate")

        return render(request,"_ajax_translators.html",{'translators':translators})

class Logout(View,LoginRequiredMixin):
    def get(self,request):
        logout(request)
        return redirect("projet_app:home")

class Login(View):
    def post(self,request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect("projet_app:home")
        else:
            return render(request, "home.html", {"categories": ALL_CATEGORIES, "languages": ALL_LANGUAGES,"form":EMPTY_USER_FORM
                          ,"err_msg":"Combinaison email/mot de passe invalide"})



class Register(View):
    def post(self, request):
        new_form = AddUserForm(request.POST)
        if new_form.is_valid():
            user = User()
            user.username = new_form.cleaned_data['email']
            user.set_password(new_form.cleaned_data['password'])
            user.save()

            profile = UserProfile()
            profile.phone_number = new_form.cleaned_data['phone']
            profile.full_name = "{} {}".format(new_form.cleaned_data['family_name'].upper(),new_form.cleaned_data['first_name'].title())
            profile.address =  new_form.cleaned_data['address']
            profile.user = user
            profile.wilaya = new_form.cleaned_data["wilaya"]
            profile.commune = new_form.cleaned_data["commune"]
            profile.save()
            return redirect("projet_app:home")
        else:
            return render(request, "home.html",{"categories": ALL_CATEGORIES, "languages": ALL_LANGUAGES, "form": new_form
                                                ,"err_msg":"Veuillez corriger les informations d'enregistrement (ouvrez l'onglet d'enregistrement pour plus de détails)"})