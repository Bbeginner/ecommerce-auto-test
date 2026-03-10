import pytest
import allure
import time
from pages.login_page import LoginPage

@allure.feature("登录功能")
class TestLogin:
    def setup_method(self):
        self.driver = self.__class__.driver
        self.driver.delete_all_cookies()
        login_page = LoginPage(self.driver)
        login_page.open()  # open 已包含等待
         # 额外等待，确保元素可交互
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        from selenium.webdriver.common.by import By
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.ID, "user-name"))
        )

    @allure.story("登录场景参数化")
    @allure.title("测试登录场景：{username} / {password}")
    @pytest.mark.parametrize("username,password,expected_status", [
        ("", "secret_sauce", "empty_username"),
        ("standard_user", "", "empty_password"),
        ("locked_out_user", "secret_sauce", "locked"),
        ("fake_user", "wrong_pwd", "invalid"),
        ("performance_glitch_user", "secret_sauce", "success"),
        ("problem_user", "secret_sauce", "success"),
        ("standard_user", "secret_sauce", "success"),  # 故意传参错误的用例放最后
    ])
    def test_login_scenarios(self, username, password, expected_status):
        with allure.step("打开登录页面"):
            login_page = LoginPage(self.driver)
            # login_page.open()
        with allure.step(f"输入用户名：{username}，密码：{password}"):
            login_page.login(username, password)
            
        with allure.step("验证登录结果"):
            if expected_status == "success":
                # # 先尝试正常登录（因为本地可以，但 CI 可能失败）
                # login_page.login(username, password)
                # time.sleep(3)  # 等待页面响应
                # if not login_page.wait_for_inventory_page(timeout=5):
                #     # 如果失败，使用 JS 强制登录
                #     self.logger.warning(f"正常登录失败，尝试 JS 登录: {username}")
                #     login_page.login_by_js(username, password)
                # # 等待商品列表页出现
                assert login_page.wait_for_inventory_page(timeout=20) is True, \
                    f"登录后未进入商品列表页，当前 URL: {login_page.driver.current_url}"
            elif expected_status == "locked":
                assert login_page.is_login_success() is False
                error = login_page.get_error_message(timeout=10)
                assert error is not None, "锁定用户应显示错误消息"
                assert "locked out" in error.lower()
            elif expected_status == "empty_username":
                assert login_page.is_login_success() is False
                error = login_page.get_error_message(timeout=10)
                assert error is not None, "空用户名应显示错误消息"
                assert "username is required" in error.lower()
            elif expected_status == "empty_password":
                assert login_page.is_login_success() is False
                error = login_page.get_error_message(timeout=10)
                assert error is not None, "空密码应显示错误消息"
                assert "password is required" in error.lower()
            else:  # invalid
                assert login_page.is_login_success() is False
                error = login_page.get_error_message(timeout=10)
                assert error is not None, "无效凭证应显示错误消息"
                assert "do not match" in error.lower() or "username and password do not match" in error.lower()

    # 独立测试方法也做同样修改，但因为我们已经在参数化中覆盖，可以保留或删除。为简洁，可删除独立方法，但为了保险保留并修改
    @allure.story("空用户名")
    def test_empty_username(self):
        login_page = LoginPage(self.driver)
        login_page.open()
        login_page.login("", "secret_sauce")
        assert login_page.is_login_success() is False
        error = login_page.get_error_message(timeout=10)
        assert error is not None, "空用户名应显示错误消息"
        assert "username is required" in error.lower()

    @allure.story("空密码")
    def test_empty_password(self):
        login_page = LoginPage(self.driver)
        login_page.open()
        login_page.login("standard_user", "")
        assert login_page.is_login_success() is False
        error = login_page.get_error_message(timeout=10)
        assert error is not None, "空密码应显示错误消息"
        assert "password is required" in error.lower()

    @allure.story("用户名大小写敏感")
    def test_username_case_sensitive(self):
        login_page = LoginPage(self.driver)
        login_page.open()
        login_page.login("Standard_User", "secret_sauce")
        assert login_page.is_login_success() is False
        error = login_page.get_error_message(timeout=10)
        assert error is not None, "大小写错误应显示错误消息"
        assert "do not match" in error.lower()

    @allure.story("密码大小写敏感")
    def test_password_case_sensitive(self):
        login_page = LoginPage(self.driver)
        login_page.open()
        login_page.login("standard_user", "Secret_Sauce")
        assert login_page.is_login_success() is False
        error = login_page.get_error_message(timeout=10)
        assert error is not None, "大小写错误应显示错误消息"
        assert "do not match" in error.lower()

    @allure.story("用户名含前后空格")
    def test_username_with_spaces(self):
        login_page = LoginPage(self.driver)
        login_page.open()
        login_page.login(" standard_user ", "secret_sauce")
        assert login_page.is_login_success() is False
        error = login_page.get_error_message(timeout=10)
        assert error is not None, "含空格用户名应显示错误消息"
        assert "do not match" in error.lower()

    @allure.story("SQL注入尝试")
    def test_sql_injection(self):
        login_page = LoginPage(self.driver)
        login_page.open()
        login_page.login("' OR 1=1--", "any")
        assert login_page.is_login_success() is False
        error = login_page.get_error_message(timeout=10)
        assert error is not None, "SQL注入应被拒绝并显示错误消息"
        assert "do not match" in error.lower()