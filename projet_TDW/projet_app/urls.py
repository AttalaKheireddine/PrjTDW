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
    url(r"^translator-transactions/(?P<pk>[\d]+)/refuse$", views.RefuseOffer.as_view(), name="refuse_request"),
    url(r"treat-response//(?P<pk>[\d]+)$",views.TreatResponse.as_view(),name="treat_response"),
    url(r"profiles/(?P<slug>[\w\d-]+)/report$",views.Report.as_view(),name="report"),
    url(r"profiles/(?P<slug>[\w\d-]+)/rate$",views.RateView.as_view(),name="rate"),

    #those are for our pages
    url(r'my-profile$',views.HomeView.as_view(),name="my profile"),
    url(r'profiles/(?P<slug>[\w\d-]+)$',views.UserProfileView.as_view(),name="profile"),
    url(r'translator-recruit$',views.RecruitTranslator.as_view(),name="recruit"),
    url(r"a-propos$",views.About.as_view(),name="about"),
    url(r"translators$",views.HomeView.as_view(),name="translators"),
    url(r"translation-types$",views.HomeView.as_view(),name="types"),
    url(r"^$",views.HomeView.as_view(),name="home"),
    url(r"^translator-transactions$",views.AllTranslatorTransactions.as_view(),name="translator_transactions"),
    url(r"^translator-transactions/(?P<pk>[\d]+)$",views.TranslationRequestDetails.as_view(),name="request_details"),
    url(r"^client-transactions$",views.AllClientTransactions.as_view(),name="client_transactions"),
    url(r"^client-transactions/(?P<pk>[\d]+)/accept$",views.ClientAccept.as_view(),name="client_accept"),
    url(r"^client-transactions/(?P<pk>[\d]+)/refuse$",views.ClientRefuse.as_view(),name="client_refuse"),
    url(r"blogs$",views.Blogs.as_view(),name="blogs"),
    url(r"blog/(?P<pk>[\d]+)$",views.BlogDetail.as_view(),name="blog_detail")
]
