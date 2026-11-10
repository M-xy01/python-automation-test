import allure
import pytest
from selenium.webdriver.common.by import By

from page_objects.goods_page import GoodsPage
from utils.config_loader import get_config


@allure.feature('商品管理')
class TestGoods:
    def setup_method(self):
        self.cfg = get_config()['ui']

    @allure.severity('critical')
    @allure.title('商品列表页能正常打开并加载数据')
    def test_goods_list_loads(self, driver):
        page = GoodsPage(driver)
        with allure.step('打开商品列表页'):
            page.open_goods_list(self.cfg['base_url'])
        with allure.step('断言出现商品表格'):
            assert page.find_all(page.TABLE), '商品列表页应渲染出表格'
        assert page.row_count() > 0, '列表应有商品数据'

    @allure.severity('normal')
    @allure.title('按商品编号搜索能过滤列表')
    def test_filter_by_goods_sn(self, driver):
        page = GoodsPage(driver)
        with allure.step('打开商品列表页'):
            page.open_goods_list(self.cfg['base_url'])
        with allure.step('按商品编号 1006002 搜索'):
            page.filter_by_sn('1006002')
            page.click_search()
        with allure.step('断言列表包含该商品编号'):
            assert page.has_goods_sn('1006002'), '搜索结果应包含该商品编号'

    @allure.severity('normal')
    @allure.title('商品在售状态标签取值合法')
    def test_on_sale_tags_valid(self, driver):
        page = GoodsPage(driver)
        with allure.step('打开商品列表页'):
            page.open_goods_list(self.cfg['base_url'])
        with allure.step('读取在售状态标签'):
            tags = page.on_sale_status()
        assert tags, '列表应有在售状态标签'
        invalid = [t for t in tags if t not in ('在售', '未售')]
        assert not invalid, f'存在非法在售标签: {invalid}'

    @allure.severity('blocker')
    @allure.title('新增按钮可点击')
    def test_create_button_enabled(self, driver):
        page = GoodsPage(driver)
        with allure.step('打开商品列表页'):
            page.open_goods_list(self.cfg['base_url'])
        with allure.step('点击新增按钮'):
            page.click_create()
        with allure.step('断言跳转到商品创建页'):
            assert page.url_contains('/goods/create'), '新增应跳转到创建页'

    @allure.severity('normal')
    @allure.title('编辑按钮跳转到商品编辑页')
    def test_edit_button_navigates(self, driver):
        page = GoodsPage(driver)
        with allure.step('打开商品列表页'):
            page.open_goods_list(self.cfg['base_url'])
        with allure.step('点击第一行编辑按钮'):
            page.click_first_row_edit()
        with allure.step('断言跳转到商品编辑页'):
            assert page.url_contains('/goods/edit'), '编辑应跳转到编辑页'

    @allure.severity('critical')
    @allure.title('删除商品后列表不再包含该商品')
    def test_delete_goods(self, driver):
        page = GoodsPage(driver)
        with allure.step('打开商品列表页'):
            page.open_goods_list(self.cfg['base_url'])
        with allure.step('记录第一个商品编号'):
            rows = page.find_all(page.ROWS)
            assert rows, '列表为空，无法执行删除用例'
            target_sn = rows[0].text
        with allure.step('删除该商品并确认'):
            page.click_first_row_delete()
            # el-confirm 弹窗
            confirm = (By.XPATH, "//button[span[text()='确定']]")
            try:
                page.wait.until(
                    lambda d: d.find_elements(*confirm)
                )
                page.click(confirm)
            except Exception:
                pass
        with allure.step('断言该商品已从列表消失'):
            assert not page.has_goods_sn(target_sn.split()[0]), '删除后列表不应再包含该商品'
