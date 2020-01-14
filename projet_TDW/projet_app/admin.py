from django.contrib import admin
from .models import UserProfile,ReferenceFile, Language, TranslationCategory, TranslatorProfile, Rate, Warn, TranslationRequest, TranslationOffer, TranslationResponse

admin.site.register([UserProfile,Language, ReferenceFile, TranslationRequest,TranslatorProfile,TranslationCategory,Rate,Warn,TranslationOffer,TranslationResponse])

# Register your models here.
