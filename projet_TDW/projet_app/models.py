from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_save
from random import randrange
from django.template.defaultfilters import slugify
from django.core.validators import MaxValueValidator, MinValueValidator
import os

# Create your models here.

# helper functions for handling media file names


def response_file_naming(instance, filename):
    path = "translation-responses/"
    format_ = instance.pk+".pdf"
    return os.path.join(path, format_)


def request_file_naming(instance, filename):
    path = "translation-requests/"
    format_ = instance.pk+".pdf"
    return os.path.join(path, format_)


def cv_file_naming(instance, filename):
    path = "cv-files/"
    format_ = instance.pk + ".pdf"
    return os.path.join(path, format_)


def reference_file_naming(instance, filename):
    path = "cv-files/"
    format_ = instance.pk + ".pdf"
    return os.path.join(path, format_)


def profile_pic_naming(instance, filename):
    path = "cv-files/"
    fn, file_extension = os.path.splitext(filename)
    format_ = instance.pk + file_extension
    return os.path.join(path, format_)


# models
class UserProfile(models.Model):

    full_name = models.CharField(max_length=60, blank=False, null=False)
    address = models.CharField(max_length=100, blank=True, null=False)
    phone_number = models.CharField(max_length=15)
    slug = models.SlugField(unique=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to=profile_pic_naming)

    def __str__(self):
        return self.slug


def create_slug(instance, new_slug=None):
    slug = new_slug if new_slug is not None else slugify(instance.full_name)
    exists=UserProfile.objects.filter(slug=slug).exists()
    if exists():
        new_slug = "{}-{}".format(slug, str(randrange(1, 100)))
        return create_slug(instance, new_slug)
    return slug


def pre_save_profile_receiver(sender, instance, *args, **kwargs):
    if not instance.slug():
        instance.slug = create_slug(instance)
# each time we save a user profile we will run this function


pre_save.connect(pre_save_profile_receiver, sender=UserProfile)


class Language(models.Model):
    name = models.CharField(max_length=80, unique=True)


class TranslationCategory(models.Model):
    name = models.CharField(max_length=80, unique=True)


class TranslatorProfile (models.Model):
    number_of_translations = models.IntegerField(default=0)
    languages = models.ManyToManyField(Language)
    categories = models.ManyToManyField(TranslationCategory)
    cv = models.FileField(upload_to=cv_file_naming)
    is_assermented = models.BooleanField(default=False)
    assermented_file = models.FileField(upload_to=request_file_naming)


class ReferenceFile(models.Model):
    translator = models.ForeignKey(TranslatorProfile, on_delete=models.CASCADE)
    file = models.FileField(upload_to="""put sth here father mocker""")


class Rate(models.Model):
    rate = models.IntegerField()
    rater = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    translator = models.ForeignKey(TranslatorProfile, on_delete=models.CASCADE)


class Warn (models.Model):
    warn_text = models.TextField()
    warner = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    translator = models.ForeignKey(TranslatorProfile, on_delete=models.CASCADE)


class TranslationRequest (models.Model):
    full_name = models.CharField(max_length=60, blank=False, null=False)
    address = models.CharField(max_length=100, blank=True, null=False)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField()
    translators = models.ManyToManyField(TranslatorProfile)
    treated = models.BooleanField(default=False)
    notes = models.TextField(blank=True)


class TranslationOffer (models.Model):
    request = models.ForeignKey(TranslationRequest, on_delete=models.CASCADE)
    accept_price = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(100000)],
    )
    full_price = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(1000000000)],
    )
    treated = models.BooleanField(default=False)
    accepted = models.BooleanField(default=False)
    notes = models.TextField(blank=True)


class TranslationResponse(models.Model):
    offer = models.ForeignKey(TranslationOffer, on_delete=models.CASCADE)
    file = models.FileField(upload_to=response_file_naming)
    done = models.BooleanField(default=False)