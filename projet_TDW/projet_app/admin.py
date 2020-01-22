from django.contrib import admin
from .models import UserProfile,ReferenceFile, Language, TranslationCategory, TranslatorProfile, Rate, Warn, TranslationRequest, TranslationOffer, TranslationResponse,Article

admin.site.register([UserProfile,Language, ReferenceFile, TranslationRequest,TranslatorProfile,TranslationCategory,Rate,Warn,TranslationOffer,TranslationResponse,Article])

# Register your models here.
