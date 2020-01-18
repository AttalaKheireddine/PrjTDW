from django.shortcuts import render, redirect
from .models import TranslationCategory, Language, TranslatorProfile, UserProfile, TranslationRequest,ReferenceFile,TranslationOffer
from .forms import AddUserForm, AddTranslatorForm,TranslationOfferForm
from django.views.generic import View
from django.db.models import Q
from django.db import IntegrityError
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib import messages
from django.utils import timezone
# Create your views here.


ALL_CATEGORIES = TranslationCategory.objects.all()
ALL_LANGUAGES = Language.objects.all()
EMPTY_USER_FORM = AddUserForm(auto_id=False)


class HomeView(View):
    def get(self, request):
        return render(request, "home.html",
                      {"categories": ALL_CATEGORIES, "languages": ALL_LANGUAGES, "form": EMPTY_USER_FORM})


class TranslatorsSelect(View):
    def get(self, request):
        filters = Q()
        filters &= Q(languages__name=request.GET['src_language'])
        filters2 = Q(languages__name=request.GET['dest_language'])
        filters &= Q(categories__name=request.GET['category'])

        if request.GET["sworn_in"] == "true":
            filters &= Q(is_assermented=True)

        translators = TranslatorProfile.objects.filter(filters).filter(filters2).order_by("-global_rate")

        return render(request, "_ajax_translators.html", {'translators': translators})


class Logout(View, LoginRequiredMixin):
    def get(self, request):
        logout(request)
        return redirect("projet_app:home")


class Login(View):
    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
        else:
            messages.add_message(request, messages.ERROR, 'Combinaison email/mot de passe invalide')
        return redirect("projet_app:home")


class Register(View):
    def post(self, request):
        new_form = AddUserForm(request.POST)
        if new_form.is_valid():
            user = User()
            user.username = new_form.cleaned_data['email']
            user.set_password(new_form.cleaned_data['password'])
            try:
                user.save()
            except IntegrityError:
                messages.add_message(request, messages.ERROR, 'Cet utilisateur existe déja. Veuillez prendre un autre email')
                return redirect("projet_app:recruit")


            profile = UserProfile()
            profile.phone_number = new_form.cleaned_data['phone']
            profile.full_name = "{} {}".format(new_form.cleaned_data['family_name'].upper(),
                                               new_form.cleaned_data['first_name'].title())
            profile.address = new_form.cleaned_data['address']
            profile.user = user
            profile.wilaya = new_form.cleaned_data["wilaya"]
            profile.commune = new_form.cleaned_data["commune"]
            profile.save()
            login(request, user)
        else:
            err = "Veuillez corriger les informations d'enregistrement (ouvrez l'onglet d'enregistrement pour plus de détails)."
            messages.add_message(request, messages.ERROR, err)
        return redirect("projet_app:home")


class SendRequest(View):
    def post(self, request):
        family_name = request.POST.get("family_name","")
        first_name = request.POST.get("first_name","")
        email = request.POST.get("email","")
        phone = request.POST.get("phone","")
        address = request.POST.get("address","")
        translators = request.POST.get("translators",'')
        src_lang = request.POST.get("src_lang",'')
        dest_lang = request.POST.get("dest_lang",'')
        category = request.POST.get("category",'')
        notes = request.POST.get("notes",'')
        file = request.FILES.get('file_req','')

        for i in [family_name, first_name, email, phone, address]:
            if not i:
                messages.add_message(request, messages.ERROR, 'Veuillez renseigner l\'ensemble des informations personnelles nécessaires')
                return redirect("projet_app:home")

        if src_lang == dest_lang:
            messages.add_message(request, messages.ERROR, 'Les langues source et destination ne peuvent être égales')
            return redirect("projet_app:home")

        if not file:
            messages.add_message(request, messages.ERROR, 'Veuillez envoyez un fichier SVP')
            return redirect("projet_app:home")

        elif not file.name.lower().endswith(".pdf"):
            messages.add_message(request, messages.ERROR, 'Votre fichier doit être en format PDF')
            return redirect("projet_app:home")

        if translators.strip() == "":
            messages.add_message(request, messages.ERROR, 'Veuillez choisir au moins un traducteur svp')
            return redirect("projet_app:home")

        translator_list = translators.strip().split(" ")

        try:
            for translator in translator_list:
                trans_req = TranslationRequest()
                trans_req.full_name = "{} {}".format(family_name.upper(), first_name.title())
                trans_req.email = email
                trans_req.phone_number = phone
                trans_req.address = address
                trans_req.translator = UserProfile.objects.filter(slug=translator)[0].translator_profile
                trans_req.src_language = Language.objects.filter(name=src_lang)[0]
                trans_req.dest_language = Language.objects.filter(name=dest_lang)[0]
                trans_req.category = TranslationCategory.objects.filter(name=category)[0]
                trans_req.notes = notes
                trans_req.file = file
                trans_req.requester = request.user.profile
                trans_req.save()

        except Exception:
            messages.add_message(request, messages.ERROR, "Il semblerait qu'une erreur se soit produite")
        else:
            messages.add_message(request, messages.SUCCESS, 'Votre demande a été effectuée avec succès')
        return redirect("projet_app:home")

class RecruitTranslator(View):
    def get(self,request):
        return render(request,"recruit.html",{"form":AddTranslatorForm()})

    def post(self,request):
        new_form = AddTranslatorForm(request.POST,request.FILES)

        if new_form.is_valid():
            if len(new_form.cleaned_data['languages'])==1:
                messages.add_message(request, messages.ERROR,
                                     'Attention: Un traducteur doit maîtriser plus d\'une seule langue!' )
                return render(request, "recruit.html", {"form": new_form})
            user = User()
            user.username = new_form.cleaned_data['email']
            user.set_password(new_form.cleaned_data['password'])
            try:
                user.save()
            except IntegrityError:
                messages.add_message(request, messages.ERROR, 'Cet utilisateur existe déja. Veuillez prendre un autre email')
                return render(request, "recruit.html",{"form":new_form})

            profile = UserProfile()
            profile.phone_number = new_form.cleaned_data['phone']
            profile.full_name = "{} {}".format(new_form.cleaned_data['family_name'].upper(),
                                               new_form.cleaned_data['first_name'].title())
            profile.address = new_form.cleaned_data['address']
            profile.user = user
            profile.wilaya = new_form.cleaned_data["wilaya"]
            profile.commune = new_form.cleaned_data["commune"]
            profile.save()

            translator_profile = TranslatorProfile()
            translator_profile.user_profile = profile
            translator_profile.save()
            for i in new_form.cleaned_data["languages"]:
                translator_profile.languages.add(i)
            for i in new_form.cleaned_data["categories"]:
                translator_profile.categories.add(i)
            translator_profile.cv = new_form.files.get("cv",None)
            if new_form.files.get("assermented_file",None):
                translator_profile.is_assermented=True
                translator_profile.assermented_file = new_form.files.get("assermented_file",None)
            else :
                translator_profile.is_assermented= False
            for i in ['ref1','ref2','ref3']:
                if new_form.files.get(i,None):
                    file_r = ReferenceFile()
                    file_r.translator = translator_profile
                    file_r.file = new_form.files.get(i,None)
                    file_r.save()
            translator_profile.save()
            login(request, user)
            return redirect("projet_app:home")
        else:
            messages.add_message(request, messages.ERROR,
                                 'Merci de bien vouloir corriger les errueres signalées')
            return render(request,"recruit.html", {'form': new_form})

class AllTranslatorTransactions(View,LoginRequiredMixin):
    def get(self,request):
        try:
            translations_requests = request.user.profile.translator_profile.translation_requests.filter(treated=False).order_by("-request_date")
        except:
            return render(request,"forbidden_request_detail.html")
        return render(request,"translator_transactions.html",{'requests':translations_requests})



class AllClientTransactions(View,LoginRequiredMixin):
    def get(self,request):
        qs = Q()
        qs &=Q(request__requester=request.user.profile)
        qs &= Q(accepted=False)
        qs &= Q(treated=False)
        offers = TranslationOffer.objects.filter(qs).order_by("-offer_date")

        return render(request,"client_transactions.html",{"offers":offers})

class TranslationRequestDetails(View,LoginRequiredMixin):
    def get(self,request,pk):
        trans_req = TranslationRequest.objects.filter(pk=pk)[0]
        try:
            if not request.user.profile.translator_profile == trans_req.translator:
                return render(request, "forbidden_request_detail.html")
        except:
            return render(request, "forbidden_request_detail.html")
        if trans_req.treated:
            return render(request, "forbidden_request_detail.html")
        return render(request, "request_detail.html",{"request":trans_req,"form":TranslationOfferForm()})

    def post(self,request,pk):
        offer_form = TranslationOfferForm(request.POST)
        if offer_form.is_valid():
            offer = TranslationOffer()
            tra_request =  TranslationRequest.objects.filter(pk=pk)[0]
            offer.request = tra_request
            tra_request.treated = True
            tra_request.save()
            offer.after_price = offer_form.cleaned_data["price"]
            offer.accept_price = offer_form.cleaned_data["accept_price"] if offer_form.cleaned_data["accept_price"] else 0
            offer.notes = offer_form.cleaned_data["notes"]
            offer.save()
            messages.add_message(request, messages.SUCCESS, 'Opération réussie!')
            return redirect("projet_app:translator_transactions")
        else:
            return render(request, "request_detail.html", {"request": trans_req, "form": offer_form})

class RefuseOffer(View,LoginRequiredMixin):
    def get(self,request,pk):
        trans_req = TranslationRequest.objects.filter(pk=pk)[0]
        try:
            if not request.user.profile.translator_profile == trans_req.translator:
                return render(request, "forbidden_request_detail.html")
        except:
            return render(request, "forbidden_request_detail.html")
        if trans_req.treated:
            return render(request, "forbidden_request_detail.html")
        trans_req.treated = True
        trans_req.save()
        messages.add_message(request, messages.SUCCESS, 'Opération réussie!')
        return redirect("projet_app:translator_transactions")

class ClientAccept(View,LoginRequiredMixin):
    def get(self,request,pk):
        offer = TranslationOffer.objects.filter(pk=pk)[0]
        if offer.treated or offer.accepted:
            return render(request, "forbidden_request_detail.html")
        if offer.request.requester != request.user.profile:
            return render(request, "forbidden_request_detail.html")
        offer.accepted=True
        messages.add_message(request, messages.SUCCESS, 'Opération réussie!')
        offer.accept_offer_date = timezone.now()
        offer.save()
        return redirect("projet_app:client_transactions")

class ClientRefuse(View,LoginRequiredMixin):
    def get(self,request,pk):
        offer = TranslationOffer.objects.filter(pk=pk)[0]
        if offer.treated or offer.accepted:
            return render(request, "forbidden_request_detail.html")
        if offer.request.requester != request.user.profile:
            return render(request, "forbidden_request_detail.html")
        offer.treated=True
        messages.add_message(request, messages.SUCCESS, 'Opération réussie!')
        offer.save()
        return redirect("projet_app:client_transactions")