import allure

from common.api_client import AdminApiClient
from utils.config_loader import get_config


@allure.feature('认证与商品接口')
class TestAuthApi:
    def test_login_success(self, api_client):
        cfg = get_config()['ui']
        with allure.step('使用正确账号登录'):
            body = api_client.login(cfg['username'], cfg['password'])
        assert body['errno'] == 0
        assert body['data']['token'], '登录成功应返回 token'

    def test_login_wrong_password(self, api_client):
        with allure.step('使用错误密码登录'):
            body = api_client.login('admin123', 'wrong-password')
        assert body['errno'] != 0

    def test_goods_list_without_token(self):
        cfg = get_config()['api']
        with allure.step('不带 token 请求商品列表'):
            client = AdminApiClient(cfg['base_url'], cfg.get('timeout', 10))
            body = client.get('/goods/list', params={'page': 1, 'limit': 10})
        assert body['errno'] != 0, '未登录应被拒绝'

    def test_goods_list_with_token(self, api_client):
        cfg = get_config()['ui']
        with allure.step('登录后请求商品列表'):
            api_client.login(cfg['username'], cfg['password'])
            body = api_client.get('/goods/list', params={'page': 1, 'limit': 10})
        assert body['errno'] == 0
        assert isinstance(body['data'].get('list'), list), '应返回商品列表'
