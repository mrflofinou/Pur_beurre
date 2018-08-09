from django.test import LiveServerTestCase

import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
import selenium.webdriver.support.ui as ui
from selenium.webdriver.support import expected_conditions as ec


class FunctionalTest(LiveServerTestCase):

    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.get("http://localhost:8000/")
        self.wait = ui.WebDriverWait(self.driver, 1000)


    def tearDown(self):
        self.driver.quit()
    
    def user_makes_search(self):
        element = self.driver.find_element_by_id("foodsearch")
        submit = self.driver.find_element_by_id("submit")
        element.send_keys("nutella")
        submit.click()
        self.wait.until(ec.presence_of_element_located((By.ID, "substitutes")))

    def test_home_page_returns_200(self):
        res = requests.get(self.driver.current_url)
        self.assertEqual(res.status_code, 200)

    def test_Pur_Beurre_in_title_of_home_page(self):
        self.assertIn("Pur Beurre", self.driver.title)
    
    def test_results_page_returns_200(self):
        self.user_makes_search()
        res = requests.get(self.driver.current_url)
        self.assertEqual(res.status_code, 200)

    def test_results_page_url_contains_query(self):
        self.user_makes_search()
        self.assertIn(
                    "query=nutella",
                    self.driver.current_url,
                    )
    
    def test_results_page_header_title_is_the_query(self):
        self.user_makes_search()
        header_title = self.driver.find_element_by_id("headerTitle")
        header_title = header_title.text
        self.assertEqual(header_title, "NUTELLA")

    
    def test_details_page_retruns_200(self):
        self.user_makes_search()
        substitute = self.driver.find_element_by_css_selector("a.substitute") # passer un identfiant unique
        substitute.click() # attendre après le clique
        self.wait.until(ec.presence_of_element_located((By.ID, "details")))
        print(self.driver.current_url)
        # res = requests.get(self.driver.current_url)
        self.assertEqual(self.driver.current_url, "http://localhost:8000/substitute/3175681105393/")
    
    # Faire des tests sur le contenu de la page de détails (image, liste ingrédients, nutriscore)

    # Faire des tests de cas d'exception (pas d'image, pas de liste d'ingrédients) et vérifier que ça s'affiche bien
