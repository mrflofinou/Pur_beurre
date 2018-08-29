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
        self.user = User.objects.create_user("testuser",
                                            "testuser@email.com",
                                            "testpswd")

    def tearDown(self):
        self.driver.quit()
    
    def user_makes_search(self, query):
        """ User path to search the substitute of a product """
        element = self.driver.find_element_by_id("foodsearch")
        submit = self.driver.find_element_by_id("submit")
        element.send_keys(query)
        submit.click()
        self.wait.until(ec.presence_of_element_located((By.ID, "substitutes")))
    
    def user_signup(self, username, email, password1, password2):
        """ User path to sign up """
        element_login = self.driver.find_element_by_id("login")
        element_login.click()
        self.wait.until(ec.presence_of_element_located((By.ID, "signup")))
        element_signup = self.driver.find_element_by_id("signup")
        element_signup.click()
        self.wait.until(ec.presence_of_element_located((By.ID, "signupform")))
        username_element = self.driver.find_element_by_name("username")
        username_element.send_keys(username)
        email_element = self.driver.find_element_by_name("email")
        email_element.send_keys(email)
        password1_element = self.driver.find_element_by_name("password1")
        password1_element.send_keys(password1)
        password2_element = self.driver.find_element_by_name("password2")
        password2_element.send_keys(password2)
        submit = self.driver.find_element_by_id("signupsubmit")
        submit.click()
    
    def user_login(self, username, password, waiting):
        """ User path to login """
        element_login = self.driver.find_element_by_id("login")
        element_login.click()
        self.wait.until(ec.presence_of_element_located((By.ID, "signup")))
        username_element = self.driver.find_element_by_name("username")
        username_element.send_keys(username)
        password_element = self.driver.find_element_by_name("password")
        password_element.send_keys(password)
        submit = self.driver.find_element_by_id("submitlogin")
        submit.click()
        self.wait.until(ec.presence_of_element_located((By.ID, waiting)))
    
    def test_home_page_returns_200(self):
        res = Client().get(f'{self.driver.current_url}')   
        self.assertEqual(res.status_code, 200)

    def test_Pur_Beurre_in_title_of_home_page(self):
        self.assertIn("Pur Beurre", self.driver.title)
    
    def test_results_page_returns_200(self):
        self.user_makes_search("nutella")
        res = Client().get(f'{self.driver.current_url}')
        self.assertEqual(res.status_code, 200)

    def test_results_page_url_contains_query(self):
        self.user_makes_search("nutella")
        self.assertIn(
                    "query=nutella",
                    self.driver.current_url,
                    )
    
    def test_results_page_returns_200_if_no_substiutes(self):
        self.user_makes_search("oreo")
        count_element = self.driver.find_element_by_id("count")
        res = Client().get(f'{self.driver.current_url}')
        self.assertEqual(count_element.text, "0 résultats") 
        self.assertEqual(res.status_code, 200)
    
    def test_results_page_header_title_is_the_query(self):
        self.user_makes_search("nutella")
        header_title = self.driver.find_element_by_id("headerTitle")
        header_title = header_title.text
        self.assertEqual(header_title, "nutella")
    
    def test_details_page_returns_200_and_contains_informations(self):
        self.user_makes_search("nutella")
        substitute = self.driver.find_element_by_css_selector("a.substitute")
        substitute.click()
        self.wait.until(ec.presence_of_element_located((By.ID, "details")))
        product_picture = self.driver.find_element_by_id("product-picture")
        product_picture_url = product_picture.get_attribute("src")
        nutriscore_picture = self.driver.find_element_by_id("nutriscore-picture")
        nutriscore_picture_url = nutriscore_picture.get_attribute("src")
        nutrition_picture = self.driver.find_element_by_id("nutriscore-picture")# ERREUR d'ID !
        nutrition_picture_url = nutrition_picture.get_attribute("src")
        ingredients_list = self.driver.find_element_by_id("ingredients")
        ingredients_list_text = ingredients_list.text
        res = Client().get(f'{self.driver.current_url}')
        self.assertEqual(res.status_code, 200)
        self.assertGreater(len(product_picture_url), 0)
        self.assertGreater(len(nutriscore_picture_url), 0)
        self.assertGreater(len(nutrition_picture_url), 0)
        self.assertGreater(len(ingredients_list_text), 0)

    def test_signup(self):
        old_users_number = User.objects.count()
        print(User.objects.all())
        self.user_signup(username="Fiflo",
                        email="Fiflo@email.com",
                        password1="bidule01",
                        password2="bidule01")
        self.wait.until(ec.presence_of_element_located((By.ID, "account")))
        new_users_number = User.objects.count()
        print(User.objects.all())
        self.assertEqual(new_users_number, old_users_number + 1)

    # Faire test cas d'exception (mauvais email, mauvais password, pseudo deja existant)

    def test_signup_user_already_exists(self):
        self.user_signup(username="testuser",
                email="Fiflo@email.com",
                password1="bidule01",
                password2="bidule01")
        self.wait.until(ec.presence_of_element_located((By.CLASS_NAME, "error")))
        error = self.driver.find_element_by_class_name("error")
        self.assertEqual(error.text, "Un utilisateur avec ce nom existe déjà.")

    def test_signup_wrong_password(self):
        self.user_signup(username="Fiflo",
                        email="Fiflo@email.com",
                        password1="bidule01",
                        password2="bidule02")
        self.wait.until(ec.presence_of_element_located((By.CLASS_NAME, "error")))
        error = self.driver.find_element_by_class_name("error")
        self.assertEqual(error.text, "Les deux mots de passe ne correspondent pas.")

    def test_signup_password_looks_like_username(self):
        self.user_signup(username="Fiflo",
                        email="Fiflo@email.com",
                        password1="fiflo0102",
                        password2="fiflo0102")
        self.wait.until(ec.presence_of_element_located((By.CLASS_NAME, "error")))
        error = self.driver.find_element_by_class_name("error")
        self.assertEqual(error.text, "Le mot de passe est trop semblable au champ « nom d'utilisateur ».")
    
    def test_signup_password_too_short(self):
        self.user_signup(username="Fiflo",
                        email="Fiflo@email.com",
                        password1="bidule",
                        password2="bidule")
        self.wait.until(ec.presence_of_element_located((By.CLASS_NAME, "error")))
        error = self.driver.find_element_by_class_name("error")
        self.assertEqual(error.text, "Ce mot de passe est trop court. Il doit contenir au minimum 8 caractères.")

    def test_signup_password_only_numerict(self):
        self.user_signup(username="Fiflo",
                        email="Fiflo@email.com",
                        password1="13243546",
                        password2="13243546")
        self.wait.until(ec.presence_of_element_located((By.CLASS_NAME, "error")))
        error = self.driver.find_element_by_class_name("error")
        self.assertEqual(error.text, "Ce mot de passe est entièrement numérique.")
    
    def test_signup_password_too_mainstram(self):
        self.user_signup(username="Fiflo",
                        email="Fiflo@email.com",
                        password1="password",
                        password2="password")
        self.wait.until(ec.presence_of_element_located((By.CLASS_NAME, "error")))
        error = self.driver.find_element_by_class_name("error")
        self.assertEqual(error.text, "Ce mot de passe est trop courant.")

    def test_login(self):
        self.user_login(username="testuser",
                        password="testpswd",
                        waiting="account")
        self.assertEqual(self.driver.current_url, self.live_server_url + "/") # Tester / urls django

    def test_login_wrong_username(self):
        self.user_login(username="wrongusername",
                        password="testpswd",
                        waiting="login_error")
        error = self.driver.find_element_by_id("login_error")
        self.assertEqual(error.text, "Le nom d'utilisateur et le mot de passe ne correspondent pas.")
    
    def test_login_wrong_password(self):
        self.user_login(username="testuser",
                        password="wrongpswd",
                        waiting="login_error")
        error = self.driver.find_element_by_id("login_error")
        self.assertEqual(error.text, "Le nom d'utilisateur et le mot de passe ne correspondent pas.")
    
    def test_logout(self):
        self.user_login(username="testuser",
                        password="testpswd",
                        waiting="account")
        element_logout = self.driver.find_element_by_id("logout")
        element_logout.click()
        self.wait.until(ec.presence_of_element_located((By.ID, "login")))
        self.assertEqual(self.driver.current_url, self.live_server_url + "/")

    def test_save_product(self):
        old_number_products = self.user.products.count()
        print(self.user.products.all())
        self.user_login(username="testuser",
                        password="testpswd",
                        waiting="account")
        self.user_makes_search("nutella")
        substitute = self.driver.find_element_by_css_selector("a.substitute")
        substitute.click()
        self.wait.until(ec.presence_of_element_located((By.ID, "details")))
        save_element = self.driver.find_element_by_id("save")
        save_element.click()
        new_number_products = self.user.products.count()
        print(self.user.products.all())
        self.assertEqual(new_number_products, old_number_products + 1)
