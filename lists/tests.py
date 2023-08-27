""" dummy test """
from django.test import TestCase

from lists.models import Item, List


class HomePageTest(TestCase):
    """test home page"""

    def test_uses_home_template(self):
        """test uses home template"""
        response = self.client.get("/")
        self.assertTemplateUsed(response, "home.html")

    def test_only_saves_items_when_necessary(self):
        """test only saves items when necessary"""
        self.client.get("/")
        self.assertEqual(Item.objects.count(), 0)


class ListViewTest(TestCase):
    """list view test"""

    def test_displys_only_items_for_that_list(self):
        """displays all items"""

        correct_list = List.objects.create()
        Item.objects.create(text="itemey 1", list=correct_list)
        Item.objects.create(text="itemey 2", list=correct_list)

        other_list = List.objects.create()
        Item.objects.create(text="other list item 1", list=other_list)
        Item.objects.create(text="other list item 2", list=other_list)

        response = self.client.get(f"/lists/{correct_list.id}/")

        self.assertContains(response, "itemey 1")
        self.assertContains(response, "itemey 2")
        self.assertNotContains(response, "other list item 1")
        self.assertNotContains(response, "other list item 2")

    def test_passes_correct_list_to_template(self):
        """test passes correct list to template"""

        other_list = List.objects.create()
        correct_list = List.objects.create()

        response = self.client.get(f"/lists/{correct_list.id}/")
        self.assertEqual(response.context["list"], correct_list)


class NewListTest(TestCase):
    """test new list"""

    def test_can_save_post_request(self):
        """test can save post request"""

        self.client.post("/lists/new", data={"item_text": "A new list item"})

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, "A new list item")

    def test_redirects_after_post(self):
        """test redirects after post"""

        response = self.client.post("/lists/new", data={"item_text": "A new list item"})
        new_list = List.objects.first()
        self.assertRedirects(response, f"/lists/{new_list.id}/")


class ItemAndListModelsTest(TestCase):
    """test item model"""

    def test_saving_and_retrieving_items(self):
        """test saving and retrieving items"""

        list_ = List()
        list_.save()

        first_item = Item()
        first_item.text = "The first (ever) list item"
        first_item.list = list_
        first_item.save()

        second_item = Item()
        second_item.text = "Item the second"
        second_item.list = list_
        second_item.save()

        saved_list = List.objects.first()
        self.assertEqual(saved_list, list_)

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, "The first (ever) list item")
        self.assertEqual(first_saved_item.list, list_)
        self.assertEqual(second_saved_item.text, "Item the second")
        self.assertEqual(second_saved_item.list, list_)


class NewItemTest(TestCase):
    """New item test"""

    def test_can_save_a_post_request_to_an_existing_list(self):
        """test can save a post request to an existing list"""

        other_list = List.objects.create()
        correct_list = List.objects.create()

        self.client.post(
            f"/lists/{correct_list.id}/add_item",
            data={"item_text": "A new item for an existing list"},
        )

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, "A new item for an existing list")
        self.assertEqual(new_item.list, correct_list)

    def test_redirects_to_list_view(self):
        """test redirects to list view"""

        other_list = List.objects.create()
        correct_list = List.objects.create()

        response = self.client.post(
            f"/lists/{correct_list.id}/add_item",
            data={"item_text": "A new item for an existing list"},
        )

        self.assertRedirects(response, f"/lists/{correct_list.id}/")
