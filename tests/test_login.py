import pytest
import allure
from pages.login_page import LoginPage

@allure.feature("登录功能")
class TestLogin:
    def setup_method(self):
        """每个测试方法执行前运行，清理浏览器状态"""
        self.driver.delete_all_cookies()
        self.driver.refresh()
        import time
        time.sleep(1)

    @allure.story("登录场景参数化")
    @allure.title("测试登录场景：{username} / {password}")
    @pytest.mark.parametrize("username,password,expected_status", [
        ("", "secret_sauce", "empty_username"),
        ("standard_user", "", "empty_password"),
        ("standard_user", "secret_sauce", "success"),
        ("performance_glitch_user", "secret_sauce", "success"),
        ("problem_user", "secret_sauce", "success"),
        ("locked_out_user", "secret_sauce", "locked"),
        ("fake_user", "wrong_pwd", "invalid"),
    ])
    def test_login_scenarios(self, username, password, expected_status):
        with allure.step("打开登录页面"):
            login_page = LoginPage(self.driver)
            login_page.open()
        with allure.step(f"输入用户名：{username}，密码：{password}"):
            login_page.login(username, password)
        with allure.step("验证登录结果"):
            if expected_status == "success":
                assert login_page.is_login_success() is True
            elif expected_status == "locked":
                assert login_page.is_login_success() is False
                error = login_page.get_error_message()
                assert "locked out" in error.lower()
            elif expected_status == "empty_username":
                assert login_page.is_login_success() is False
                error = login_page.get_error_message().lower()
                assert "username is required" in error
            elif expected_status == "empty_password":
                assert login_page.is_login_success() is False
                error = login_page.get_error_message().lower()
                assert "password is required" in error
            else:  # invalid
                assert login_page.is_login_success() is False
                error = login_page.get_error_message().lower()
                assert "do not match" in error or "username and password do not match" in error

    @allure.story("空用户名")
    def test_empty_username(self):
        with allure.step("打开登录页面"):
            login_page = LoginPage(self.driver)
            login_page.open()
        with allure.step("输入空用户名和正确密码"):
            login_page.login("", "secret_sauce")
        with allure.step("验证错误提示"):
            assert login_page.is_login_success() is False
            error = login_page.get_error_message().lower()
            assert "username is required" in error

    @allure.story("空密码")
    def test_empty_password(self):
        with allure.step("打开登录页面"):
            login_page = LoginPage(self.driver)
            login_page.open()
        with allure.step("输入正确用户名和空密码"):
            login_page.login("standard_user", "")
        with allure.step("验证错误提示"):
            assert login_page.is_login_success() is False
            error = login_page.get_error_message().lower()
            assert "password is required" in error

    @allure.story("用户名大小写敏感")
    def test_username_case_sensitive(self):
        with allure.step("打开登录页面"):
            login_page = LoginPage(self.driver)
            login_page.open()
        with allure.step("输入大写用户名和正确密码"):
            login_page.login("Standard_User", "secret_sauce")
        with allure.step("验证登录失败"):
            assert login_page.is_login_success() is False
            error = login_page.get_error_message().lower()
            assert "do not match" in error

    @allure.story("密码大小写敏感")
    def test_password_case_sensitive(self):
        with allure.step("打开登录页面"):
            login_page = LoginPage(self.driver)
            login_page.open()
        with allure.step("输入正确用户名和大写密码"):
            login_page.login("standard_user", "Secret_Sauce")
        with allure.step("验证登录失败"):
            assert login_page.is_login_success() is False
            error = login_page.get_error_message().lower()
            assert "do not match" in error

    @allure.story("用户名含前后空格")
    def test_username_with_spaces(self):
        with allure.step("打开登录页面"):
            login_page = LoginPage(self.driver)
            login_page.open()
        with allure.step("输入带空格用户名和正确密码"):
            login_page.login(" standard_user ", "secret_sauce")
        with allure.step("验证登录失败"):
            assert login_page.is_login_success() is False
            error = login_page.get_error_message().lower()
            assert "do not match" in error

    @allure.story("SQL注入尝试")
    def test_sql_injection(self):
        with allure.step("打开登录页面"):
            login_page = LoginPage(self.driver)
            login_page.open()
        with allure.step("输入 SQL 注入语句"):
            login_page.login("' OR 1=1--", "any")
        with allure.step("验证登录失败"):
            assert login_page.is_login_success() is False
            error = login_page.get_error_message().lower()
            assert "do not match" in error