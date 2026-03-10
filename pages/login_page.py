from pages.base_page import BasePage
from selenium.webdriver.common.by import By

class LoginPage(BasePage):
    # 定位符
    _username_input = (By.ID, "user-name")
    _password_input = (By.ID, "password")
    _login_button = (By.ID, "login-button")
    _error_message = (By.CSS_SELECTOR, "h3[data-test='error']")

    def open(self):
        self.driver.get("https://www.saucedemo.com")
        self.logger.info("打开登录页面")

    def login(self, username, password):
        self.input_text(self._username_input, username)
        self.input_text(self._password_input, password)
        self.click(self._login_button)
        self.logger.info(f"尝试登录: {username}")
        # 新增调试输出
        current_url = self.driver.current_url
        print(f"[DEBUG] 登录后 URL: {current_url}")
        error = self.get_error_message()
        if error:
            print(f"[DEBUG] 错误信息: {error}")

    def get_error_message(self):
        if self.is_element_visible(self._error_message, timeout=3):
            return self.get_text(self._error_message)
        return None

    def is_login_success(self):
        return "inventory.html" in self.driver.current_url