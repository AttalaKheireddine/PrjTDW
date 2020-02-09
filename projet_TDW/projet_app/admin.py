from django.contrib import admin
from .models import UserProfile,ReferenceFile, Language, TranslationCategory,Notification, TranslatorProfile, Rate, Warn, TranslationRequest, TranslationOffer, TranslationResponse,Article
from .forms import ChartForm
# admin.site.register([UserProfile,Language, ReferenceFile, TranslationRequest,TranslatorProfile,TranslationCategory,Rate,Warn,TranslationOffer,TranslationResponse,Article])
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render


from django.template.response import TemplateResponse
from django.urls import path


class MyAdminSite(admin.AdminSite):
    index_template = "ADMIN.html"
    site_header = "Translate Admin"
    site_title = "Translate"
    # login_form = AuthenticationForm
    # login_template = super(*args,**kwargs).login_template


    def index(self, request, extra_context={"form":ChartForm()}):
        return super(MyAdminSite, self).index(request, extra_context)
        return render(request, self.index_template, dict(self.each_context(request), **extra_context))


class RequestsInline(admin.TabularInline):
    model = TranslationRequest
    ordering = ("-request_date",)


class ProfileAdmin(admin.ModelAdmin):
    # list_filter =
    search_fields = ["full_name", "wilaya"]
    list_display = ["full_name", "wilaya", "commune", "phone_number"]
    sortable_by = list_display[:3]
    inlines = [RequestsInline]


class TranslatorAdmin(admin.ModelAdmin):
    inlines = [RequestsInline]


class RequestAdmin(admin.ModelAdmin):
    pass


class ResponseAdmin(admin.ModelAdmin):
    pass


admin_site = MyAdminSite(name='myadmin')
admin_site.register(UserProfile, ProfileAdmin)
admin_site.register(TranslatorProfile, TranslatorAdmin)
admin_site.register(TranslationRequest, RequestAdmin)
admin_site.register(TranslationResponse, ResponseAdmin)
admin_site.register(Notification)
