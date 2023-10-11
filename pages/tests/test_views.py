from http import HTTPStatus

from django.test import SimpleTestCase, tag
from django.urls import resolve, reverse

from pages.views import (
    AboutPageView,
    HomePageView,
    PrivacyPageView,
    RobotsTxtView,
    TermsPageView,
)


@tag("pages", "fast")
class HomePageTests(SimpleTestCase):
    """
    Test suite for the main home page or our awesome site.
    """

    def setUp(self):
        self.url = reverse("pages:home")
        self.response = self.client.get(self.url)
        self.template_name = "pages/home.html"

    def test_homepage_works(self):
        self.assertEqual(self.response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(self.response, self.template_name)
        self.assertContains(self.response, "Indie")
        self.assertNotContains(self.response, "Hi there! I should not be on this page.")

    def test_homepage_url_resolves_homepageview(self):
        view = resolve(self.url)
        self.assertEqual(view.func.__name__, HomePageView.as_view().__name__)


@tag("pages", "fast")
class AboutPageTests(SimpleTestCase):
    def setUp(self):
        self.url = reverse("pages:about")
        self.response = self.client.get(self.url)
        self.template_name = "pages/about.html"

    def test_aboutpage_status_code(self):
        self.assertEqual(self.response.status_code, HTTPStatus.OK)

    def test_aboutpage_renders_correct_template(self):
        self.assertTemplateUsed(self.response, self.template_name)

    def test_aboutpage_contains_correct_html(self):
        self.assertContains(self.response, "About")

    def test_aboutpage_does_not_contain_incorrect_html(self):
        self.assertNotContains(self.response, "Hi there! I should not be on this page.")

    def test_aboutpage_url_resolves_aboutpageview(self):
        view = resolve(self.url)
        self.assertEqual(view.func.__name__, AboutPageView.as_view().__name__)


@tag("pages", "fast")
class TermsPageTests(SimpleTestCase):
    def setUp(self):
        self.url = reverse("pages:terms")
        self.response = self.client.get(self.url)
        self.template_name = "pages/terms.html"

    def test_termspage_status_code(self):
        self.assertEqual(self.response.status_code, HTTPStatus.OK)

    def test_termspage_renders_correct_template(self):
        self.assertTemplateUsed(self.response, self.template_name)

    def test_termspage_contains_correct_html(self):
        self.assertContains(self.response, "Terms")

    def test_termspage_does_not_contain_incorrect_html(self):
        self.assertNotContains(self.response, "Hi I should not be on this page!")

    def test_termspage_url_resolves_termspageview(self):
        view = resolve(self.url)
        self.assertEqual(view.func.__name__, TermsPageView.as_view().__name__)


@tag("pages", "fast")
class PrivacyPageTests(SimpleTestCase):
    def setUp(self):
        self.url = reverse("pages:privacy")
        self.response = self.client.get(self.url)
        self.template_name = "pages/privacy.html"

    def test_privacy_page_status_code(self):
        self.assertEqual(self.response.status_code, HTTPStatus.OK)

    def test_privacy_page_renders_correct_template(self):
        self.assertTemplateUsed(self.response, self.template_name)

    def test_privacy_page_contains_correct_html(self):
        self.assertContains(self.response, "Privacy")

    def test_privacy_page_does_not_contain_incorrect_html(self):
        self.assertNotContains(self.response, "Hi I should not be on this page!")

    def test_privacy_page_url_resolves_privacypageview(self):
        view = resolve(self.url)
        self.assertEqual(view.func.__name__, PrivacyPageView.as_view().__name__)


class RobotsTxtTests(SimpleTestCase):
    def setUp(self):
        self.url = reverse("pages:robots")
        self.template_name = "robots.txt"

    def test_robots_txt_works_correctly(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, self.template_name)
        self.assertNotContains(response, "Hi I should not be on this page")
        self.assertEqual(response["content-type"], "text/plain")
        self.assertTrue(response.content.startswith(b"User-Agent: *\n"))

    def test_post_disallowed_for_robots_txt(self):
        response = self.client.post(self.url)

        self.assertEqual(response.status_code, HTTPStatus.METHOD_NOT_ALLOWED)

    def test_robots_txt_url_resolves_correct_view(self):
        view = resolve(self.url)
        self.assertEqual(view.func.__name__, RobotsTxtView.as_view().__name__)


class FaviconTests(SimpleTestCase):
    def test_get(self):
        response = self.client.get("/favicon.ico")

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response["Cache-Control"], "max-age=86400, immutable, public")
        self.assertGreater(len(response.getvalue()), 0)
