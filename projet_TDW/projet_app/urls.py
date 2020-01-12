from django.conf.urls import url
from . import views

app_name = "projet_app"

urlpatterns = [
    url(r'my-profile$',views.home,name="my profile"),
    url(r'profiles/(?P<slug>[\w\d-]+)$',views.home,name="profile"),
    url(r'translator-recruit$',views.home,name="recruit"),
    url(r"a-propos$",views.home,name="a propos"),
    url(r"translators$",views.home,name="translators"),
    url(r"translation-types$",views.home,name="types"),
    url(r"^$",views.home,name="home")
]
