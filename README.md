# 数字乡村综合服务平台项目实战（DV-IAS 教学版）

> 德国双元制本土化 · 64 课时 · 高职高专 AI/大数据专业核心课
> 以真实交付工程 DV-IAS（数字乡村综合服务平台）为载体的项目实战课程

[![build-docs](https://github.com/USER/REPO/actions/workflows/build-docs.yml/badge.svg)](.github/workflows/build-docs.yml)

## 仓库结构

| 目录 | 内容 |
|---|---|
| `docs/` | 课程标准、授课计划（64 课时/16 次）、课程教学方案（双元制+费曼+布鲁姆） |
| `ppt/` | 16 次课 PPT（L01~L16.pptx，可直接授课） |
| `slides-md/` | PPT 源稿（如需修改内容，改 `gen_ppt.py` 重新生成） |
| `worksheets/` | 16 张六步法任务单 + 费曼卡 + 小队章程 + 引导文问题清单 |
| `assessments/` | 3 份阶段实作卷 + 答辩评分表 + 任务单验收表 |
| `project-ref/` | 真实项目资料镜像（设计文档 00~16、ADR、压测/E2E 报告）——**只读**，随项目自动同步 |
| `word/` `pdf/` | 全部 md 教学资料的 Word/PDF 版（学生下发用），由 `build_docs.py` 生成 |
| `sync/` | 项目→课程同步脚本与约定（`sync-from-project.sh`） |
| `.github/workflows/` | 推送时自动重建 word/pdf（Actions） |

## 快速开始（教师）

```bash
# 1) 转换/重建教学文档（word + pdf）
pip install xhtml2pdf markdown python-pptx
python build_docs.py && python gen_ppt.py

# 2) 项目有更新后，同步进课程仓库
cd ../ && bash course/sync/sync-from-project.sh && cd course && git push

# 3) 直接授课
#    - 讲义：ppt/L01.pptx ~ L16.pptx
#    - 学生用：word/ 或 pdf/ 下的任务单
#    - 评分：assessments/
```

## 教学模式一句话

**双元制六步法（资讯→计划→决策→实施→检查→评价）组织每次课；每次课 15 分钟费曼互讲；目标与考核对齐布鲁姆认知层；企业导师 5 次驻场（开班/联邦事故复盘/监控/压测/答辩主考，一票否决制）。**

## 与真实项目的关系

本课程载体 DV-IAS 已在生产环境完成验收（详见 `project-ref/14-最终执行报告.md`、
`project-ref/15-融合测试报告.md`）：18 个 K8s 负载在线、GraphQL 联邦网关全链路贯通、
1.058 亿行数据、k6 350VU 压测 0 失败、Playwright E2E 12/12 通过。
学生学习的是**仍在运行、仍在迭代的真实系统**；项目仓库每次更新都会通过 `sync/` 同步到本仓库。

## 许可与使用

- 教学使用自由；请保留"基于真实项目 DV-IAS"的出处说明。
- 项目本体见（校内）`D:\projects\数字乡村`。
