from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_save, post_save
from random import randrange
from django.template.defaultfilters import slugify
from django.core.validators import MaxValueValidator, MinValueValidator
from django.conf.global_settings import MEDIA_ROOT
from django.utils import timezone
import os
import uuid

# Create your models here.
# helper functions for handling media file names

def response_file_naming(instance, filename):
    path = "translation-responses"
    format_ = str(uuid.uuid4())+".pdf"
    return os.path.join(path, format_)


def request_file_naming(instance, filename):
    path = "translation-requests"
    format_ = str(uuid.uuid4())+".pdf"
    return os.path.join(path, format_)


def cv_file_naming(instance, filename):
    path = "cv-files"
    format_ = str(uuid.uuid4()) + ".pdf"
    return os.path.join(path, format_)


def reference_file_naming(instance, filename):
    path = "ref-files"
    format_ = str(uuid.uuid4()) + ".pdf"
    return os.path.join(path, format_)


def assermented_file_naming(instance, filename):
    path = "asermented-files"
    format_ = str(uuid.uuid4()) + ".pdf"
    return os.path.join(path, format_)


def profile_pic_naming(instance, filename):
    path = "profile-pic"
    fn, file_extension = os.path.splitext(filename)
    format_ = str(uuid.uuid4()) + file_extension
    return os.path.join(path, format_)


# models
class UserProfile(models.Model):

    full_name = models.CharField(max_length=60, blank=False, null=False)
    address = models.CharField(max_length=100, blank=True, null=False)
    phone_number = models.CharField(max_length=15)
    slug = models.SlugField(unique=True, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    profile_picture = models.ImageField(upload_to=profile_pic_naming, blank=True)
    wilaya = models.CharField(max_length=30)
    commune = models.CharField(max_length=50)

    def __str__(self):
        return self.slug


def create_slug(instance, new_slug=None):
    slug = new_slug if new_slug is not None else slugify(instance.full_name)
    exists = UserProfile.objects.filter(slug=slug).exists()
    if exists:
        new_slug = "{}-{}".format(slug, str(randrange(1, 100)))
        return create_slug(instance, new_slug)
    return slug


class Article(models.Model):
    title = models.CharField(max_length=100)
    text = models.TextField()
    date = models.DateTimeField(default=timezone.now)


class Language(models.Model):
    name = models.CharField(max_length=80, unique=True)

    def __str__(self):
        return self.name.title()


class TranslationCategory(models.Model):
    name = models.CharField(max_length=80, unique=True)
    description = models.TextField()

    def __str__(self):
        return self.name.title()

    class Meta:
        verbose_name_plural = "Categories"


class TranslatorProfile (models.Model):
    number_of_translations = models.IntegerField(default=0)
    languages = models.ManyToManyField(Language, related_name="translator")
    categories = models.ManyToManyField(TranslationCategory, related_name="translator")
    cv = models.FileField(upload_to=cv_file_naming)
    is_assermented = models.BooleanField(default=False)
    assermented_file = models.FileField(upload_to=assermented_file_naming, blank=True)
    user_profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE, related_name="translator_profile")
    global_rate = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.user_profile.slug


class ReferenceFile(models.Model):
    translator = models.ForeignKey(TranslatorProfile, on_delete=models.CASCADE,related_name="reference_files")
    file = models.FileField(upload_to=reference_file_naming)


class Rate(models.Model):
    rate = models.IntegerField()
    rater = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    translator = models.ForeignKey(TranslatorProfile, on_delete=models.CASCADE)


class Warn (models.Model):
    warn_text = models.TextField()
    warner = models.ForeignKey(UserProfile, on_delete=models.CASCADE,related_name="warns_from_set")
    warned_against = models.ForeignKey(UserProfile, on_delete=models.CASCADE,related_name="warns_against_set")
    treated = models.BooleanField(default=False)
    warn_date = models.DateTimeField(default=timezone.now)

class TranslationRequest (models.Model):
    requester = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=60, blank=False, null=False)
    address = models.CharField(max_length=100, blank=True, null=False)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField()
    translator = models.ForeignKey(TranslatorProfile, on_delete=models.CASCADE, blank=True,related_name="translation_requests")
    treated = models.BooleanField(default=False)
    notes = models.TextField(blank=True)
    file = models.FileField(upload_to=request_file_naming)
    src_language = models.ForeignKey(Language, on_delete=models.CASCADE, related_name="src_requests")
    dest_language = models.ForeignKey(Language, on_delete=models.CASCADE, related_name="dest_requests")
    category = models.ForeignKey(TranslationCategory, on_delete=models.CASCADE)
    request_date = models.DateTimeField(default=timezone.now)


class TranslationOffer (models.Model):
    request = models.ForeignKey(TranslationRequest, on_delete=models.CASCADE)
    accept_price = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(100000)],
    )
    after_price = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(1000000000)],
    )
    treated = models.BooleanField(default=False)
    accepted = models.BooleanField(default=False)
    notes = models.TextField(blank=True)
    offer_date = models.DateTimeField(default=timezone.now)
    accept_offer_date = models.DateTimeField(blank=True,null=True)


class TranslationResponse(models.Model):
    offer = models.ForeignKey(TranslationOffer, on_delete=models.CASCADE)
    file = models.FileField(upload_to=response_file_naming)
    done = models.BooleanField(default=False)
    response_date = models.DateTimeField(default=timezone.now)


def pre_save_profile_receiver(sender, instance, *args, **kwargs):
        if not instance.slug:
            instance.slug = create_slug(instance)

# each time we save a user profile we will run this function

pre_save.connect(pre_save_profile_receiver, sender=UserProfile)


def update_translator_rate(sender, instance, *args, **kwargs):
    print("__________________________________________")
    print (instance.translator.rate_set.all().aggregate(models.Avg('rate')))
    print("__________________________________________")
    instance.translator.global_rate = instance.translator.rate_set.all().aggregate(models.Avg('rate'))['rate__avg']
    instance.translator.save()


post_save.connect(update_translator_rate, sender=Rate)