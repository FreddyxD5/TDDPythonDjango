import os
import time
import unittest

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By



# browser = webdriver.Edge()
# browser.get('http://localhost:8000')

# assert 'install' in browser.title

MAX_WAIT = 5

class NewVisitorTest(StaticLiveServerTestCase):
    """
    New Visitor Test
    """
    def setUp(self):
        self.browser = webdriver.Edge()
        staging_server = os.environ.get('STAGING_SERVER')
        if staging_server:            
            self.live_server_url = 'http://'+staging_server

    def tearDown(self):
        # self.browser.refresh()
        self.browser.quit()

    def wait_for_row_in_list_table(self, row_text):
        """
        Verifica todos los textos dentro del table
        """
        start_time = time.time()
        while True:
            try:
                table = self.browser.find_element(By.ID, 'id_list_table')
                rows = table.find_elements(By.TAG_NAME, 'tr')
                self.assertIn(row_text, [row.text for row in rows])
                return
            except (AssertionError, WebDriverException) as error:
                if time.time() - start_time > MAX_WAIT:
                    raise error
                time.sleep(0.5)

    def test_can_start_a_list_and_retrieve_it_later(self):
        """
        Test para ver los items del html
        """
        self.browser.get(self.live_server_url)
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
        inputbox.send_keys('Buy peacock feathers')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy peacock feathers')
        #Hay otro text box invitando a que ingrese otro valor
        #Enter another item
        inputbox = self.browser.find_element(By.ID, 'id_new_item')
        inputbox.send_keys('Use peacock feathers to make a fly')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('2: Use peacock feathers to make a fly')
        self.wait_for_row_in_list_table('1: Buy peacock feathers')        
        # self.fail('Finish the TEST!!!!!!!!!')
        #La pagina se actualiza de nuevo :D

    def test_can_start_a_list_for_one_user(self):
        """
        Can start a list for one user
        """
        self.wait_for_row_in_list_table('2: Use peacock feathers to make a fly')
        self.wait_for_row_in_list_table('1: Buy a peacock feathers')

    def test_multiple_users_can_start_lists_at_different_urls(self):
        """
        Multiple users
        """
        #Edith empieza con una nueva todo lista
        self.browser.get(self.live_server_url)
        inputbox = self.browser.find_element(By.ID, 'id_new_item')
        inputbox.send_keys('Buy peacock feathers')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy peacock feathers')

        #Se da cuenta que su lista tiene un unico url
        edith_list_url = self.browser.current_url
        self.assertRegex(edith_list_url, '/lists/.+')

        #Ahora un nuevo usuario, Maby, viene al sitio
        ## Usamos una nueva session para asegurarnos que la informacion
        ## de edith esta viviendo a través de las cookies
        self.browser.quit()
        self.browser = webdriver.Edge()

        #Jose visita la pagina de inicio, Ahi no hay signos de la lista
        #de Edith
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element(By.TAG_NAME, 'body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertNotIn('make a fly', page_text)

        #Jose empieza una nueva lista insertando un nuevo item.
        # Es el menos interesante que edith
        inputbox = self.browser.find_element('id_new_item')
        inputbox.send_keys('Buy milk')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy milk')

        #Jose obtiene su propia url unica
        jose_list_url = self.browser.current_url
        self.assertRegex(jose_list_url, '/lists/.+')
        self.assertNotEqual(jose_list_url, edith_list_url)

        #De nuevo, no hay rastro de la lista de edith
        page_text = self.browser.find_element(By.TAG_NAME, 'body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertIn('Buy milk', page_text)
        #Satisfecho, ambos regresan a dormir
        
    def test_layout_and_styling(self):
        #Edith va a la pagina de inicio (HomePage)
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024, 768)
        #Ella se da cuenta que el cuadro de entrada esta bien centrado
        inputbox = self.browser.find_element(By.ID, 'id_new_item')
        self.assertAlmostEqual(inputbox.location['x'] + inputbox.size['width']/2,
                               290,
                               delta=50
                               )
        
        #Ella empieza una nueva lista y ve que la entrada esta bien centrada
        inputbox.send_keys('testing')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table("1: testing")
        inputbox = self.browser.find_element(By.ID, 'id_new_item')
        self.assertAlmostEqual(inputbox.location['x'] + inputbox.size['width']/2,
                               512,
                               delta=50
                               )

