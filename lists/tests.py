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


class HomePageTest2(TestCase):
    """test home page use reverse"""

    def test_root_url_reverse_to_home_page_view(self):
        """test home page root url"""
        from django.urls import reverse  # reverse name to url

        home_url = reverse("home")
        found = resolve(home_url)
        self.assertEqual(found.func, home_page)
