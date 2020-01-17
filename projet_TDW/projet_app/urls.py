from django.conf.urls import url
from . import views

app_name = "projet_app"

urlpatterns = [

    #those are for AJAX and forms stuff
    url(r"^select-translators$",views.TranslatorsSelect.as_view(),name="select_translator"),
    url(r"^logout",views.Logout.as_view(),name="logout"),
    url(r"^login",views.Login.as_view(),name="login"),
    url(r"^register",views.Register.as_view(),name="register"),
    url(r"^send-request",views.SendRequest.as_view(),name="send_request"),

    #those are for our pages
    url(r'my-profile$',views.HomeView.as_view(),name="my profile"),
    url(r'profiles/(?P<slug>[\w\d-]+)$',views.HomeView.as_view(),name="profile"),
    url(r'translator-recruit$',views.RecruitTranslator.as_view(),name="recruit"),
    url(r"a-propos$",views.HomeView.as_view(),name="a propos"),
    url(r"translators$",views.HomeView.as_view(),name="translators"),
    url(r"translation-types$",views.HomeView.as_view(),name="types"),
    url(r"^$",views.HomeView.as_view(),name="home"),


]
