import os
import yaml
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager

class DriverFactory:
    @staticmethod
    def get_driver(config_path='config/config.yaml'):
        # 读取配置文件
        with open(config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)

        browser = config.get('browser', 'chrome').lower()
        headless = config.get('headless', False)
        timeout = config.get('timeout', 10)

        # 初始化 driver 变量为 None
        driver = None

        # ---------- Chrome ----------
        if browser == 'chrome':
            options = webdriver.ChromeOptions()
            if headless:
                options.add_argument('--headless')
            try:
                service = ChromeService(ChromeDriverManager().install())
                driver = webdriver.Chrome(service=service, options=options)
            except Exception as e:
                raise Exception(f"Failed to initialize Chrome driver: {e}")

        # ---------- Firefox ----------
        elif browser == 'firefox':
            options = webdriver.FirefoxOptions()
            if headless:
                options.add_argument('--headless')
            try:
                service = FirefoxService(GeckoDriverManager().install())
                driver = webdriver.Firefox(service=service, options=options)
            except Exception as e:
                raise Exception(f"Failed to initialize Firefox driver: {e}")

        # ---------- Edge ----------
        elif browser == 'edge':
            options = webdriver.EdgeOptions()
            if headless:
                options.add_argument('--headless')
            try:
                service = EdgeService(EdgeChromiumDriverManager().install())
                driver = webdriver.Edge(service=service, options=options)
            except Exception as e:
                raise Exception(f"Failed to initialize Edge driver: {e}")

        # ---------- 不支持的浏览器 ----------
        else:
            raise ValueError(f"Unsupported browser: {browser}")

        # 确保 driver 已初始化
        if driver is None:
            raise RuntimeError("Driver initialization failed for unknown reason")

        # 设置隐式等待和窗口最大化
        driver.implicitly_wait(timeout)
        driver.maximize_window()
        return driver