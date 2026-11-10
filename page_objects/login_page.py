from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from common.base_page import BasePage


class LoginPage(BasePage):
    USERNAME_INPUT = (By.XPATH, "//input[contains(@placeholder,'账户') or contains(@placeholder,'用户名') or contains(@placeholder,'账号')]")
    PASSWORD_INPUT = (By.XPATH, "//input[contains(@placeholder,'密码')]")
    LOGIN_BTN = (By.XPATH, "//button[contains(., '登录')]")
    # Element Plus 的错误提示可能是 .el-message（message box）或 .el-notification（右上角通知）
    ERROR_MESSAGE = (By.CSS_SELECTOR, ".el-message, .el-notification, .el-message-box")

    def open_login(self, base_url):
        self.open(base_url + '/#/login')

    def login(self, username, password):
        # 部分登录页没有独立的用户名输入框（只有密码框），找不到时跳过用户名输入，避免整体超时
        if username and self.exists(self.USERNAME_INPUT):
            self.input(self.USERNAME_INPUT, username)
        self.input(self.PASSWORD_INPUT, password)
        self.click(self.LOGIN_BTN)

    def has_error(self):
        try:
            self.wait.until(EC.visibility_of_element_located(self.ERROR_MESSAGE))
            return True
        except TimeoutException:
            return False
