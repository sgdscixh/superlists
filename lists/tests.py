""" dummy test """
from django.test import TestCase
from django.urls import resolve
from lists.views import home_page


class SmokeTest(TestCase):
    """dummy test"""

    def test_bad_maths(self):
        """dummy test"""
        self.assertEqual(1 + 2, 3)


class HomePageTest(TestCase):
    """test home page"""

    def test_root_url_resolves_to_home_page_view(self):
        """test home page root url"""
        found = resolve("/")
        self.assertEqual(found.func, home_page)

    # def test_uses_home_template(self):
    #     """test home page"""
    #     response = self.client.get("/")
    #     self.assertTemplateUsed(response, "home.html")
