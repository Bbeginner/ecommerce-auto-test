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
                options.add_argument('--no-sandbox')           # 关键：解决权限问题
                options.add_argument('--disable-dev-shm-usage') # 关键：解决共享内存不足
                options.add_argument('--disable-gpu')          # 可选，某些环境需要
                options.add_argument('--remote-debugging-port=9222')  # 可选
            # 优先使用环境变量指定的 chromedriver 路径（CI 中设置）
            chromedriver_path = os.environ.get('CHROMEDRIVER_PATH')
            # 公共日志路径
            log_path = "./chromedriver.log"

            if chromedriver_path and os.path.exists(chromedriver_path):
                service = Service(os.environ.get('CHROMEDRIVER_PATH', '/usr/local/bin/chromedriver'))
                driver = webdriver.Chrome(service=service, options=options)
                # service = ChromeService(
                #     executable_path=chromedriver_path,
                #     service_args=['--verbose', f'--log-path={log_path}']
                # )
                # driver = webdriver.Chrome(service=service, options=options)
            else:
                try:
                    service = ChromeService(
                        ChromeDriverManager().install(),
                        service_args=['--verbose', f'--log-path={log_path}']
                    )
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
            # 优先使用本地驱动
            local_driver_path = os.path.join(os.path.dirname(__file__), '..', 'drivers', 'msedgedriver.exe')
            if os.path.exists(local_driver_path):
                service = EdgeService(executable_path=local_driver_path)
                driver = webdriver.Edge(service=service, options=options)
                print(f"使用本地 Edge 驱动: {local_driver_path}")
            else:
                # 本地驱动不存在，尝试自动下载
                try:
                    service = EdgeService(EdgeChromiumDriverManager().install())
                    driver = webdriver.Edge(service=service, options=options)
                except Exception as e:
                    raise Exception(f"无法自动下载 Edge 驱动，请检查网络或手动放置驱动到 drivers/ 目录。原始错误: {e}")

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