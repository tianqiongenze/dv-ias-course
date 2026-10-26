# -*- coding: utf-8 -*-
"""生成 16 次课 PPT（python-pptx）。
设计：16:9，深蓝主题，每课 8-10 页：封面/目标(布鲁姆)/情境导入/知识讲解×3/
动手实作/费曼环节/小结与产出/作业。
"""
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
import os

BLUE = RGBColor(0x1F, 0x3A, 0x5F)
TEAL = RGBColor(0x0E, 0x7C, 0x7B)
ORANGE = RGBColor(0xE8, 0x6A, 0x33)
GRAY = RGBColor(0x44, 0x44, 0x44)
LIGHT = RGBColor(0xF4, 0xF6, 0xF8)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)

LESSONS = [
    ("L01", "开班与项目全景：数字乡村为什么做、做什么", "L1 走进项目",
     ["素质：数字乡村振兴使命感、企业守则", "知识：DV-IAS 三大端与 1+1+N 定位", "能力：能画出平台全景认知图（理解层）"],
     "情境：你们是 DV-IAS 第 2 期迭代的新员工，第 1 个任务是在 4 课时内看懂这个已上线的系统",
     ["成果参观：大屏 / H5 / 压测报告 0 失败——这不是 PPT 项目", "找茬活动：原始建设方案 5 大缺陷（无量化需求/无选型/区块链提法/无GPU评估/等保一句话）", "组队：4人小队，角色 PO/后端/前端/测试，签小队章程", "企业守则：文档、代码、账号密码不得外传"],
     "实作：小队章程 + 全景认知图（三大端→用户→核心功能）", "费曼题：向搭档讲清平台三大端各给谁用、解决什么问题"),
    ("L02", "架构解码：1+1+N 与 GraphQL Federation", "L1 走进项目",
     ["知识：BDAT 四架构与 8 个子图", "知识：Federation 实体/@key/_resolve_reference", "能力：能独立画出架构图并解释数据流（分析层）"],
     "情境：入职第 2 天，架构师休假前只留给你一句话：'先画图，画对了再动手'",
     ["1+1+N = 1个数字底座 + 1个指挥中枢 + N个场景应用", "GraphQL Federation：schema 合并、实体跨子图组合（party+pointsAccount 一次查询）", "为什么不是单体 REST：限界上下文/独立部署/按需取数", "读图：请求→网关(鉴权/限流)→子图→TiDB/Redis"],
     "实作：画 DV-IAS 架构图 v1（8 子图+网关+存储+数据流）", "费曼题：讲清一个请求从 H5 到数据库的完整旅程"),
    ("L03", "数据底座：TiDB HTAP 与库表设计", "L2 数据底座",
     ["知识：TiDB 为什么能扛 1 亿行", "知识：幂等唯一键设计", "能力：为新场景设计规范 DDL（应用/创造层）"],
     "情境：产品经理要加'农资兑换'功能，第一个问题——表怎么建？",
     ["TiDB = 兼容 MySQL 协议的分布式 NewSQL：HTAP、在线扩缩、强一致", "建表三规：自增主键、created_at 默认当前、业务幂等唯一键 uk_ref", "索引意识：查什么建什么（village_code/state 常用组合）", "反例讲评：字符串主键/缺时间戳/无索引"],
     "实作：设计农资兑换 3 张表（商品/兑换单/流水）+ DDL 脚本", "费曼题：幂等唯一键为什么能防重复发积分"),
    ("L04", "1 亿行数据从哪来：批量生成与预分裂", "L2 数据底座",
     ["知识：SHARD_ROW_ID_BITS 与 PRE_SPLIT_REGIONS", "能力：会跑 K8s Job 并核验行数（应用层）", "素质：生产操作红线意识"],
     "情境：测试部说'没有大数据测不出真问题'——给你 4 课时，把测试库灌到 1 亿行",
     ["K8s Job：跑完即止的批处理（bulk-gen3，4表×6线程）", "SHARD_ROW_ID_BITS=4 打散行 id 热点；PRE_SPLIT_REGIONS=8 预分裂避免写热点", "批量写入：executemany 8000行/批 + commit", "红线：绝不在生产库 TRUNCATE/DROP，操作前必 kubectl get 确认 namespace"],
     "实作：跑 bulk-gen Job + 行数核验记录（COUNT=计划）", "费曼题：预分裂为什么能防写热点"),
    ("L05", "多级缓存与读写分离（阶段实作一）", "L2 数据底座",
     ["知识：L1进程缓存/L2 Redis/网关微缓存", "能力：会加双层缓存并验证命中率（应用/分析层）"],
     "情境：积分榜接口被投诉'打开要 800ms'——压测证明 DB 成了瓶颈",
     ["读路径：L1 TTL(进程内) → L2 Redis Cluster → TiDB 读池", "三防：单飞锁(singleflight)防击穿 / TTL±20%抖动防雪崩 / 空值缓存防穿透", "读写分离：双连接池 rw/ro 双账号（本轮 MVP 账号级）", "命中率验收线：≥90%"],
     "阶段实作一：为积分榜加双层缓存，压测命中率≥90%（占10%）", "费曼题：缓存击穿/雪崩/穿透三者区别与对策"),
    ("L06", "DDD 限界上下文与微服务拆分", "L3 服务构建",
     ["知识：限界上下文/聚合/上下文地图", "能力：能为新业务划分上下文（分析/创造层）"],
     "情境：'农资兑换'该塞进 points 服务，还是独立一个 service？",
     ["事件风暴简化：名词→实体→聚合→上下文→边界", "DV-IAS 8 子图：iam/portal/governance/points/data/agent/mcp/web", "拆分判据：数据所有权不同/变更节奏不同/团队边界", "反模式：共享库当集成层、分布式单体"],
     "实作：画出农资兑换上下文地图 + 聚合设计", "费曼题：为什么积分流水必须归属 points 上下文而不是 iam"),
    ("L07", "GraphQL Schema-first：SDL 契约设计", "L3 服务构建",
     ["知识：SDL 类型系统/mutation/query", "能力：契约先行写 SDL（应用/创造层）"],
     "情境：前后端约好接口再开发——契约就是法律",
     ["Schema-first 流程：SDL→评审→生成/对照实现", "type/Mutation/@key 实体声明", "命名规约：camelCase 字段、reportEvent 动词开头", "对照 DV-IAS：type GovernanceEvent @key(fields:\"id\")"],
     "实作：农资兑换 SDL（RedeemItem/RedeemOrder + redeem/confirmRedeem）", "费曼题：@key 在联邦里的作用——没有它会怎样"),
    ("L08", "Strawberry 子图实现", "L3 服务构建",
     ["能力：实现可冒烟通过的子图（应用/创造层）", "知识：Strawberry 类型装饰器"],
     "情境：SDL 已评审冻结，今天交代码——冒烟不过不算完成",
     ["strawberry.federation.type(keys=[...]) 实体 + _resolve_reference", "Query/Mutation 用 strawberry.federation.type", "db.py 双连接池 + repo 模式", "冒烟门禁：smoke-import.sh IMPORT-OK 才算完成"],
     "实作：农资子图代码 + 本地导入冒烟通过", "费曼题：repo 层为什么要把 SQL 收拢而不是写在 resolver 里"),
    ("L09", "联邦网关与跨域组合（企业导师日）", "L3 服务构建",
     ["分析：生产事故复盘方法论", "评价：能判断自己的实体是否被正确组合"],
     "情境：一次真实的深夜告警——网关突然 400，所有跨域查询失败",
     ["事故链复盘：现象(400)→排查(_service.sdl 无 Party)→根因(未引用实体不进SDL)→修复(Schema(types=[Party]))→沉淀(冒烟加SDL断言)", "实体可见性三条件：@key声明 + 被引用或显式注册 + _resolve_reference", "网关组合失败=全站故障：探针与组合解耦（/healthz 独立 8081）"],
     "实作：农资子图接入 gw，演示 party+redeem 跨域查询录屏", "费曼题：把这次事故用'现象-根因-修复-预防'讲给搭档"),
    ("L10", "国密落地：SM3 与 SM4", "L4 安全合规",
     ["知识：SM3 口令派生/SM4-GCM 字段加密", "能力：为敏感字段加国密保护（应用层）"],
     "情境：等保测评师在场：'手机号明文存储？一票否决'",
     ["登录链路：phone_hash=SM3(phone) 查行；password_hash=SM3-PBKDF2(10000轮)；phone_enc=SM4-GCM", "为什么口令不能 SM3 一轮：彩虹表→必须加盐+迭代", "SM4-GCM：认证加密（nonce+tag），密钥来自 K8s Secret", "合规红线：身份证/位置/健康字段单独库+单独授权"],
     "实作：农资兑换联系人手机号 SM4 加密改造", "费曼题：SM3 哈希查行 vs SM4 加密存储——为什么手机号要两样都做"),
    ("L11", "网关安全与等保三级", "L4 安全合规",
     ["分析：限流桶算法复算", "能力：给接口加鉴权与审计（应用层）"],
     "情境：安全部扫描报告：'接口可被未登录调用、可被伪造身份'",
     ["网关三防线：JWT校验+身份头注入(剥离伪造) / 令牌桶6000per-min-per-user / INTERNAL错误脱敏", "限流算法复算：cap 6000、refill 6000/60000，突发与稳态各能过多少", "等保三级映射：身份鉴别/访问控制/安全审计→MCP 工具调用全落库 mcp_audit"],
     "实作：农资接口加 require_user + 审计记录", "费曼题：为什么网关不信任任何客户端传来的身份头"),
    ("L12", "K8s 部署：从 Dockerfile 到 Deployment", "L5 部署运维",
     ["能力：独立完成服务上线（应用/创造层）", "知识：探针/HPA/资源配额"],
     "情境：代码写完了——上线的仪式感：kubectl apply 那一刻",
     ["链路：Dockerfile→build→push 私有Registry→Deployment→Service→探针", "探针事故：readiness 打在 GraphQL 端口返回400 → CrashLoop → 独立 /healthz:8081", "资源三件套：requests/limits/priorityClassName；HPA CPU 60% 2→6", "清单即文档：20-services.yaml 就是生产说明书"],
     "实作：农资服务 Deployment+Service+探针清单，pod Running 截图", "费曼题：liveness 与 readiness 职责区别——配错了各会发生什么"),
    ("L13", "监控可观测（企业导师日）", "L5 部署运维",
     ["能力：接入 Prometheus 并自建看板（应用层）", "知识：四个黄金信号"],
     "情境：没有监控的服务=盲飞；今天给农资服务装上仪表盘",
     ["四个黄金信号：延迟/流量/错误/饱和度", "Prometheus 抓取链：ServiceMonitor(label metrics=true)→/metrics→Grafana", "踩坑：JSONResponse 序列化 metrics 会转义引号→必须 Response 直出", "DV-IAS 实测：7/7 targets UP"],
     "实作：农资服务 ServiceMonitor + 自建 Grafana 看板（至少2个面板）", "费曼题：延迟/流量/错误/饱和度——在你们看板上分别对应哪块图"),
    ("L14", "压测实战：k6+Locust（企业导师日·阶段实作三）", "L5 部署运维",
     ["能力：独立完成压测并出报告（分析/评价层）", "知识：容量工程与拐点法"],
     "情境：领导问'能扛多少人？'——不许说'大概'，拿数据说话",
     ["k6：场景化(browse ramping-vus / report constant-vus) + thresholds 门槛", "Locust：Python 用户行为建模，headless 出分位报告", "实测：350VU 20.6万req 0失败 p95=355ms；150用户 3894req 0失败", "方法论：阶梯加压找拐点，拐点流量≥目标×1.5 才算余量合格"],
     "阶段实作三：农资接口压测报告（含瓶颈定位）（占10%）", "费曼题：你的接口瓶颈在 CPU/DB/锁？证据是什么"),
    ("L15", "质量闭环：Playwright E2E 与融合测试", "L6 质量与交付",
     ["能力：写自动化 E2E 并全量回归（应用/评价层）", "知识：测试金字塔与验收口径"],
     "情境：人工回归一次 2 小时，每次发版都提心吊胆——自动化吧",
     ["E2E 12 用例全景：三端渲染/登录/上报/流转/积分幂等/联邦/问答/拦截", "测试金字塔：单元(快、多)→集成→E2E(慢、少、关键路径)", "数据准备：1.058亿行背景数据让 E2E 更接近真实", "验收口径：P0 100% / P1≥98%"],
     "实作：为农资场景写 3 条 E2E + 全量回归报告", "费曼题：E2E 和单元测试各防什么问题——为什么不能全用 E2E"),
    ("L16", "综合答辩与双元评价（企业导师日）", "L6 质量与交付",
     ["评价：能按验收标准陈述与答辩（评价/创造层）"],
     "情境：今天你是乙方，评委是甲方+监理——按企业验收来",
     ["答辩结构：功能演示4min + 架构讲述2min + 数据与测试2min", "评分：功能40/工程30/表达15/应变15；企业导师一票否决制", "必答题类型：故障应急（如：网关全400你第一步做什么）", "课程闭环：优秀作品进入课程案例库，反哺下一期"],
     "产出：答辩 PPT + 双元验收单", "费曼题（压轴）：把整个项目讲给'完全外行'听懂"),
]


def add_title_slide(prs, lid, title, domain):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    bg = s.shapes.add_shape(1, Inches(0), Inches(0), Inches(13.33), Inches(7.5))
    bg.fill.solid(); bg.fill.fore_color.rgb = BLUE; bg.line.fill.background()
    tb = s.shapes.add_textbox(Inches(0.8), Inches(2.2), Inches(11.7), Inches(2))
    tf = tb.text_frame; tf.word_wrap = True
    p = tf.paragraphs[0]; r = p.add_run(); r.text = title
    r.font.size = Pt(34); r.font.bold = True; r.font.color.rgb = WHITE
    p2 = tf.add_paragraph(); r2 = p2.add_run()
    r2.text = "数字乡村综合服务平台项目实战 ｜ %s ｜ %s" % (lid, domain)
    r2.font.size = Pt(16); r2.font.color.rgb = RGBColor(0xBE, 0xD2, 0xE8)
    return s


def add_bullets(slide, title, items, x=Inches(0.6), y=Inches(1.3), w=Inches(12.1), color=GRAY, size=17, title_color=BLUE):
    tb = slide.shapes.add_textbox(x, y, w, Inches(5.6))
    tf = tb.text_frame; tf.word_wrap = True
    p = tf.paragraphs[0]; r = p.add_run(); r.text = title
    r.font.size = Pt(22); r.font.bold = True; r.font.color.rgb = title_color
    for it in items:
        p = tf.add_paragraph(); r = p.add_run(); r.text = "• " + it
        r.font.size = Pt(size); r.font.color.rgb = color
        p.space_after = Pt(8)
    return tb


def header_bar(slide, text, sub=""):
    bar = slide.shapes.add_shape(1, Inches(0), Inches(0), Inches(13.33), Inches(1.0))
    bar.fill.solid(); bar.fill.fore_color.rgb = BLUE; bar.line.fill.background()
    tf = bar.text_frame; tf.word_wrap = True
    p = tf.paragraphs[0]; r = p.add_run(); r.text = text
    r.font.size = Pt(20); r.font.bold = True; r.font.color.rgb = WHITE
    if sub:
        p2 = tf.add_paragraph(); r2 = p2.add_run(); r2.text = sub
        r2.font.size = Pt(11); r2.font.color.rgb = RGBColor(0xBE, 0xD2, 0xE8)


def gen(lid, title, domain, goals, scene, contents, practice, feynman):
    prs = Presentation()
    prs.slide_width = Inches(13.33); prs.slide_height = Inches(7.5)
    add_title_slide(prs, lid, title, domain)

    # 目标（布鲁姆）
    s = prs.slides.add_slide(prs.slide_layouts[6]); header_bar(s, "学习目标（布鲁姆分层）", lid)
    tb = s.shapes.add_textbox(Inches(0.6), Inches(1.3), Inches(12.1), Inches(5.5))
    tf = tb.text_frame; tf.word_wrap = True
    levels = ["素质目标", "知识目标（记忆/理解）", "能力目标（应用/分析/评价/创造）"]
    for grp, lv in zip(goals, levels):
        p = tf.paragraphs[0] if grp == goals[0] and tf.paragraphs[0].runs == [] else tf.add_paragraph()
        r = p.add_run(); r.text = "◆ " + lv; r.font.size = Pt(18); r.font.bold = True; r.font.color.rgb = TEAL
        p2 = tf.add_paragraph(); r2 = p2.add_run(); r2.text = grp; r2.font.size = Pt(15); r2.font.color.rgb = GRAY
        p2.space_after = Pt(10)

    # 情境导入
    s = prs.slides.add_slide(prs.slide_layouts[6]); header_bar(s, "情境导入（资讯）", "德国双元制 · 完整行动")
    box = s.shapes.add_shape(1, Inches(0.6), Inches(1.5), Inches(12.1), Inches(1.6))
    box.fill.solid(); box.fill.fore_color.rgb = LIGHT; box.line.color.rgb = TEAL
    tfx = box.text_frame; tfx.word_wrap = True
    r = tfx.paragraphs[0].add_run(); r.text = scene; r.font.size = Pt(17); r.font.italic = True; r.font.color.rgb = BLUE
    add_bullets(s, "本课任务", ["阅读引导文，回答 3 个关键提问", "明确本次课要交付的工件"], y=Inches(3.4))

    # 知识讲解
    s = prs.slides.add_slide(prs.slide_layouts[6]); header_bar(s, "知识要点", "讲给你听 · 讲给别人听")
    add_bullets(s, "核心内容", contents, size=16)

    # 动手实作
    s = prs.slides.add_slide(prs.slide_layouts[6]); header_bar(s, "动手实作（计划→决策→实施）", "产出即证明")
    box = s.shapes.add_shape(1, Inches(0.6), Inches(1.5), Inches(12.1), Inches(2.2))
    box.fill.solid(); box.fill.fore_color.rgb = RGBColor(0xFD, 0xF0, 0xE7); box.line.color.rgb = ORANGE
    r = box.text_frame.paragraphs[0].add_run(); r.text = "★ 本次课工件：" + practice
    r.font.size = Pt(19); r.font.bold = True; r.font.color.rgb = ORANGE
    add_bullets(s, "实施要求", ["六步法任务单同步填写（worksheets/%s）" % lid, "自检表全项通过才算完成", "同伴走查后签字"], y=Inches(4.0))

    # 费曼
    s = prs.slides.add_slide(prs.slide_layouts[6]); header_bar(s, "费曼学习环节（15分钟）", "讲不清 = 没学会")
    box = s.shapes.add_shape(1, Inches(0.6), Inches(1.5), Inches(12.1), Inches(1.5))
    box.fill.solid(); box.fill.fore_color.rgb = RGBColor(0xE8, 0xF4, 0xF1); box.line.color.rgb = TEAL
    r = box.text_frame.paragraphs[0].add_run(); r.text = "★ " + feynman
    r.font.size = Pt(18); r.font.bold = True; r.font.color.rgb = TEAL
    add_bullets(s, "规程", ["两人一组：讲3分钟→听众提1个'为什么'→填费曼卡", "卡点登记≥2次的概念：下节课开头重讲"], y=Inches(3.3))

    # 小结
    s = prs.slides.add_slide(prs.slide_layouts[6]); header_bar(s, "小结与检查", "检查(Evaluieren) → 评价(Bewerten)")
    add_bullets(s, "本次课小结", [
        "对照学习目标自检：知识讲得出 / 工件交得出",
        "任务单 + 费曼卡下课前提交（成长档案）",
        "下次课预告：见授课计划（docs/02）",
        "课程仓库：随项目更新自动同步（sync/）",
    ])

    out = os.path.join("ppt", "%s.pptx" % lid)
    prs.save(out)
    return out


if __name__ == "__main__":
    os.makedirs("ppt", exist_ok=True)
    for args in LESSONS:
        path = gen(*args)
        print("OK", path)
    print("DONE", len(LESSONS), "lessons")
