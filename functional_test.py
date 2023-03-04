from selenium import webdriver
import unittest
# browser = webdriver.Edge()
# browser.get('http://localhost:8000')

# assert 'install' in browser.title


class NewVisitorTest(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Edge()

    def tearDown(self):
        self.browser.quit()
    
    def test_can_start_a_list_and_retrieve_it_later(self):
        self.browser.get('http://localhost:8000')
        #Ella se da cuenta que el titulo de la pagina y el header
        #mencionan To-Do List
        self.assertIn('To-DOOOOOO', self.browser.title)
        self.fail('Test Acabado!')

        #Es invitada a entrar a to-do item directamente
        # [...rest of comments as before]

if __name__ == '__main__':
    unittest.main(warnings='ignore')

