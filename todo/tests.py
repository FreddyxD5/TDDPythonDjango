from django.test import TestCase
# from django.template.loader import render_to_string
# from todo.views import home_page
from todo.models import Item


class SmokeTest(TestCase):
    """
    Smoke Test
    """

    def test_bad_maths(self):
        """
        test
        """
        self.assertEqual(1+1,2)


class HomePageTest(TestCase):
    """
    Home page Test
    """

    def test_home_page_return_correct_html(self):
        """
        test home page
        """
        response = self.client.get('/')
        html = response.content.decode('utf-8')
        # expected_html = render_to_string('todo/home.html')
        # self.assertEqual(html, expected_html)
        self.assertTrue(html.startswith('<!DOCTYPE html>'))
        self.assertIn('<title>To-Do lists</title>', html)
        self.assertTrue(html.endswith('</html>'))

    def test_uses_home_template(self):
        """
        smth
        """
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'todo/home.html')
   
    def test_can_save_a_post_request(self):
        """
        metodo para guardar una peticion POST
        """
        response = self.client.post('/', data={'item_text':'A new list item'})
        self.assertIn('A new list item', response.content.decode())
        self.assertTemplateUsed(response, 'todo/home.html')

class ItemModelTest(TestCase):
    """
    Test to item model
    """
    def test_saving_and_retrievign_items(self):
        first_item = Item()
        first_item.text = 'The first (ever) list item'
        first_item.save()

        second_item = Item()
        second_item.text = 'Item the second'
        second_item.save()

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, 'The first (ever) list item')
        self.assertEqual(second_saved_item.text, 'Item the second')        