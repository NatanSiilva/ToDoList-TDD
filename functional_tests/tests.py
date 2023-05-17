import time
import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException
from django.test import LiveServerTestCase

MAX_WAIT = 5


class NewVisitorTest(LiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Chrome()

    def tearDown(self):
        self.browser.quit()

    def wait_for_row_in_list_table(self, row_text):
        start_time = time.time()
        while True:
            try:
                table = self.browser.find_element(By.ID, "id_list_table")
                rows = table.find_elements(By.TAG_NAME, "tr")
                self.assertIn(row_text, [row.text for row in rows])
                return
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)

    def test_can_start_a_todo_list(self):
        # Edith ouviu falar de um novo aplicativo de tarefas on-line legal.
        # Ela vai verificar a página inicial
        self.browser.get(self.live_server_url)

        # Ela percebe que o título da página e o cabeçalho mencionam listas de tarefas
        self.assertIn("To-Do", self.browser.title)
        header_text = self.browser.find_element(By.TAG_NAME, "h1").text
        self.assertIn("To-Do", header_text)

        # Ela é convidada a inserir um item de tarefa imediatamente
        inputbox = self.browser.find_element(By.ID, "id_new_item")

        self.assertEqual(inputbox.get_attribute("placeholder"), "Enter a to-do item")

        # Ela digita "Buy peacock feathers" (compra penas de pavão) em uma caixa
        # de texto (o hobby de Edith é fazer iscas para pesca com fly)
        inputbox.send_keys("Buy peacock feathers")

        # Quando ela tecla enter, a página é atualizada, e agora A página lista
        # "1: Buy peacock feathers" como um item em uma lista de tarefas
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table("1: Buy peacock feathers")

        # Ainda continua havendo uma caixa de texto convidando-a a acrescentar outro
        # item. Ela insere "Use peacock feathers to make a fly" (Edith é bem metódica)
        inputbox = self.browser.find_element(By.ID, "id_new_item")
        inputbox.send_keys("Use peacock feathers to make a fly")
        inputbox.send_keys(Keys.ENTER)

        # A página é atualizada novamente e agora mostra os dois itens em sua lista
        self.wait_for_row_in_list_table("1: Buy peacock feathers")
        self.wait_for_row_in_list_table("2: Use peacock feathers to make a fly")

        # Edith se pergunta se o site lembrará de sua lista. Então ela nota
        # que o site gerou um URL único para ela -- há um pequeno
        # texto explicativo para isso.

        self.fail("Finish the test!")

        # Ela acessa esse URL -- sua lista de tarefas continua lá.

        # Satisfeita, ela volta a dormir

    def test_multiple_users_can_start_list_at_different_url(self):
        # Edith inicia uma nova lista de tarefas
        self.browser.get(self.live_server_url)
        inputbox = self.browser.find_element(By.ID, "id_new_item")  
        inputbox.send_keys("Buy peacock feathers")
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table("1: Buy peacock feathers")

        # Ela percebe que sua lista tem um URL único
        edith_list_url = self.browser.current_url
        self.assertRegex(edith_list_url, "/lists/.+")

        # Agora um novo usuário, Francis, chega ao site.

        ## Usamos uma nova sessão de navegador para garantir que nenhuma informação
        ## de Edith está vindo de cookies etc
        self.browser.quit()
        self.browser = webdriver.Chrome()
        
        # Francis acessa a página inicial. Não há nenhum sinal da lista de Edith
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element(By.TAG_NAME, "body").text
        self.assertNotIn("Buy peacock feathers", page_text)
        self.assertNotIn("make a fly", page_text)

        # Francis inicia uma nova lista inserindo um item novo. Ele
        # é menos interessante que Edith...
        inputbox = self.browser.find_element(By.ID, "id_new_item")
        inputbox.send_keys("Buy milk")
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table("1: Buy milk")

        # Francis obtém seu próprio URL exclusivo
        francis_list_url = self.browser.current_url
        self.assertRegex(francis_list_url, "/lists/.+")
        self.assertNotEqual(francis_list_url, edith_list_url)

        # Novamente, não há sinal algum da lista de Edith
        page_text = self.browser.find_element(By.TAG_NAME, "body").text
        self.assertNotIn("Buy peacock feathers", page_text)
        self.assertIn("Buy milk", page_text)

        # Satisfeitos, ambos voltam a dormir