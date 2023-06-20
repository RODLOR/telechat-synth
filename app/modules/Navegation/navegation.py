# Browser setup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class Navegation():
    
    def __init__(self, arguments : list):
        self.app_driver = webdriver.Chrome(options=self.options(arguments))
        self.wait_to = WebDriverWait(self.app_driver, 180)
        self.number = 0
        
    @staticmethod
    def options(arguments : list):
        app_options = webdriver.ChromeOptions()
        for argument in arguments:
            app_options.add_argument(argument)
        return app_options
    
    @staticmethod
    def appRoute(path : str):
        return Service(path)

    def navegating(self, req : str):
        
        # Encontrar el campo de entrada
        textarea = self.wait_to.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, '[id="mat-input-0"]')))
        # Enviar texto
        textarea.send_keys(req)

        # Encontrar el botón de envío y hacer click
        submit_button = self.app_driver.find_element(
            By.CSS_SELECTOR, '[mattooltip="Submit"]')
        submit_button.click()

        # Esperar hasta que aparezca un nuevo elemento 'message-content'
        new_element = None

        if self.number == 0:
            elements = self.wait_to.until(
                EC.presence_of_all_elements_located((By.TAG_NAME, 'message-content')))
            new_element = elements[0]
            self.element_number()
        else:
            while new_element is None:
                elements = self.wait_to.until(
                    EC.presence_of_all_elements_located((By.TAG_NAME, 'message-content')))
                if len(elements) > self.number:
                    new_element = elements[-1]
                    self.element_number()
                else:
                    # Esperar 3 segundo antes de verificar nuevamente
                    time.sleep(3)
        res = new_element.get_attribute('innerHTML')  
        return res
    
    def refresh(self):
        self.app_driver.refresh()
        return
    
    def stop_app(self):
        self.app_driver.close()
        self.app_driver.quit()
        return
    
    def element_number(self):
        self.number += 1
        return self.number