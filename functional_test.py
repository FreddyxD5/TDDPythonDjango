import time
import unittest

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By


# browser = webdriver.Edge()
# browser.get('http://localhost:8000')

# assert 'install' in browser.title


class NewVisitorTest(unittest.TestCase):
    """
    New Visitor Test
    """
    def setUp(self):
        self.browser = webdriver.Edge()

    def tearDown(self):
        self.browser.quit()

    def check_for_row_in_list_table(self, row_text):
        """
        Verifica todos los textos dentro del table
        """
        table = self.browser.find_element(By.ID, 'id_list_table')
        rows = table.find_elements(By.TAG_NAME, 'tr')
        self.assertIn(row_text, [row.text for row in rows])

    def test_can_start_a_list_and_retrieve_it_later(self):
        """
        Test para ver los items del html
        """
        self.browser.get('http://localhost:8000')
        #Ella se da cuenta que el titulo de la pagina y el header
        #mencionan To-Do List
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element(By.TAG_NAME, "h1")
        self.assertIn('To-Do', header_text.text)
        #Es invitada a entrar a to-do item directamente
        inputbox  = self.browser.find_element(By.ID, 'id_new_item')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter a to-do item'
        )
        #El usuario tipea "Buy peacock feathers" dentro del cuadro de texto,(El hobby
        # de su amigo esta tipeando fly-fishinf lures)

        #El usuario presiona enter, la pagina se actualiza y ahora
        #la pagina muestra una lista,
        # "1: Buy peacokc feathers" como un item en una tabla de to-do
        time.sleep(5)
        inputbox.send_keys('Buy peacock feathers')
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)
        self.check_for_row_in_list_table('1: Buy peacock feathers')
        #Hay otro text box invitando a que ingrese otro valor
        #Enter another item
        inputbox = self.browser.find_element(By.ID, 'id_new_item')
        inputbox.send_keys('Use peacock feathers to make a fly')
        inputbox.send_keys(Keys.ENTER)
        time.sleep(5)
        self.check_for_row_in_list_table('1: Buy peacock feathers')
        self.check_for_row_in_list_table('2: Use peacock feathers to make a fly')
        self.fail('Finish the TEST!!!!!!!!!')
        #La pagina se actualiza de nuevo :D

if __name__ == '__main__':
    unittest.main(warnings='ignore')
