from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

import time
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
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element(By.TAG_NAME, "h1").text
        
        self.assertIn('To-Do', header_text)        

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
        inputbox.send_keys('Buy peacock feathers')
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)

        table = self.browser.find_element(By.ID, 'id_list_table')
        rows = table.find_elements(By.TAG_NAME, 'tr')

        self.assertTrue(
            any(row.text == '1: Buy peacock feathers' for row in rows)
            )
        #Aun hay una caja de texto invitando a agregar otro item
        # Se ingresa "Use peacock feathers to make a fly" (Ediths is very
        # methodical)
        self.fail('Finish the TEST!!!!!!!!!')
        #La pagina se actualiza de nuevo :D

if __name__ == '__main__':
    unittest.main(warnings='ignore')

