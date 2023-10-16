from django.urls import path

from . import views

app_name = "pages"

urlpatterns = [
    path("", views.HomePageView.as_view(), name="home"),
    path("about/", views.AboutPageView.as_view(), name="about"),
    path("terms/", views.TermsPageView.as_view(), name="terms"),
    path("get-listed/", views.GetListedView.as_view(), name="get-listed"),
    path("help/", views.HelpPageView.as_view(), name="help"),
    path("privacy/", views.PrivacyPageView.as_view(), name="privacy"),
    path("sitemap/", views.SiteMapPageView.as_view(), name="sitemap"),
    path("contact/", views.ContactPageView.as_view(), name="contact"),
    path("feedback/", views.FeedbackPageView.as_view(), name="feedback"),
    path("favicon.ico", views.favicon, name="favicon"),
    path("robots.txt", views.RobotsTxtView.as_view(), name="robots"),
]
