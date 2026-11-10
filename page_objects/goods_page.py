from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By

from common.base_page import BasePage


class GoodsPage(BasePage):
    """商品管理页 PO（/goods/list）。

    表格列：商品ID / 商品编号 / 名称 / 专柜价 / 当前价 / 是否新品 / 是否热品 / 是否在售 / 操作(编辑/删除)。
    顶部筛选：商品ID、商品编号、商品名称 + 搜索/新增/批量删除。
    """

    # 顶部筛选区
    GOODS_ID_INPUT = (By.XPATH, "//input[@placeholder='请输入商品ID']")
    GOODS_SN_INPUT = (By.XPATH, "//input[@placeholder='请输入商品编号']")
    NAME_INPUT = (By.XPATH, "//input[@placeholder='请输入商品名称']")
    SEARCH_BTN = (By.XPATH, "//button[span[text()='搜索']]")
    CREATE_BTN = (By.XPATH, "//button[span[text()='新增']]")
    BATCH_DELETE_BTN = (By.XPATH, "//button[span[text()='批量删除']]")

    # 表格
    TABLE = (By.XPATH, "//el-table")
    ROWS = (By.XPATH, "//el-table//tbody/tr")
    NAME_LINK = (By.XPATH, "//a[contains(@href,'/goods/edit')]")
    EDIT_BTN = (By.XPATH, "//button[span[text()='编辑']]")
    DELETE_BTN = (By.XPATH, "//button[span[text()='删除']]")
    ON_SALE_TAG = (By.XPATH, "//el-table//el-tag")

    def open_goods_list(self, base_url):
        self.open(base_url + '/#/goods/list')

    def filter_by_id(self, goods_id):
        self.input(self.GOODS_ID_INPUT, str(goods_id))

    def filter_by_sn(self, goods_sn):
        self.input(self.GOODS_SN_INPUT, str(goods_sn))

    def filter_by_name(self, name):
        self.input(self.NAME_INPUT, str(name))

    def click_search(self):
        self.click(self.SEARCH_BTN)

    def click_create(self):
        self.click(self.CREATE_BTN)

    def click_edit(self):
        self.click(self.EDIT_BTN)

    def click_delete(self):
        self.click(self.DELETE_BTN)

    def click_batch_delete(self):
        self.click(self.BATCH_DELETE_BTN)

    def row_count(self):
        try:
            rows = self.wait.until(
                lambda d: d.find_elements(*self.ROWS)
            )
            return len([r for r in rows if r.is_displayed()])
        except TimeoutException:
            return 0

    def has_goods_sn(self, goods_sn):
        """列表中是否存在指定商品编号。"""
        try:
            self.wait.until(
                lambda d: any(
                    goods_sn in (r.text or '') for r in d.find_elements(*self.ROWS)
                )
            )
            return True
        except TimeoutException:
            return False

    def on_sale_status(self):
        """返回列表中"在售/未售"标签文本列表。"""
        return [tag.text for tag in self.find_all(self.ON_SALE_TAG)]

    def find_all(self, locator):
        try:
            return self.wait.until(lambda d: d.find_elements(*locator))
        except TimeoutException:
            return []

    def click_first_row_edit(self):
        rows = self.find_all(self.ROWS)
        if not rows:
            raise AssertionError('商品列表为空，无可编辑行')
        rows[0].find_element(*self.EDIT_BTN).click()

    def click_first_row_delete(self):
        rows = self.find_all(self.ROWS)
        if not rows:
            raise AssertionError('商品列表为空，无可删除行')
        rows[0].find_element(*self.DELETE_BTN).click()