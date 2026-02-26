import os
from selenium import webdriver
from selenium.webdriver.edge.service import Service

# 你的驱动路径（请务必替换为你的实际绝对路径）
edge_path = r"C:\Users\Linux\Desktop\DEAR\gupn\ecommerce-auto-test\drivers\msedgedriver.exe"

# 1. 检查路径是否存在
print("文件存在吗？", os.path.exists(edge_path))

# 2. 尝试创建 Service 对象
try:
    service = Service(executable_path=edge_path)
    print("Service 创建成功")
except Exception as e:
    print("Service 创建失败:", e)

# 3. 尝试启动浏览器
try:
    driver = webdriver.Edge(service=service)
    driver.get("https://www.saucedemo.com")
    print("浏览器启动成功")
    driver.quit()
except Exception as e:
    print("浏览器启动失败:", e)