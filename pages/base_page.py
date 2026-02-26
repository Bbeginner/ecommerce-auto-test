from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from utils.logger import Logger

class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.logger = Logger().get_logger()

    def find_element(self, locator, timeout=10):
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(locator)
            )
            self.logger.debug(f"找到元素: {locator}")
            return element
        except TimeoutException:
            self.logger.error(f"元素未找到: {locator}")
            raise

    def click(self, locator, timeout=10):
        element = self.find_element(locator, timeout)
        element.click()
        self.logger.debug(f"点击元素: {locator}")

    def input_text(self, locator, text, timeout=10):
        element = self.find_element(locator, timeout)
        element.clear()
        element.send_keys(text)
        self.logger.debug(f"向 {locator} 输入: {text}")

    def get_text(self, locator, timeout=10):
        element = self.find_element(locator, timeout)
        text = element.text
        self.logger.debug(f"获取文本 {locator}: {text}")
        return text

    def is_element_visible(self, locator, timeout=5):
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
            return True
        except TimeoutException:
            return False