from django.test import LiveServerTestCase, Client
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session

from selenium import webdriver
from selenium.webdriver.common.by import By
import selenium.webdriver.support.ui as ui
from selenium.webdriver.support import expected_conditions as ec


class FunctionalTest(LiveServerTestCase):

    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.get(self.live_server_url)
        self.driver.maximize_window()
        self.wait = ui.WebDriverWait(self.driver, 1000)
        user = User.objects.create_user("testuser", "testuser@email.com", "testpswd")

    def tearDown(self):
        self.driver.quit()
    
    def user_makes_search(self):
        element = self.driver.find_element_by_id("foodsearch")
        submit = self.driver.find_element_by_id("submit")
        element.send_keys("nutella")
        submit.click()
        self.wait.until(ec.presence_of_element_located((By.ID, "substitutes")))

    # def test_home_page_returns_200(self):
    #     res = Client().get(f'{self.driver.current_url}')   
    #     self.assertEqual(res.status_code, 200)

    # def test_Pur_Beurre_in_title_of_home_page(self):
    #     self.assertIn("Pur Beurre", self.driver.title)
    
    # def test_results_page_returns_200(self):
    #     self.user_makes_search()
    #     res = Client().get(f'{self.driver.current_url}') 
    #     self.assertEqual(res.status_code, 200)

    # def test_results_page_url_contains_query(self):
    #     self.user_makes_search()
    #     self.assertIn(
    #                 "query=nutella",
    #                 self.driver.current_url,
    #                 )
    
    # def test_results_page_header_title_is_the_query(self):
    #     self.user_makes_search()
    #     header_title = self.driver.find_element_by_id("headerTitle")
    #     header_title = header_title.text
    #     self.assertEqual(header_title, "nutella")

    
    # def test_details_page_returns_200_and_contains_informations(self):
    #     self.user_makes_search()
    #     substitute = self.driver.find_element_by_css_selector("a.substitute")
    #     substitute.click()
    #     self.wait.until(ec.presence_of_element_located((By.ID, "details")))
    #     product_picture = self.driver.find_element_by_id("product-picture")
    #     product_picture_url = product_picture.get_attribute("src")
    #     nutriscore_picture = self.driver.find_element_by_id("nutriscore-picture")
    #     nutriscore_picture_url = nutriscore_picture.get_attribute("src")
    #     nutrition_picture = self.driver.find_element_by_id("nutriscore-picture")
    #     nutrition_picture_url = nutrition_picture.get_attribute("src")
    #     ingredients_list = self.driver.find_element_by_id("ingredients")
    #     ingredients_list_text = ingredients_list.text
    #     res = Client().get(f'{self.driver.current_url}')
    #     self.assertEqual(res.status_code, 200)
    #     self.assertGreater(len(product_picture_url), 0)
    #     self.assertGreater(len(nutriscore_picture_url), 0)
    #     self.assertGreater(len(nutrition_picture_url), 0)
    #     self.assertGreater(len(ingredients_list_text), 0)

    # Faire des tests de cas d'exception (pas d'image, pas de liste d'ingrédients) et vérifier que ça s'affiche bien

    # def test_signup(self):
    #     old_users_number = User.objects.count()
    #     print(User.objects.all())
    #     element_connexion = self.driver.find_element_by_id("login")
    #     element_connexion.click()
    #     self.wait.until(ec.presence_of_element_located((By.ID, "signup")))
    #     element_signup = self.driver.find_element_by_id("signup")
    #     element_signup.click()
    #     self.wait.until(ec.presence_of_element_located((By.ID, "signupform")))
    #     username = self.driver.find_element_by_name("username")
    #     username.send_keys("Fiflo")
    #     email = self.driver.find_element_by_name("email")
    #     email.send_keys("Fiflo@email.com")
    #     password1 = self.driver.find_element_by_name("password1")
    #     password1.send_keys("bidule01")
    #     password2 = self.driver.find_element_by_name("password2")
    #     password2.send_keys("bidule01")
    #     submit = self.driver.find_element_by_id("signupsubmit")
    #     submit.click()
    #     self.wait.until(ec.presence_of_element_located((By.ID, "foodsearch")))
    #     new_users_number = User.objects.count()
    #     print(User.objects.all())
    #     self.assertEqual(new_users_number, old_users_number + 1)

    # Faire test cas d'exception (mauvais email, mauvais password, email deja existant)
    
    # def test_login(self):
    #     element_connexion = self.driver.find_element_by_id("login")
    #     element_connexion.click()
    #     self.wait.until(ec.presence_of_element_located((By.ID, "signup")))
    #     username = self.driver.find_element_by_name("username")
    #     username.send_keys("testuser")
    #     password = self.driver.find_element_by_name("password")
    #     password.send_keys("testpswd")
    #     submit = self.driver.find_element_by_id("submitlogin")
    #     submit.click()
    #     self.wait.until(ec.presence_of_element_located((By.ID, "foodsearch")))
    #     self.assertEqual(self.driver.current_url, self.live_server_url + "/")

    # Faire test cas d'exception mauvais password, mauvais pseudo