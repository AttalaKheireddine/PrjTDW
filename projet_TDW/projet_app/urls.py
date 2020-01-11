from django.conf.urls import url
from . import views

app_name = "projet_app"

urlpatterns = [
    url(r'my-profile',),
    url(r'/profiles/(?P<slug>[\w\d-]+)/$',),
    url(r'translator-recruit',),
    url(r"a-propos"),
    url(r"")
]
