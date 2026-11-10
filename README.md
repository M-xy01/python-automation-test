# litemall-test 电商后台管理系统测试实战

与简历"电商后台管理系统测试实战（开源项目 litemall）"对应的真实练习项目。
被测对象：开源电商系统 [litemall](https://github.com/linlinjava/litemall)（Spring Boot + Vue + MySQL）。

## 环境准备

- JDK 8+、Maven、Node.js（部署 litemall 用）
- MySQL 5.7+ / 8.0
- Python 3.8+（跑测试框架用）
- Chrome 浏览器（Selenium 4.6+ 会自动匹配驱动，无需手动下载 chromedriver）
- Allure 命令行（报告用）：`scoop install allure` 或参考 [allure 官网](https://allurereport.org/docs/)

## 部署 litemall（以官方仓库 README 为准）

1. 克隆仓库：`git clone https://github.com/linlinjava/litemall.git`
2. 数据库：在 `litemall-db/sql/` 目录找到建库脚本和数据脚本（litemall.sql），在 MySQL 中创建 `litemall` 库并导入
3. 后端：仓库根目录执行 `mvn install -DskipTests`，然后 `mvn spring-boot:run -pl litemall-all`，默认端口 8080
4. 前端：`cd litemall-admin`，`npm install --registry=https://registry.npmmirror.com`，`npm run dev`，默认端口 9527
5. 打开 http://localhost:9527 ，默认管理员账号 `admin123 / admin123`

> 端口、脚本路径如对不上，以官方 README 为准，并同步修改 `config/config.yaml`。
> 部署过程本身就是练习：Maven 依赖下载失败、MySQL 时区报错、npm 慢，都是面试可讲的问题。

## 框架结构

```
litemall-test
├── config/config.yaml        # 环境配置（地址、账号、数据库）
├── common/
│   ├── base_page.py          # 页面基类：显式等待封装
│   ├── api_client.py         # 接口客户端：登录鉴权、token 统一管理
│   └── db_client.py          # 数据库客户端：MySQL 封装，用例里查库校验数据一致性
├── page_objects/
│   ├── login_page.py         # 登录页 PO
│   └── goods_page.py         # 商品管理页 PO（列表/搜索/新增/编辑/删除）
├── testcases/
│   ├── conftest.py           # driver / api / db fixtures，失败自动截图
│   ├── ui/test_login.py      # UI 登录用例（Excel 数据驱动）
│   ├── api/test_auth_api.py  # 接口用例（鉴权、商品列表）
│   └── api/test_db_check.py  # 数据校验用例（查库核对订单/商品/金额）
├── data/testdata.xlsx        # 测试数据（tools/make_testdata.py 生成）
├── tools/make_testdata.py
└── reports/                  # 报告、截图输出目录
```

## 快速开始

```bash
pip install -r requirements.txt
python tools/make_testdata.py          # 生成 data/testdata.xlsx
pytest testcases -v --alluredir=reports/allure-results
allure serve reports/allure-results    # 查看可视化报告
```

- 有界面模式调试元素定位时直接跑 pytest；服务器/批量跑可 `HEADLESS=1 pytest ...`
- 前后端没启动时 UI 用例会失败——先确认 litemall 已部署

## 面试怎么讲这个项目

- **分层设计**：PO 模式把页面元素和操作封装在 page_objects，用例只写业务流程；页面改版只需改 PO，不动用例
- **数据驱动**：用例逻辑与测试数据分离（Excel），新增场景零代码
- **稳定性**：全程显式等待（WebDriverWait）替代 sleep；用例失败自动截图并附到 Allure 报告
- **接口鉴权**：登录获取 token 后统一注入请求头（X-Litemall-Admin-Token），业务接口复用同一会话
- **数据校验**：接口/UI 操作后用 SQL 核对数据库（订单状态、库存），验证数据一致性。已落地为 `common/db_client.py` + `testcases/api/test_db_check.py`，无需启动被测应用即可跑（直接查 MySQL）
- **举例**：被问"遇到过什么难的问题"——可以讲元素定位不到/加载时序问题 → 分析原因 → 改用显式等待与定位策略解决

## 进阶 TODO（做完可以继续加简历亮点）

- [ ] 跑通全部用例，报告截图留档
- [ ] 用例扩充到 50 条以上（商品搜索、订单状态流转、会员管理等），之后简历可写真实用例数量
- [ ] 商品页 PO 补全（goods_page），覆盖商品上下架场景
- [x] 新增 MySQL 数据校验用例（订单状态/商品上下架/金额一致性，test_db_check.py，4 条已通过）
- [ ] 接入 Jenkins 持续集成，简历可加 CI 关键词
