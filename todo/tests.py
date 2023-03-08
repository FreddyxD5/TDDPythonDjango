from django.test import TestCase
from django.urls import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string

from todo.views import home_page
# Create your tests here.

class SmokeTest(TestCase):
    def test_bad_maths(self):
        self.assertEqual(1+1,2)


class HomePageTest(TestCase):
    
    def test_home_page_return_correct_html(self):        
        response = self.client.get('/')
        html = response.content.decode('utf-8')        
        expected_html = render_to_string('todo/home.html')        
        self.assertEqual(html, expected_html)
        self.assertTrue(html.startswith('<!DOCTYPE html>'))
        self.assertIn('<title>To-Do lists</title>',html)
        self.assertTrue(html.endswith('</html>'))        

    def test_uses_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'todo/home.html')

    
        
        
        