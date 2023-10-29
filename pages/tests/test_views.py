from http import HTTPStatus

from django.contrib.messages import get_messages
from django.core import mail
from django.test import SimpleTestCase, TestCase, tag
from django.urls import resolve, reverse

from pages.forms import ContactForm, FeedbackForm
from pages.views import (
    AboutPageView,
    ContactPageView,
    FeedbackPageView,
    HomePageView,
    PrivacyPageView,
    RobotsTxtView,
    SiteMapPageView,
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


@tag("pages", "fast")
class SiteMapPageTests(SimpleTestCase):
    def setUp(self):
        self.url = reverse("pages:sitemap")
        self.response = self.client.get(self.url)
        self.template_name = "pages/sitemap.html"

    def test_sitemap_page_works(self):
        self.assertEqual(self.response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(self.response, self.template_name)
        self.assertContains(self.response, "Sitemap")
        self.assertNotContains(self.response, "Hi I should not be on this page!")

    def test_sitemap_page_url_resolves_sitemap_pageview(self):
        view = resolve(self.url)
        self.assertEqual(view.func.__name__, SiteMapPageView.as_view().__name__)


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


@tag("pages", "fast")
class ContactPageTests(TestCase):
    def setUp(self):
        self.url = reverse("pages:contact")
        self.response = self.client.get(self.url)
        self.valid_data = {
            "name": "Guest User",
            "email": "guestuser@email.com",
            "subject": "How have you been?",
            "message": "Golu this project looks great. Awesome job!!! Keep up the good work 💪",
        }

    def test_contact_page_status_code(self):
        self.assertEqual(self.response.status_code, HTTPStatus.OK)

    def test_contact_page_renders_correct_template(self):
        self.assertTemplateUsed(self.response, "pages/contact.html")

    def test_contact_page_contains_correct_html(self):
        self.assertContains(self.response, "Contact")

    def test_contact_page_does_not_contain_incorrect_html(self):
        self.assertNotContains(self.response, "Hi I should not be on this page!")

    def test_contact_page_url_resolves_contactpageview(self):
        view = resolve(self.url)
        self.assertEqual(view.func.__name__, ContactPageView.as_view().__name__)

    def test_contact_page_renders_contactform(self):
        form = self.response.context["form"]
        self.assertIsInstance(form, ContactForm)

    @tag("email")
    def test_contact_page_sends_email_for_valid_data(self):
        response = self.client.post(self.url, data=self.valid_data)

        self.assertEqual(response.status_code, HTTPStatus.FOUND)

        # Test that an email has been sent.
        # Verify that the subject of the first message is correct.
        # Check page redirected to home after success
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, self.valid_data.get("subject"))
        self.assertEqual(response["Location"], reverse("pages:home"))

        # Check that a confirmation message is included in the response
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), ContactPageView.success_message)

    @tag("messages")
    def test_contact_page_sends_valid_message_after_successul_post(self):
        response = self.client.post(self.url, data=self.valid_data)

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), ContactPageView.success_message)


@tag("pages", "fast")
class FeedbackPageTests(TestCase):
    def setUp(self):
        self.url = reverse("pages:feedback")
        self.response = self.client.get(self.url)
        self.valid_data = {
            "email": "guestuser@email.com",
            "message": "Golu this project looks great. Awesome job!!! Keep up the good work 💪",
        }

    def test_feedback_page_status_code(self):
        self.assertEqual(self.response.status_code, HTTPStatus.OK)

    def test_feedback_page_renders_correct_template(self):
        self.assertTemplateUsed(self.response, "pages/feedback.html")

    def test_feedback_page_contains_correct_html(self):
        self.assertContains(self.response, "Feedback")

    def test_feedback_page_does_not_contain_incorrect_html(self):
        self.assertNotContains(self.response, "Hi I should not be on this page!")

    def test_feedback_page_url_resolves_feedbackpageview(self):
        view = resolve(self.url)
        self.assertEqual(view.func.__name__, FeedbackPageView.as_view().__name__)

    def test_feedback_page_renders_feedbackform(self):
        form = self.response.context["form"]
        self.assertIsInstance(form, FeedbackForm)

    @tag("email")
    def test_feedback_page_sends_email_for_valid_data(self):
        response = self.client.post(self.url, data=self.valid_data)

        self.assertEqual(response.status_code, HTTPStatus.FOUND)

        # Test that an email has been sent.
        # Verify that the subject of the first message is correct.
        # Check page redirected to home after success
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, FeedbackForm.subject)
        self.assertEqual(response["Location"], reverse("pages:home"))

        # Check that a confirmation message is included in the response
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), FeedbackPageView.success_message)

    @tag("messages")
    def test_feedback_page_sends_valid_message_after_successul_post(self):
        response = self.client.post(self.url, data=self.valid_data)

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), FeedbackPageView.success_message)
