import time
from typing import Optional
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement


class WebElementsHandler:
    def __init__(self):
        self.something = None
        self.driver = None


    @staticmethod
    def wait_for_element(*locators: str, driver: WebDriver, timeout: int) -> Optional[WebElement]:
            element = WebDriverWait(driver, timeout).until(EC.any_of(
                *[EC.presence_of_element_located((By.XPATH, locator)) for locator in locators]
            ))
            time.sleep(0.5)
            return element


    @staticmethod
    def move_to_element_and_click(actions, element_to_hover):
        actions.move_to_element(element_to_hover).perform()  # Эмулируем движение мыши
        actions.click(element_to_hover).perform()   # Эмулируем клик по элементу после наведения


