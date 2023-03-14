"""
Unit test to todo application
"""
from django.test import TestCase
# from django.template.loader import render_to_string
# from todo.views import home_page
from todo.models import Item, List


# class SmokeTest(TestCase):
#     """
#     Smoke Test
#     """

#     def test_bad_maths(self):
#         """
#         test
#         """
#         self.assertEqual(1+1,2)


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
        self.client.post('/lists/new', data={'item_text':'A new list item'})
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item')

    def test_redirects_after_post(self):
        """
        smht
        """
        response = self.client.post('/lists/new', data={'item_text':'A new list item'})
        self.assertEqual(response.status_code, 302)
        new_list = List.objects.first()
        self.assertEqual(response['location'],f'/lists/{new_list.id}')


class ListViewTest(TestCase):
    """
    liststest
    """
    def test_use_list_template(self):
        response = self.client.get('/lists/the-only-list-in-the-world/')
        self.assertTemplateUsed(response,'todo/list.html')

    def test_display_only_items_for_that_list(self):
        """
        Test que muestra Todos los  items de la lista a la que fue asociada
        """
        correct_list = List.objects.create()
        Item.objects.create(text='itemey 1', list = correct_list)
        Item.objects.create(text='itemey 2', list = correct_list)
        other_list = List.objects.create()
        Item.objects.create(text='other list item 1', list = other_list)
        Item.objects.create(text='other list item 2', list = other_list)        

        response = self.client.get(f'/lists/{correct_list.id}')

        self.assertContains(response, 'itemey 1')
        self.assertContains(response, 'itemey 2')
        self.assertNotContains(response, 'other list item 1')
        self.assertNotContains(response, 'other list item 2')
    
    def test_passes_correct_list_to_template(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()
        response = self.client.get(f'/lists/{correct_list.id}')
        self.assertEqual(response.context['list'], correct_list)

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


class NewListTest(TestCase):
    """
    Lista nueva de items
    """
    def test_can_save_a_post_request(self):
        self.client.post('/lists/new', data={'item_text':'A new list item'})
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item')

    def test_redirects_after_post(self):
        response = self.client.post('/lists/new', data={'item_text':'A new list item'})
        new_list = List.objects.first()
        self.assertRedirects(response,f"/lists/{new_list.id}")

class NewItemTest(TestCase):
    """
    Nuevo item para una lista pre definida
    """

    def test_can_save_a_post_request_to_an_existing_list(self):
        """
            La ruta puede guardar un nuevo item a una lista existente
        """
        other_list = List.objects.create()
        correct_list = List.objects.create()

        self.client.post(
            f"/lists/{correct_list.id}/add_item/",
            data={'item_text':'A new item for an existing list|can_save'}
            )        
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first() 
        self.assertEqual(new_item.text, 'A new item for an existing list|can_save')
        self.assertEqual(new_item.list, correct_list)

    def test_redirects_to_list_view(self):
        """
        Test para redireccionar a la lista de items
        """
        other_list = List.objects.create()
        correct_list = List.objects.create()

        response = self.client.post(
            f"/lists/{correct_list.id}/add_item/",
            data={'item_text':'A new item for an existing list|redirects'}
        )
        self.assertRedirects(response, f"/lists/{correct_list.id}")
