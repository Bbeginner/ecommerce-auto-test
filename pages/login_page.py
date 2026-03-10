from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from pages.base_page import BasePage
import time

class LoginPage(BasePage):
    _username_input = (By.ID, "user-name")
    _password_input = (By.ID, "password")
    _login_button = (By.ID, "login-button")
    _error_message = (By.CSS_SELECTOR, "h3[data-test='error']")
    _inventory_container = (By.CSS_SELECTOR, "div.inventory_list")

    def open(self):
        self.driver.get("https://www.saucedemo.com")
        self.logger.info("打开登录页面")
        # 强制等待，确保页面完全加载
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self._username_input)
        )

    def login(self, username, password):
        self.input_text(self._username_input, username)
        self.input_text(self._password_input, password)
        self.click(self._login_button)
        self.logger.info(f"尝试登录: {username}")
        # 登录后强制等待一段时间，让页面跳转完成（尤其对 performance_glitch_user 有用）
        time.sleep(2)  # 简单粗暴，但有效

    def get_error_message(self, timeout=10):
        """获取错误消息，带显式等待"""
        try:
            error_element = WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(self._error_message)
            )
            text = error_element.text
            self.logger.info(f"错误消息: {text}")
            return text
        except TimeoutException:
            self.logger.warning(f"等待 {timeout} 秒后错误消息未出现")
            return None

    def is_login_success(self):
        return "inventory.html" in self.driver.current_url

    def wait_for_inventory_page(self, timeout=15):
        """等待商品列表页出现"""
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(self._inventory_container)
            )
            return True
        except TimeoutException:
            return False