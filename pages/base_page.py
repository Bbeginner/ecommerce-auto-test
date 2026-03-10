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
        """输入文本，输入后立即验证，确保真正输入成功"""
        element = self.find_element(locator, timeout)
        
        # 1. 先点击激活元素（解决 CI 中元素未完全聚焦的问题）
        element.click()
        
        # 2. 清空输入框
        element.clear()
        
        # 3. 逐字符输入（比一次性输入更稳定）
        for char in text:
            element.send_keys(char)
        
        # 4. 关键步骤：验证输入是否成功
        actual_value = element.get_attribute('value')
        if actual_value != text:
            self.logger.warning(f"输入验证失败，期望: '{text}'，实际: '{actual_value}'，尝试重新输入")
            # 如果验证失败，强制使用 JavaScript 设置值
            self.driver.execute_script("arguments[0].value = arguments[1];", element, text)
            # 再次验证
            final_value = element.get_attribute('value')
            if final_value != text:
                raise Exception(f"输入元素 {locator} 失败，无法设置文本 '{text}'，当前值为 '{final_value}'")
        
        self.logger.debug(f"向 {locator} 成功输入: {text}")

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