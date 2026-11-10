import os

from openpyxl import Workbook

CASES = [
    ('用例编号', '用户名', '密码', '预期结果'),
    ('login_01', 'admin123', 'admin123', 'success'),
    ('login_02', 'admin123', 'wrong123', 'fail'),
    ('login_03', '', 'admin123', 'fail'),
    ('login_04', 'admin123', '', 'fail'),
    ('login_05', 'no_such_user', 'admin123', 'fail'),
]

out_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
os.makedirs(out_dir, exist_ok=True)
wb = Workbook()
ws = wb.active
ws.title = '登录用例'
for row in CASES:
    ws.append(row)
wb.save(os.path.join(out_dir, 'testdata.xlsx'))
print('已生成 data/testdata.xlsx，共', len(CASES) - 1, '条用例')
