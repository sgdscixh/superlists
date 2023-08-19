""" dummy test """
from django.test import TestCase
from django.urls import resolve
from django.http import HttpRequest

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

    def test_home_page_returns_correct_html(self):
        """test home page html use django client"""

        response = self.client.get("/")
        html = response.content.decode("utf8")
        self.assertTrue(html.startswith("<html>"))
        self.assertIn("<title>To-Do lists</title>", html)
        self.assertTrue(html.strip().endswith("</html>"))


class HomePageTest2(TestCase):
    """test home page use reverse"""

    def test_root_url_reverse_to_home_page_view(self):
        """test home page root url"""
        from django.urls import reverse  # reverse name to url

        home_url = reverse("home")
        found = resolve(home_url)
        self.assertEqual(found.func, home_page)

    def test_home_page_returns_correct_html(self):
        """test home page html"""
        request = HttpRequest()  # 用户请求网页时，django看到的是HttpRequest对象
        response = home_page(request)
        html = response.content.decode("utf8")
        self.assertTrue(html.startswith("<html>"))
        self.assertIn("<title>To-Do lists</title>", html)
        self.assertTrue(html.strip().endswith("</html>"))

    def test_home_page_returns_correct_html2(self):
        """test home page html use render_to_string"""

        from django.template.loader import render_to_string

        request = HttpRequest()
        response = home_page(request)
        html = response.content.decode("utf8")
        expected_html = render_to_string("home.html")
        self.assertEqual(html, expected_html)
