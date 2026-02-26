import os
import subprocess
import webbrowser
import http.server
import socketserver
import threading
import time

allure_bin_dir = r"C:\Users\Linux\Desktop\DEAR\gupn\allure\bin"
allure_cmd = os.path.join(allure_bin_dir, "allure.bat")

results_dir = "./allure-results"
output_dir = "./reports/allure-report"

os.makedirs(output_dir, exist_ok=True)

print("正在生成 Allure 报告...")
subprocess.run([allure_cmd, "generate", results_dir, "-o", output_dir, "--clean"])

# 切换到报告目录启动 HTTP 服务器
os.chdir(output_dir)

PORT = 8080
handler = http.server.SimpleHTTPRequestHandler

# 在后台线程启动服务器
httpd = socketserver.TCPServer(("", PORT), handler)
thread = threading.Thread(target=httpd.serve_forever)
thread.daemon = True
thread.start()

print(f"报告已生成，访问 http://localhost:{PORT}/ 查看")
webbrowser.open(f"http://localhost:{PORT}/")

# 保持脚本运行，直到用户按 Ctrl+C
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("\n关闭服务器...")
    httpd.shutdown()

# import os
# import subprocess
# import webbrowser

# # 配置路径
# allure_bin_dir = r"C:\Users\Linux\Desktop\DEAR\gupn\allure\bin"
# allure_cmd = os.path.join(allure_bin_dir, "allure.bat")

# # 定义结果目录和输出目录
# results_dir = "./allure-results"
# output_dir = "./reports/allure-report"

# # 确保输出目录存在
# os.makedirs(output_dir, exist_ok=True)

# # 执行 allure generate
# print("正在生成 Allure 报告...")
# subprocess.run([allure_cmd, "generate", results_dir, "-o", output_dir, "--clean"])

# # 完成后打开报告（可选）
# report_index = os.path.join(output_dir, "index.html")
# if os.path.exists(report_index):
#     webbrowser.open(report_index)
#     print(f"报告已生成并打开：{report_index}")
# else:
#     print("报告生成失败，请检查错误信息。")