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
        time.sleep(4)
        self.input_text(self._username_input, username)
        self.input_text(self._password_input, password)
        self.click(self._login_button)
        self.logger.info(f"尝试登录: {username}")

    # def login(self, username, password, retry=True):
    #     """执行登录操作，增加兜底重试机制"""
    #     self.input_text(self._username_input, username)
    #     self.input_text(self._password_input, password)
    #     self.click(self._login_button)
    #     self.logger.info(f"尝试登录: {username}")
        
    #     # 短暂等待，让页面响应，尤其对 performance_glitch_user 有用
    #     time.sleep(2) # 简单粗暴，但有效
        
    #     # 兜底逻辑：如果 URL 没变（还在登录页）且没有错误消息，说明登录操作可能没触发
    #     current_url = self.driver.current_url
    #     error_element_exists = self.is_element_visible(self._error_message, timeout=2)
        
    #     if "inventory.html" not in current_url and not error_element_exists and retry:
    #         self.logger.warning("登录后页面无变化，尝试刷新并重试一次")
    #         self.driver.refresh()
    #         time.sleep(2)
    #         # 重新尝试登录（不再重试，避免死循环）
    #         self.input_text(self._username_input, username)
    #         self.input_text(self._password_input, password)
    #         self.click(self._login_button)
    #         time.sleep(2)
        
    #      # 如果仍然无变化，尝试用 JS 点击登录按钮
    #     if "inventory.html" not in self.driver.current_url and not self.is_element_visible(self._error_message, timeout=2):
    #         self.logger.warning("常规点击无效，尝试 JS 点击登录按钮")
    #         btn = self.find_element(self._login_button)
    #         self.driver.execute_script("arguments[0].click();", btn)
    #         time.sleep(2)
        
    #     # 终极兜底：如果仍然没反应，直接提交表单
    #     if "inventory.html" not in self.driver.current_url and not self.is_element_visible(self._error_message, timeout=2):
    #         self.logger.warning("JS点击无效，尝试直接提交表单")
    #         self.driver.execute_script("""
    #             var form = document.querySelector('form');
    #             if (form) form.submit();
    #         """)
    #         time.sleep(2)

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