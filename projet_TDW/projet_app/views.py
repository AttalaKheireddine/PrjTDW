from django.shortcuts import render,redirect
from .models import TranslationCategory,Language,TranslatorProfile
from django.http import JsonResponse
from django.views.generic import View
from django.db.models import Q
from django.core.serializers import serialize
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login,logout,authenticate
import json
# Create your views here.

ALL_CATEGORIES = TranslationCategory.objects.all()
ALL_LANGUAGES = Language.objects.all()


class HomeView(View):
    def get(self,request):
        return render(request, "home.html", {"categories": ALL_CATEGORIES, "languages": ALL_LANGUAGES})


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
            return render(request, "home.html", {"categories": ALL_CATEGORIES, "languages": ALL_LANGUAGES,"err_msg":"Combinaison email/mot de passe invalide"})
            


class Register(View):
    def Post(self, request):
        ""


