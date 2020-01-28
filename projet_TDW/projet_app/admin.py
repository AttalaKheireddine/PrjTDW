from django.contrib import admin
from .models import UserProfile,ReferenceFile, Language, TranslationCategory, TranslatorProfile, Rate, Warn, TranslationRequest, TranslationOffer, TranslationResponse,Article
from .forms import ChartForm
#admin.site.register([UserProfile,Language, ReferenceFile, TranslationRequest,TranslatorProfile,TranslationCategory,Rate,Warn,TranslationOffer,TranslationResponse,Article])



from django.template.response import TemplateResponse
from django.urls import path

class MyAdminSite(admin.AdminSite):
    index_template = "ADMIN.html"
    site_header = "Translate Admin"
    site_title = "Translate"
    def each_context(self, request):
        return {"form":ChartForm()}

class RequestsInline(admin.TabularInline):
    model = TranslationRequest
    ordering = ("-request_date",)
# Register your models here.

class ProfileAdmin(admin.ModelAdmin):
    #list_filter =
    search_fields = ["full_name","wilaya"]
    list_display = ["full_name","wilaya","commune","phone_number"]
    sortable_by = list_display[:3]
    inlines = [RequestsInline]

class TranslatorAdmin(admin.ModelAdmin):
    #search_fields = ["user_profile__full_name", "user_profile__wilaya"]
    #list_display = ["user_profile__full_name", "user_profile__wilaya", "user_profile__commune", "user_profile__phone_number"]
    #sortable_by = ["user_profile__full_name", "user_profile__wilaya", "user_profile__commune","number_of_translations"]
    inlines = [RequestsInline]

class RequestAdmin(admin.ModelAdmin):
    pass

class ResponseAdmin(admin.ModelAdmin):
    pass



admin_site = MyAdminSite(name='myadmin')
admin_site.register(UserProfile,ProfileAdmin)
admin_site.register(TranslatorProfile,TranslatorAdmin)
admin_site.register(TranslationRequest,RequestAdmin)
admin_site.register(TranslationResponse,ResponseAdmin)


