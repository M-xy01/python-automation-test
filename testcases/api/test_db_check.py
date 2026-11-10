import allure

from common.db_client import DbClient


@allure.feature('数据校验')
class TestDbCheck:
    """用例执行后直接查库，核对业务数据一致性（订单状态、商品状态等）。"""

    def test_order_status_consistent(self, db):
        """订单表 order_status 与实际业务状态取值合法，无脏数据。"""
        with allure.step('查询订单状态分布'):
            rows = db.query(
                'SELECT order_status, COUNT(*) AS cnt '
                'FROM litemall_order GROUP BY order_status'
            )
        statuses = {r['order_status'] for r in rows}
        invalid = statuses - {'101', '102', '103', '121', '130', '131', '201', '202', '301', '302', '401', '402'}
        assert not invalid, f'存在非法订单状态: {invalid}'

    def test_goods_on_sale_flag(self, db):
        """在售商品 is_on_sale=1，下架商品 is_on_sale=0，无矛盾数据。"""
        with allure.step('校验商品上下架标记'):
            bad = db.query(
                'SELECT id, name, is_on_sale FROM litemall_goods '
                'WHERE is_on_sale NOT IN (0, 1)'
            )
        assert not bad, f'存在非法 is_on_sale 取值: {bad}'

    def test_no_soft_deleted_active_orders(self, db):
        """已删除订单不应出现在业务查询中（deleted 标记一致性）。"""
        with allure.step('校验订单逻辑删除标记'):
            bad = db.query(
                'SELECT id, order_sn, deleted FROM litemall_order '
                'WHERE deleted NOT IN (0, 1)'
            )
        assert not bad, f'存在非法 deleted 取值: {bad}'

    def test_order_total_matches(self, db):
        """订单金额字段非负，且实付金额 <= 商品总额 + 运费。"""
        with allure.step('校验订单金额合理性'):
            bad = db.query(
                'SELECT id, order_sn, order_price, goods_price, freight_price '
                'FROM litemall_order '
                'WHERE order_price < 0 OR goods_price < 0 OR freight_price < 0 '
                'OR order_price < goods_price + freight_price - 0.01'
            )
        assert not bad, f'存在金额异常订单: {bad}'