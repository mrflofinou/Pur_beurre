from django.test import TestCase

from selenium import webdriver


class FonctionalTest(TestCase):

    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.get("http://localhost:8000/")
    
    def tearDown(self):
        self.driver.quit()

    def test_Pur_Beurre_in_title_of_home_page(self):
        self.assertIn("Pur Beurre", self.driver.title)
    
    def test_when_make_food_search_results_page_appears(self):
        element = self.driver.find_element_by_id("foodsearch")
        submit = self.driver.find_element_by_id("submit")
        element.send_keys("nutella")
        submit.click()
        self.assertEqual(self.driver.current_url, "http://localhost:8000/substitute/?query=nutella")
    
    def test_header_title_is_the_query(self):
        element = self.driver.find_element_by_id("foodsearch")
        submit = self.driver.find_element_by_id("submit")
        element.send_keys("nutella")
        submit.click()
        header_title = self.driver.find_element_by_id("headerTitle")
        header_title = header_title.text
        self.assertEqual(header_title, "NUTELLA")

    
    def test_when_product_is_selected_details_page_appears(self):
        element = self.driver.find_element_by_id("foodsearch")
        submit = self.driver.find_element_by_id("submit")
        element.send_keys("nutella")
        submit.click()
        substitute = self.driver.find_element_by_css_selector("a.substitute")
        substitute.click()
        self.assertIn("http://localhost:8000/substitute/details/", self.driver.current_url)
    

    