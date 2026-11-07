from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class FoundationSmokeTest(TestCase):
    def test_custom_user_and_homepage(self):
        user_model = get_user_model()
        self.assertEqual(user_model._meta.label, "accounts.User")
        user = user_model.objects.create_user(username="smoke-user")
        self.assertTrue(user_model.objects.filter(pk=user.pk).exists())
        self.assertFalse(user.has_usable_password())

        response = self.client.get(reverse("home"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "home.html")
        self.assertTemplateUsed(response, "base.html")
        self.assertContains(response, "Loyiha asosi ishlayapti.")
        self.assertContains(response, "Основа проекта работает.")
        self.assertContains(response, 'href="/static/css/base.css"')
