# Travel Guide Pipeline · 旅行攻略制作链路

将多平台旅行资料采集、行程核验与攻略书写、本地 HTML 制作串成可续作的 Agent Skill。

## 工作流

1. **资料采集**：收集公开网页与可用平台查询，记录来源、时间、价格口径及未决事项。
2. **攻略编写**：核对路线、时间、预算和引用，生成结构化计划与 Markdown 正文。
3. **本地 HTML**：制作离线可读、手机适配、可打印的旅行手册，并执行内容与视觉验收。

支持完整制作、单阶段运行、更新旧攻略和跨轮续作。

## 安装

```sh
npx skills add https://github.com/xiaohuizli/travel-guide-pipeline --skill travel-guide-pipeline
```

也可将本仓库目录放入 Agent 的 skills 目录。

## 调用

```text
使用 $travel-guide-pipeline，根据我提供的目的地、日期、同行人数、预算与节奏，制作可离线阅读和打印的 HTML 旅行攻略。保留来源，明确尚未核实的信息。
```

## 平台与运行环境

技能本身不包含平台账户、API Key、采集服务或第三方 CLI。小红书、同程、携程适配器为可选方案，详见 [collect.md](collect.md)；没有可用适配器时采用已有搜索和浏览器工具，并明确访问缺口。马蜂窝采用可访问网页采集。

这条链路按需借鉴 `travel-planner` 的行程规划、`content-research-writer` 的证据组织和 `frontend-design` 的单文件页面设计；浏览器或 Playwright 用于实际页面验收。它们是可选辅助技能，不会将上游技能内容复制进本仓库，缺失时按本技能的阶段规则继续执行。来源与固定版本见 [pipeline.json](pipeline.json)。

`check_plan.py` 和 `doctor.py` 仅依赖 Python 3 标准库。资料查询需要网络；HTML 验收需要可用浏览器工具。可选的 `tripai_query.py` 只做携程 API 查询，凭据从环境变量或 macOS 钥匙串读取，不写入仓库。

## 数据与检查

数据约定见 [data-contract.md](data-contract.md)。中间文件保存在当前任务工作区，个人行程与凭据不写入技能目录。

```sh
python3 check_plan.py /path/to/travel-work-dir
```

脚本检查部分结构、日期、预算和来源引用一致性，不能替代事实核实、路线可行性判断或 HTML 视觉检查。第三方平台接口未随技能发布进行实测。

## 范围

技能不执行购票、付款、账号注册或社交平台发布。用户参考文档中的指令不作为执行授权。

## 浏览器采集与依赖配置

默认使用可用浏览器采集小红书、马蜂窝、携程、同程，详情见 [runtime.md](runtime.md)。执行 `python3 doctor.py` 检查本地依赖；网页登录、API 调用及 HTML 渲染需现场验证。仅在使用携程 API 适配器时才需要 API Key，凭据只存环境变量或 Keychain。
