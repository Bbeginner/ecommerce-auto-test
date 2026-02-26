## 第一阶段详细讲解：地基与蓝图 (Day 1-2)

这个阶段的核心是：**用AI帮你设计项目结构、生成测试用例蓝图，让你不用从零开始想，直接站在AI的肩膀上起步。**


### 📅 **第1天：项目结构搭建（AI当架构师）**

#### **1.1 确定项目骨架**

先打开终端，创建你的项目根目录：

```bash
mkdir ecommerce-auto-test
cd ecommerce-auto-test
```

然后，用VS Code打开这个文件夹。现在我们要决定项目长什么样。**这时候就轮到AI出场了**。

**操作**：打开 **Cursor** 或 **Continue** 的聊天窗口，输入以下Prompt：

> "请帮我设计一个基于Pytest + Selenium的自动化测试项目目录结构，针对电商网站saucedemo.com进行测试。需要使用Page Object模式，包含配置文件、页面对象、测试用例、工具类、测试报告等模块。请给出详细的目录树和每个文件的用途说明。"

AI会给你一个类似这样的输出 ：

```
ecommerce-auto-test/
├── config/
│   └── config.yaml          # 配置文件（URL、超时时间、浏览器等）
├── pages/
│   ├── __init__.py
│   ├── base_page.py         # 页面基类，封装通用操作
│   ├── login_page.py        # 登录页面对象
│   ├── inventory_page.py    # 商品列表页面对象
│   └── cart_page.py         # 购物车页面对象
├── tests/
│   ├── __init__.py
│   ├── conftest.py          # Pytest夹具（如driver初始化和清理）
│   ├── test_login.py        # 登录测试用例
│   ├── test_inventory.py    # 商品测试用例
│   └── test_cart.py         # 购物车测试用例
├── utils/
│   ├── __init__.py
│   ├── driver_factory.py    # WebDriver工厂类
│   └── logger.py            # 日志封装
├── reports/                 # 测试报告存放目录
├── requirements.txt         # 项目依赖
└── pytest.ini               # Pytest配置文件
```

**你只需要照着这个目录树，在VS Code里把文件夹和空文件建好就行。** 这不费脑子，但能让项目看起来很专业。

#### **1.2 编写配置文件**

在`config/config.yaml`里放什么？继续问AI：

> "请给我一个pytest自动化测试项目的config.yaml示例，包含base_url、browser、timeout、headless模式等配置项。"

AI会给出类似：

```yaml
# config/config.yaml
base_url: "https://www.saucedemo.com"
browser: "chrome"  # chrome / firefox / edge
headless: false    # true: 无界面运行, false: 显示浏览器
timeout: 10        # 元素等待超时时间(秒)
```

直接复制进去，搞定。

#### **1.3 生成requirements.txt**

还是同样的方法：

> "请给我一个pytest+selenium自动化测试项目的requirements.txt，包含所有必要的依赖包。"

得到：

```
selenium==4.18.1
pytest==8.0.2
pytest-html==4.1.1
pyyaml==6.0.1
webdriver-manager==4.0.1
```

保存后，在终端运行 `pip install -r requirements.txt`，一键装好所有依赖。


### 📅 **第2天：测试用例生成（AI当产品经理）**

今天的目标是：**不用自己想测试用例，让AI根据需求生成**。

#### **2.1 注册并进入Coze**

打开 [Coze官网](https://www.coze.cn)，用手机号注册登录。Coze是字节跳动的AI应用开发平台，**完全免费**，且支持中文 。

#### **2.2 创建一个"测试用例生成助手"**

在Coze里，点击"创建Bot"，给它起名叫"测试用例设计师"。然后在"人设与回复逻辑"里，粘贴以下Prompt ：

```
你是一名资深的软件测试工程师，精通电商网站的自动化测试设计。
用户会给你一个功能模块的名称，你需要为这个功能设计详细的测试用例。

设计要求：
1. 覆盖正常流程、异常场景、边界值
2. 每个用例包含：用例标题、前置条件、测试步骤、预期结果
3. 用Markdown表格的形式输出
4. 考虑数据驱动测试的可能性，建议测试数据组合

现在，请为SauceDemo网站的【登录功能】设计测试用例。
```

#### **2.3 生成第一个模块的用例**

点击"测试"按钮，Coze就会生成一份相当专业的测试用例表，类似这样 ：

| 用例ID | 用例标题 | 前置条件 | 测试步骤 | 预期结果 |
|--------|----------|----------|----------|----------|
| TC001 | 正常登录 - 标准用户 | 打开登录页面 | 1. 输入用户名 standard_user<br>2. 输入密码 secret_sauce<br>3. 点击Login按钮 | 跳转到商品列表页，页面标题显示"Products" |
| TC002 | 正常登录 - 问题用户 | 打开登录页面 | 1. 输入用户名 problem_user<br>2. 输入密码 secret_sauce<br>3. 点击Login按钮 | 登录成功，但部分图片可能加载失败 |
| TC003 | 异常登录 - 密码错误 | 打开登录页面 | 1. 输入用户名 standard_user<br>2. 输入密码 wrong_password<br>3. 点击Login按钮 | 页面显示错误提示："Epic sadface: Username and password do not match" |
| TC004 | 异常登录 - 用户被锁定 | 打开登录页面 | 1. 输入用户名 locked_out_user<br>2. 输入密码 secret_sauce<br>3. 点击Login按钮 | 页面显示错误提示："Epic sadface: Sorry, this user has been locked out." |
| TC005 | 边界测试 - 空用户名 | 打开登录页面 | 1. 用户名留空<br>2. 输入密码 secret_sauce<br>3. 点击Login按钮 | 页面显示错误提示："Epic sadface: Username is required" |
| TC006 | 边界测试 - 空密码 | 打开登录页面 | 1. 输入用户名 standard_user<br>2. 密码留空<br>3. 点击Login按钮 | 页面显示错误提示："Epic sadface: Password is required" |

**这些就是你后面要写的测试用例**。不用自己想，AI已经帮你覆盖了主要场景。

#### **2.4 生成其他模块的用例**

同样的方法，继续问Coze ：

- "请为SauceDemo的【商品列表功能】设计测试用例（排序、添加到购物车）"
- "请为SauceDemo的【购物车功能】设计测试用例（查看、删除、继续购物）"
- "请为SauceDemo的【结算流程】设计测试用例（填写信息、完成订单）"

每次都会得到一份结构化的用例表格。把所有这些用例整理到一个文档里（比如`test_cases.md`），放在项目根目录。

#### **2.5 准备测试数据（可选）**

如果你想实现数据驱动测试，可以让AI帮你生成测试数据 ：

> "请为SauceDemo的登录测试生成一组测试数据，包含用户名、密码、预期结果，以CSV格式输出。"

AI会输出类似：

```csv
username,password,expected_result
standard_user,secret_sauce,success
locked_out_user,secret_sauce,locked_out
problem_user,secret_sauce,success_but_issues
,secret_sauce,username_required
standard_user,,password_required
```

保存为`data/login_data.csv`，后面写代码时直接用。


### ✅ **第一阶段产出物**

两天下来，你手里应该有这些东西：

1. **完整的项目结构**（目录+空文件）
2. **配置文件**（config.yaml）
3. **依赖清单**（requirements.txt）
4. **测试用例文档**（test_cases.md，包含登录、商品、购物车、结算的全套用例）
5. **测试数据文件**（可选，login_data.csv）

**最关键的是：这些几乎都是AI帮你生成的，你只是做了一些复制粘贴和整理。** 但面试时，这些都是你的项目成果，你可以自信地说：“我设计了完整的测试用例，覆盖了核心业务流程。”


### ⚡ **AI辅助小技巧汇总**

| 任务 | 用哪个AI | 提示词示例 |
|------|----------|------------|
| 设计项目结构 | Cursor/Continue | "帮我设计pytest+selenium项目结构，用Page Object模式" |
| 生成配置文件 | Cursor/Continue | "给一个config.yaml示例，包含URL、浏览器、超时时间" |
| 生成依赖清单 | Cursor/Continue | "生成pytest+selenium的requirements.txt" |
| 生成测试用例 | Coze | "为SauceDemo登录功能设计测试用例" |
| 生成测试数据 | Coze | "为登录测试生成CSV格式的测试数据" |

**现在就可以开始动手了。** 如果遇到AI回答不够理想的情况（比如生成的用例太简单），可以追问："能再补充一些异常场景吗？" 让AI迭代优化 。

第二阶段（核心代码搭建）需要我接着详细讲解吗？











我们先把**第一阶段**彻底收尾，然后无缝进入**第二阶段**。

### ✅ 第一阶段收尾：生成测试用例（用 Coze）
你刚才的步骤非常正确，现在只需要实际操作一下：

1. **打开 Coze 官网**（https://www.coze.cn），注册/登录。
2. **创建 Bot**，命名为“测试用例设计师”，把那段 Prompt 粘贴进去（就是你引用的那个）。
3. **点击“测试”**，它就会输出登录功能的测试用例表格（Markdown 格式）。
4. **复制保存**到项目根目录下的 `test_cases.md` 文件中。
5. **继续生成其他模块**：你可以修改 Prompt 最后一句，例如“请为 SauceDemo 网站的【商品列表功能】设计测试用例”、“【购物车功能】”等等，把生成的用例追加到同一个文档里。

这样你就拥有了全套测试用例，后面写代码时可以直接对照。

---

### 🚀 **第二阶段：核心代码编写（现在开始）**
你的项目骨架已经有了，依赖也已安装。接下来我们填充核心代码。按照计划，我们需要编写：

- `utils/driver_factory.py` – 管理浏览器驱动
- `utils/logger.py` – 日志封装
- `pages/base_page.py` – 页面基类（封装通用操作）
- `pages/login_page.py` – 登录页面对象
- `tests/conftest.py` – pytest 夹具（driver 初始化和清理）
- `tests/test_login.py` – 第一个测试用例（登录）

**我将提供可直接复制粘贴的代码模板**，并标注关键点。你只需依次在对应文件中写入即可。

---

### 1️⃣ `utils/driver_factory.py` – 驱动管理
```python
import yaml
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager

class DriverFactory:
    """根据配置创建 WebDriver 实例"""

    @staticmethod
    def get_driver(config_path='config/config.yaml'):
        with open(config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)

        browser = config.get('browser', 'chrome').lower()
        headless = config.get('headless', False)

        if browser == 'chrome':
            options = webdriver.ChromeOptions()
            if headless:
                options.add_argument('--headless')
            driver = webdriver.Chrome(
                ChromeDriverManager().install(),
                options=options
            )
        elif browser == 'firefox':
            options = webdriver.FirefoxOptions()
            if headless:
                options.add_argument('--headless')
            driver = webdriver.Firefox(
                GeckoDriverManager().install(),
                options=options
            )
        elif browser == 'edge':
            options = webdriver.EdgeOptions()
            if headless:
                options.add_argument('--headless')
            driver = webdriver.Edge(
                EdgeChromiumDriverManager().install(),
                options=options
            )
        else:
            raise ValueError(f"Unsupported browser: {browser}")

        driver.implicitly_wait(config.get('timeout', 10))
        driver.maximize_window()
        return driver
```

---

### 2️⃣ `utils/logger.py` – 日志封装
```python
import logging
import os
from datetime import datetime

class Logger:
    """简单日志封装，输出到控制台和文件"""
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._setup_logger()
        return cls._instance

    def _setup_logger(self):
        log_dir = "logs"
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        log_filename = f"test_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        log_path = os.path.join(log_dir, log_filename)

        self.logger = logging.getLogger("AutoTest")
        self.logger.setLevel(logging.DEBUG)

        # 文件处理器
        file_handler = logging.FileHandler(log_path, encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)
        file_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(file_formatter)

        # 控制台处理器
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_formatter = logging.Formatter('%(levelname)s: %(message)s')
        console_handler.setFormatter(console_formatter)

        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)

    def get_logger(self):
        return self.logger
```

---

### 3️⃣ `pages/base_page.py` – 页面基类
```python
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from utils.logger import Logger

class BasePage:
    """所有页面对象的基类，封装常用操作"""

    def __init__(self, driver):
        self.driver = driver
        self.logger = Logger().get_logger()

    def find_element(self, locator, timeout=10):
        """查找单个元素，显式等待"""
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
        """点击元素"""
        element = self.find_element(locator, timeout)
        element.click()
        self.logger.debug(f"点击元素: {locator}")

    def input_text(self, locator, text, timeout=10):
        """输入文本"""
        element = self.find_element(locator, timeout)
        element.clear()
        element.send_keys(text)
        self.logger.debug(f"向元素 {locator} 输入: {text}")

    def get_text(self, locator, timeout=10):
        """获取元素文本"""
        element = self.find_element(locator, timeout)
        text = element.text
        self.logger.debug(f"获取元素文本 {locator}: {text}")
        return text

    def is_element_visible(self, locator, timeout=5):
        """判断元素是否可见"""
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
            return True
        except TimeoutException:
            return False
```

---

### 4️⃣ `pages/login_page.py` – 登录页面对象
```python
from pages.base_page import BasePage
from selenium.webdriver.common.by import By

class LoginPage(BasePage):
    """登录页面对象"""

    # 页面元素定位
    _username_input = (By.ID, "user-name")
    _password_input = (By.ID, "password")
    _login_button = (By.ID, "login-button")
    _error_message = (By.CSS_SELECTOR, "h3[data-test='error']")

    def __init__(self, driver):
        super().__init__(driver)
        self.url = "https://www.saucedemo.com"

    def open(self):
        """打开登录页面"""
        self.driver.get(self.url)
        self.logger.info("打开登录页面")

    def login(self, username, password):
        """执行登录操作"""
        self.input_text(self._username_input, username)
        self.input_text(self._password_input, password)
        self.click(self._login_button)
        self.logger.info(f"尝试登录: username='{username}', password='{'*'*len(password)}'")

    def get_error_message(self):
        """获取错误提示（如果有）"""
        if self.is_element_visible(self._error_message, timeout=3):
            return self.get_text(self._error_message)
        return None

    def is_login_success(self):
        """判断登录是否成功（通过URL变化）"""
        return "inventory.html" in self.driver.current_url
```

---

### 5️⃣ `tests/conftest.py` – Pytest 夹具
```python
import pytest
from utils.driver_factory import DriverFactory
import yaml

@pytest.fixture(scope="function")
def driver():
    """每个测试用例独立浏览器实例"""
    driver = DriverFactory.get_driver()
    yield driver
    driver.quit()

@pytest.fixture(scope="session")
def config():
    """全局配置"""
    with open('config/config.yaml', 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)
```

---

### 6️⃣ `tests/test_login.py` – 登录测试用例（数据驱动示例）
```python
import pytest
from pages.login_page import LoginPage

class TestLogin:
    """登录功能测试套件"""

    @pytest.mark.parametrize("username,password,expected", [
        ("standard_user", "secret_sauce", "success"),
        ("locked_out_user", "secret_sauce", "locked_out"),
        ("problem_user", "secret_sauce", "success_but_issues"),
    ])
    def test_login_scenarios(self, driver, username, password, expected):
        login_page = LoginPage(driver)
        login_page.open()
        login_page.login(username, password)

        if expected == "success":
            assert login_page.is_login_success() is True
        elif expected == "locked_out":
            error = login_page.get_error_message()
            assert "locked out" in error.lower()
        elif expected == "success_but_issues":
            # problem_user 登录后可能页面异常，这里简单判断登录成功
            assert login_page.is_login_success() is True

    def test_login_empty_username(self, driver):
        login_page = LoginPage(driver)
        login_page.open()
        login_page.login("", "secret_sauce")
        error = login_page.get_error_message()
        assert "Username is required" in error

    def test_login_empty_password(self, driver):
        login_page = LoginPage(driver)
        login_page.open()
        login_page.login("standard_user", "")
        error = login_page.get_error_message()
        assert "Password is required" in error
```

---

### 🔍 现在运行第一个测试
在项目根目录（已激活虚拟环境）执行：
```bash
pytest tests/test_login.py -v --html=reports/report.html
```

如果一切顺利，你会看到浏览器自动打开又关闭，并输出测试结果。同时 `reports/report.html` 会生成一份简单的测试报告。

---

### 📌 接下来你可以：
- 用同样的模式实现 `inventory_page.py`、`cart_page.py` 以及对应的测试用例。
- 参考 Coze 生成的其他模块用例，逐步完善测试覆盖率。
- 后续再集成 Allure 报告、失败截图等功能（第三阶段）。

如果你在编写某个页面对象或测试用例时卡住，随时把问题发过来，我帮你快速解决。


接下来可以做的几件事
1️⃣ 优化测试速度（可选）

    将 driver fixture 的 scope 从 function 改为 class，让一个测试类只启动一次浏览器。但要小心测试间的相互影响（需要清 cookies 或重置状态）。这个可以后续再考虑。

2️⃣ 添加失败截图功能

让测试在失败时自动截图，符合“失败自动截图”的亮点。
3️⃣ 集成 Allure 报告

生成更漂亮的报告，符合简历中“集成 Allure 报告”的描述。
4️⃣ 增加 Page Object 的其他页面

目前只有登录页面，可以继续实现商品列表页、购物车页等，丰富测试覆盖。
5️⃣ 完善项目 README

让 Gitee 项目看起来更专业。。