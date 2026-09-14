# 交接数据契约

所有文件使用 UTF-8。JSON 的未知值用 null，不填 0 或编造默认值。日期为 YYYY-MM-DD，时间记录时区；事实与预算分开。

## brief.json

字段：destination、origin、start_date、end_date（可 null）、days（正整数）、party（adults、children_ages）、currency、budget_limit_minor（可 null）、pace、transport、must_visit、constraints、confirmed_decisions。
金额以最小货币单位整数存储，例如人民币 17000 元为 1700000 分。没有硬性预算时 limit 为 null。

## evidence.json

- sources：数组；每项有 id（S1 等唯一编号）、url、title、platform、retrieved_at、published_at（可 null）、access（full/partial/blocked）。仅保存公开来源地址，不含访问令牌。
- facts：数组；每项有 id、claim、source_ids、status（verified/reported/unknown）、applies_to_date（可 null）、checked_at、price_basis（不涉价格可 null）。verified 必须有已读取的来源；单一游记体验用 reported。
- media：数组；每项有 id（M1 等）、source_id、local_path（可 null）、caption、usage_note。图片不可用时不虚构路径。

来源示例：{"id":"S1","url":"实际读取到的公开网页地址","title":"标题","platform":"景区官网","retrieved_at":"带时区的 ISO 时间","published_at":null,"access":"full"}。示例值不可原样当作证据。

## plan.json

- days：数组；每项有 day（1 起连续序号）、date（未知为 null）、overnight（住宿城市/夜车等；最后一日可 null）、items（活动数组，各项 time、place、transport、rest、source_ids，可按实际增加字段）。
- budget：数组；每项 label、amount_minor（非负整数）、kind（allocation/quote/estimate）、basis（家庭/每人/每晚等）、source_ids。
- budget_total_minor：整数，等于各项 amount_minor 之和。不要在明细同时计入分类小计和对应子项。
- unresolved：字符串数组，列明尚待核实事项。

## guide.md 与 state.json

guide.md 是唯一正文稿；源编号对应 evidence，真实事实不得只存在于 HTML 而缺失正文/证据。
state.json 记录 stage 状态（pending/in_progress/complete）、每个阶段输入文件的修改时间或哈希、失败原因、未决项、qa 检查及产物路径。仅视觉修改复用正文；修改出行日期或路线后复核受影响的证据和计划。

本契约是最小交接格式，可加字段。缺少具体日期允许相对日程；不得因为契约字段缺失要求用户回答对当前任务无关的问题。

来源可增加 `content_origin`（user/official/platform_ai/author_ai_disclosed/unknown）和 `access_note`（实际读取章节、登录阻断、签名链接限制）。这些字段不改变原有 access 定义；只读到部分正文时仍为 partial。
