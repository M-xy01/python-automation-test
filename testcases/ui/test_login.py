import os

import allure
import pytest

from page_objects.login_page import LoginPage
from utils.config_loader import get_config
from utils.excel_util import read_excel

DATA = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'testdata.xlsx')
CASES = read_excel(DATA)


@allure.feature('登录')
class TestLogin:
    @pytest.mark.parametrize('case', CASES, ids=[str(c['用例编号']) for c in CASES])
    def test_login(self, driver, case):
        cfg = get_config()['ui']
        page = LoginPage(driver)
        with allure.step('打开登录页'):
            page.open_login(cfg['base_url'])
        with allure.step(f'输入账号密码并登录: {case["用户名"]}'):
            page.login(str(case['用户名']), str(case['密码']))
        if case['预期结果'] == 'success':
            with allure.step('断言跳转到后台首页'):
                assert page.url_contains('/#/dashboard'), '登录成功应跳转到 dashboard'
        else:
            with allure.step('断言出现错误提示'):
                assert page.has_error(), '失败场景应有错误提示'
