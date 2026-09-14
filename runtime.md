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
