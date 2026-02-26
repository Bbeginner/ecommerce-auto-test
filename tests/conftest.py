import pytest
from utils.driver_factory import DriverFactory
import yaml
import allure
import os
from datetime import datetime

@pytest.fixture(scope="class", autouse=True)
def driver(request):
    """类级别的 driver fixture，每个测试类只启动一次浏览器，自动应用到所有测试"""
    driver = DriverFactory.get_driver()
    request.cls.driver = driver  # 将 driver 绑定到测试类的类属性
    yield driver
    driver.quit()

@pytest.fixture(scope="session")
def config():
    with open('config/config.yaml', 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    if report.when == "call" and report.failed:
        driver = item.funcargs.get("driver")
        if driver:
            screenshot_dir = "screenshots"
            if not os.path.exists(screenshot_dir):
                os.makedirs(screenshot_dir)
            test_name = item.name
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            screenshot_path = os.path.join(screenshot_dir, f"{test_name}_{timestamp}.png")
            driver.save_screenshot(screenshot_path)
            allure.attach.file(screenshot_path, name="失败截图", attachment_type=allure.attachment_type.PNG)
            print(f"\n截图已保存并附加到 Allure: {screenshot_path}")