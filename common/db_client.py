import logging

import pymysql
from pymysql.cursors import DictCursor

from utils.config_loader import get_config

log = logging.getLogger(__name__)


class DbClient:
    """MySQL 封装，用于用例里的数据校验（查库核对订单状态、库存等）。"""

    def __init__(self, cfg=None):
        cfg = cfg or get_config()['db']
        self.cfg = cfg
        self.conn = None
        self.connect()

    def connect(self):
        if self.conn is not None:
            try:
                self.conn.ping(reconnect=True)
                return
            except Exception:
                self.conn = None
        self.conn = pymysql.connect(
            host=self.cfg['host'],
            port=int(self.cfg.get('port', 3306)),
            user=self.cfg['user'],
            password=str(self.cfg.get('password', '')),
            database=self.cfg['database'],
            charset='utf8mb4',
            cursorclass=DictCursor,
            autocommit=True,
        )
        log.debug('connected to mysql %s/%s', self.cfg['host'], self.cfg['database'])

    def _ensure(self):
        if self.conn is None:
            self.connect()
        return self.conn

    def query(self, sql, args=None):
        """执行查询，返回 dict 列表。"""
        conn = self._ensure()
        with conn.cursor() as cur:
            cur.execute(sql, args)
            return cur.fetchall()

    def fetch_one(self, sql, args=None):
        rows = self.query(sql, args)
        return rows[0] if rows else None

    def execute(self, sql, args=None):
        """执行写操作（INSERT/UPDATE/DELETE）。"""
        conn = self._ensure()
        with conn.cursor() as cur:
            affected = cur.execute(sql, args)
        conn.commit()
        return affected

    def close(self):
        if self.conn is not None:
            self.conn.close()
            self.conn = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()