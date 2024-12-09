import random
import time
from typing import Optional, Tuple

from selenium.common import TimeoutException, StaleElementReferenceException, ElementNotInteractableException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement


class WebElementsHandler:
    def __init__(self):
        self.something = None

    @staticmethod
    def move_to_element_and_click(actions: ActionChains, element_to_hover: WebElement):
        try:
            actions.move_to_element(element_to_hover).perform()  # Наведение на элемент
            actions.click(element_to_hover).perform()  # Клик по элементу
        except TimeoutException:
            print("Элемент не доступен для клика.")
        except Exception as e:
            print(f"Произошла ошибка при попытке кликнуть по элементу: {e}")

    @staticmethod
    def wait_for_element_css(
            *locators: str, driver, timeout: int = 30, interval: int = 1
    ) -> Optional[WebElement]:
        """
        Ждёт, пока элемент станет доступен.

        :param locators: Локаторы элементов в формате CSS Selector.
        :param driver: WebDriver Selenium.
        :param timeout: Таймаут ожидания в секундах.
        :param interval: Интервал повторных попыток в секундах.
        :param interval: Интервал времени для повторного поиска в рамках таймаута
        :return: WebElement, если он найден и доступен, иначе None.
        """
        # Преобразование каждого локатора CSS Selector в кортеж формата (By.CSS_SELECTOR, locator)
        locator_tuples = [(By.CSS_SELECTOR, locator) for locator in locators]

        # Используем wait_for_element_tuple для выполнения ожидания
        try:
            return WebElementsHandler.wait_for_element_tuple(
                *locator_tuples, driver=driver, timeout=timeout, interval=interval
            )
        except TimeoutException as e:
            print(f"Элемент не найден за {timeout} секунд. Ошибка: {e}")
            return None

    @staticmethod
    def wait_for_element_xpath(
            *locators: str, driver, timeout: int = 30, interval: int=1
    ) -> Optional[WebElement]:
        """
        Ждёт, пока элемент станет доступен

        :param locators: Локаторы элементов в формате XPath.
        :param driver: WebDriver Selenium.
        :param timeout: Таймаут ожидания в секундах.
        :param interval: Интервал времени для повторного поиска в рамках таймаута
        :return: WebElement, если он найден и доступен, иначе None.
        """
        # Преобразование каждого локатора XPath в кортеж формата (By.XPATH, locator)
        locator_tuples = [(By.XPATH, locator) for locator in locators]

        # Используем wait_for_element_tuple для выполнения ожидания
        try:
            return WebElementsHandler.wait_for_element_tuple(
                *locator_tuples, driver=driver, timeout=timeout, interval=interval
            )
        except TimeoutException as e:
            print(f"Элемент не найден за {timeout} секунд. Ошибка: {e}")
            return None

    @staticmethod
    def wait_for_element_tuple(
            *locators: Tuple[str, str], driver, timeout: int = 30, interval: int = 1
    ) -> Optional[WebElement]:
        """
        Ждёт, пока элемент станет доступен, пытается найти его каждый interval в рамках заданного timeout

        :param locators: Локаторы в формате Tuple. Например, (By.CSS_SELECTOR, locator) или (By.XPATH, locator)
        :param driver: WebDriver Selenium.
        :param timeout: Таймаут ожидания в секундах.
        :param interval: Интервал времени для повторного поиска в рамках таймаута
        :return: WebElement, если он найден и доступен, иначе None.
        """
        end_time = time.time() + timeout

        while time.time() < end_time:
            try:
                element = WebDriverWait(driver, interval).until(EC.any_of(  # Ждём, пока элемент появится на странице
                    *[EC.presence_of_element_located(locator) for locator in locators]
                ))
                time.sleep(1)  # Дополнительная задержка
                return element
            except StaleElementReferenceException:
                print("Элемент обновился в DOM. Повторяем попытку...")
            except TimeoutException:
                print(f"Элемент не найден в течение {timeout} секунд.")
            except Exception as e:
                print(f"Произошла ошибка при поиске элемента: {e}")
            time.sleep(0.5)  # Небольшая задержка перед повторной попыткой
        raise TimeoutException(f"Не удалось найти элементы с указанными локаторами: {locators}")

    @staticmethod
    def ensure_element_is_interactable(driver: WebDriver, locator: Tuple[str, str], timeout: int = 10) -> bool:
        """
        Проверяет, что элемент доступен для взаимодействия:
        1. Элемент присутствует в DOM.
        2. Элемент видим.
        3. Элемент активен (не заблокирован).

        :param driver: WebDriver Selenium.
        :param locator: Локатор элемента (например, (By.XPATH, "//button[@id='submit']")).
        :param timeout: Таймаут ожидания в секундах.
        :return: True, если элемент доступен для взаимодействия, иначе False.
        """
        try:
            # Явное ожидание появления элемента в DOM
            element = WebDriverWait(driver, timeout).until(
                EC.presence_of_element_located(locator)
            )

            # Проверка видимости элемента на странице
            if not WebElementsHandler.is_element_visible(driver, element):
                raise StaleElementReferenceException("Элемент не видим или скрыт на странице.")

            # Проверка доступности элемента для взаимодействия
            if not element.is_enabled():
                raise StaleElementReferenceException("Элемент не активен для взаимодействия.")

            return True

        except StaleElementReferenceException:
            print("Элемент был перестроен в DOM. Повторяем попытку...")
            return WebElementsHandler.ensure_element_is_interactable(driver, locator, timeout)

    @staticmethod
    def is_element_visible(driver: WebDriver, element: WebElement) -> bool:
        """
        Проверяет, что элемент видим в области окна браузера.
        :param driver: WebDriver Selenium.
        :param element: WebElement.
        :return: True, если элемент видим, иначе False.
        """
        try:
            # Скроллим элемент в видимую область
            driver.execute_script("arguments[0].scrollIntoView(true);", element)

            # Получаем координаты элемента и проверяем его видимость
            rect = driver.execute_script(
                "const rect = arguments[0].getBoundingClientRect();"
                "return { top: rect.top, bottom: rect.bottom, left: rect.left, right: rect.right };", element
            )

            # Проверка, что элемент полностью в пределах области окна
            return rect['top'] >= 0 and rect['left'] >= 0 and rect['bottom'] <= driver.execute_script(
                "return window.innerHeight;") and rect['right'] <= driver.execute_script("return window.innerWidth;")
        except Exception as e:
            print(f"Ошибка при проверке видимости элемента: {e}")
            return False

    @staticmethod
    def slow_typing(element: WebElement, text: str, driver: WebDriver = None, use_clipboard: bool = False):
        """
        Печатает текст с задержкой, чтобы имитировать ввод вручную.
        Проверяет, что элемент актуален перед каждой отправкой символа.
        :param element: Элемент для ввода текста, полученный ранее.
        :param text: Текст, который необходимо ввести.
        :param driver: WebDriver, используется, если нужно сфокусироваться на элементе с помощью javascript
        :param use_clipboard: Флаг, отвечающий за то, нужно ли вставлять текст в поле сразу полностью
        """
        if driver is not None:
            driver.execute_script("arguments[0].focus();", element)

        if use_clipboard:
            element.send_keys(text)
            return

        for char in text:
            delay = random.uniform(0.015, 0.15)
            try:
                element.send_keys(char)
            except ElementNotInteractableException:
                print("Элемент недоступен для ввода.")
                raise
            time.sleep(delay)