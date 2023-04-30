import unittest
from selenium import webdriver


class NewVisitorTest(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Chrome()

    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_todo_list(self):
        # Edith ouviu falar de um novo aplicativo de tarefas on-line legal.
        # Ela vai verificar a página inicial
        self.browser.get("http://localhost:8000")

        # Ela percebe que o título da página e o cabeçalho mencionam listas de tarefas
        self.assertIn("To-Do", self.browser.title)

        # Ela é convidada a inserir um item de tarefa imediatamente
        self.fail("Finish the test!")

        # Ela digita "Buy peacock feathers" em uma caixa 
        # de texto (o hobby de Edith é fazer iscas para pesca com fly)


        # Quando ela tecla enter, a página é atualizada, e agora A página lista
        # "1: Buy peacock feathers" como um item em uma lista de tarefas


        # Ainda continua havendo uma caixa de texto convidando-a a acrescentar outro
        # item. Ela insere "Use peacock feathers to make a fly" (Edith é bem metódica)


        # A página é atualizada novamente e agora mostra os dois itens em sua lista


        # Edith se pergunta se o site lembrará de sua lista. Então ela nota
        # que o site gerou um URL único para ela -- há um pequeno
        # texto explicativo para isso.


        # Ela acessa esse URL -- sua lista de tarefas continua lá.


        # Satisfeita, ela volta a dormir


if __name__ == "__main__":
    unittest.main(warnings="ignore")
