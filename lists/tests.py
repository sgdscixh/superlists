""" dummy test """
from django.test import TestCase
from django.urls import resolve


from lists.views import home_page
from lists.models import Item


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

    def test_only_saves_items_when_necessary(self):
        """test only saves items when necessary"""
        self.client.get("/")
        self.assertEqual(Item.objects.count(), 0)

    def test_can_save_post_request(self):
        """test can save post request"""

        self.client.post("/", data={"item_text": "A new list item"})

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, "A new list item")

    def test_redirects_after_post(self):
        """test redirects after post"""

        response = self.client.post("/", data={"item_text": "A new list item"})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response["location"], "/")

    def test_displays_muilt_list_items(self):
        """mutiple list items"""
        Item.objects.create(text="itemey 1")
        Item.objects.create(text="itemey 2")

        response = self.client.get("/")
        self.assertIn("itemey 1", response.content.decode())
        self.assertIn("itemey 2", response.content.decode())


class ItemModelTest(TestCase):
    """test item model"""

    def test_saving_and_retrieving_items(self):
        """test saving and retrieving items"""
        first_item = Item()
        first_item.text = "The first (ever) list item"
        first_item.save()

        second_item = Item()
        second_item.text = "Item the second"
        second_item.save()

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, "The first (ever) list item")
        self.assertEqual(second_saved_item.text, "Item the second")
