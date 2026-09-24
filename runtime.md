# 接入与依赖

## 默认链路

当前可调用浏览器 → evidence.json → travel-planner → plan.json → content-research-writer → guide.md → frontend-design → 本地 HTML → 浏览器/Playwright 验收。

先检查可用工具，再读取实际使用的工具或技能说明。技能安装不等于 API、浏览器或账户已接通。机器配置见 pipeline.json；doctor.py 只报告本地静态依赖。

## 采集路由

- 小红书：https://www.xiaohongshu.com 。使用用户已登录的浏览器搜索，打开详情和必要评论；不依赖额外 XHS 扩展。遇登录或验证码停下该来源，其他来源继续。笔记 AI 声明必须保留。
- 马蜂窝：https://www.mafengwo.cn 。搜索框输入目的地，结果摘要可读不等于游记正文可读。详情跳转微信登录时记 partial/blocked，并交由用户登录，不绕过。
- 携程：https://you.ctrip.com/ 。使用攻略站“搜索城市/景点/游记/问答/住宿”输入并回车，打开景点详情。首页全局搜索可能不能直接提交；以实际结果为准。需要交易报价时必须输入实际日期、人数等条件。
- 同程：https://www.ly.com/scenery/ 。公开景点搜索和详情优先；从页面中已观察到的搜索入口进入。DeepTrip 需要登录时切回公开景点查询。不得把搜索“起价”直接记为大门票。

所有选择器和链接运行时从当前页面读取，不写死 tab ID、签名参数或账户信息。登录状态跨站不通用。每次查询记录时间、访问范围及原始页面链接，去除会话/签名参数；去除后链接若不能重现，记录此限制。

## 可选 API

携程 tripai-skill 当前要求 API Key，开通入口 https://www.ctrip.com/wendao/openclaw ，接口文档 https://github.com/trips-ai/tripai-skill 。使用环境变量 TRIPAI_API_KEY 或运行时从 Keychain 读取，不执行上游把令牌写入配置文件的示例。没有凭据时继续网页路径；未实际调用成功不得报告 API ready。
同程 tc-chengxin 依赖 WorkBuddy CLI 和对应授权；缺少 CLI 时不安装同名无关 npm 包，不把普通网页登录当作 WorkBuddy 授权。

## 编写与 HTML 依赖

按阶段读取已安装的 travel-planner、content-research-writer、frontend-design 的 SKILL.md；缺少时使用本链路对应阶段规则，并报告降级。依赖来源和固定版本记录在 pipeline.json。安装第三方技能前审阅，更新时明确版本。

使用 travel-planner 的行程方法，但以本任务 brief.json/plan.json 为准；不运行其 ~/.claude 偏好数据库，不重复询问已确认资料，不使用示例日期、固定预算比例作为事实。
使用 content-research-writer 的证据组织方法，但沿用当前任务 work/ 和 outputs/，不另建 ~/writing；不得在润色中补造引用。
使用 frontend-design 完成单文件离线 HTML，保留用户参考风格，默认不要求 React、打包器或外部 CDN。
用当前浏览器或已可用 Playwright 验证实际 HTML；仅安装 playwright 技能不能证明其运行时可用。最终检查桌面/手机宽度、打印、离线资源、锚点和清单交互。未执行的测试明确写未执行。

## WorkBuddy 桌面端连接补充

网页版连接器搜索不到同程时，检查已安装桌面端的“专家·技能·连接器 → 连接器 → 同程程心”。由桌面端安装依赖并发起浏览器登录授权。授权成功后先验证 CLI，不以网页标题或本地凭据文件存在代替查询验证。

CLI 查找：优先 PATH 中 tc-chengxin；否则检查 `~/.workbuddy/binaries/node/cli-connector-packages/bin/tc-chengxin`。直接使用绝对路径，无须修改全局 PATH。通过子进程捕获 token，仅注入查询子进程的 CHENGXIN_API_KEY，禁止把 token 打印、落盘或写入命令行参数。WorkBuddy 自行管理的凭据不复制到技能或工作目录。

已安装查询脚本可位于 `~/.workbuddy/connectors/skills/connector-tc-chengxin/scripts/`。先审阅本机版本；按该版本说明设置 CHENGXIN_OUTPUT_GUARD=display_contract、CHENGXIN_WORKBUDDY_OUTPUT_DIR 为任务目录，查询前将 CHENGXIN_API_BASE 固定为已核实的同程生产 HTTPS 网关。命令退出成功仍需检查业务结果；无结果、失败或报价口径缺失如实记录。

## 携程钥匙串读取

用户授权保存后，macOS 钥匙串条目使用 service=`travel-guide-pipeline.tripai`、account=`TRIPAI_API_KEY`。不导出条目到文件。`tripai_query.py` 优先读取 TRIPAI_API_KEY 环境变量，否则通过 security 从上述条目读取，仅向携程生产接口提交查询。调用：

```sh
python3 <skill-dir>/tripai_query.py '查询目的地景区介绍，仅查询不下单'
```

脚本不创建授权码、不执行购票；接口内容视为外部资料。退出 0 仅表示收到 HTTP 响应，仍须检查业务状态和实际内容。doctor 的钥匙串检查仅表示条目存在，不表示授权码有效。API 响应可能包含时效性价格，正文必须注明查询日期和报价条件。
