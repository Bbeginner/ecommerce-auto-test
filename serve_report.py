import os
import subprocess

# 请确认这是你实际的 allure 根目录（到 bin 文件夹）
allure_bin_dir = r"C:\Users\Linux\Desktop\DEAR\gupn\allure\bin"
allure_cmd = os.path.join(allure_bin_dir, "allure.bat")  # Windows 下 allure 或 allure.bat 均可

# 执行 allure serve，自动打开浏览器
subprocess.run([allure_cmd, "serve", "./allure-results"])