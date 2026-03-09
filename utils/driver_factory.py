import yaml
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService

class DriverFactory:
    @staticmethod
    def get_driver(config_path='config/config.yaml'):
        with open(config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)

        browser = config.get('browser', 'chrome').lower()
        headless = config.get('headless', False)
        timeout = config.get('timeout', 10)

        if browser == 'chrome':
            options = webdriver.ChromeOptions()
            if headless:
                options.add_argument('--headless')
            # 检查环境变量 CHROMEDRIVER_PATH
            chromedriver_path = os.environ.get('CHROMEDRIVER_PATH')
            if chromedriver_path:
                service = ChromeService(executable_path=chromedriver_path)
                driver = webdriver.Chrome(service=service, options=options)
            else:
                service = ChromeService(ChromeDriverManager().install())
                driver = webdriver.Chrome(service=service, options=options)

        elif browser == 'firefox':
            options = webdriver.FirefoxOptions()
            if headless:
                options.add_argument('--headless')
            service = FirefoxService(GeckoDriverManager().install())
            driver = webdriver.Firefox(service=service, options=options)

        elif browser == 'edge':
            options = webdriver.EdgeOptions()
            if headless:
                options.add_argument('--headless')
            # 请务必将此路径改为你的实际绝对路径
            edge_driver_path = r"C:\Users\Linux\Desktop\DEAR\gupn\ecommerce-auto-test\drivers\msedgedriver.exe"
            service = Service(executable_path=edge_driver_path)
            driver = webdriver.Edge(service=service, options=options)

        else:
            raise ValueError(f"不支持的浏览器: {browser}")

        driver.implicitly_wait(timeout)
        driver.maximize_window()
        return driver