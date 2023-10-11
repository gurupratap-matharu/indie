from django.urls import path

from . import views

app_name = "pages"

urlpatterns = [
    path("", views.HomePageView.as_view(), name="home"),
    path("about/", views.AboutPageView.as_view(), name="about"),
    path("terms/", views.TermsPageView.as_view(), name="terms"),
    path("privacy/", views.PrivacyPageView.as_view(), name="privacy"),
    path("favicon.ico", views.favicon, name="favicon"),
    path("robots.txt", views.RobotsTxtView.as_view(), name="robots"),
]
