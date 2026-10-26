# 项目（DV-IAS）→ 课程仓库 同步说明（项目侧视图）

> 课程仓库：https://github.com/tianqiongenze/dv-ias-course
> 本项目（D:\projects\数字乡村）每次更新后，按以下约定同步到课程仓库。

## 一键同步

```bash
# 在项目根目录执行：
bash course/sync/sync-from-project.sh
# 输出会提示是否产生新 commit；随后：
cd course && git push
```

## 同步映射（自动）

| 项目变更 | → 课程仓库 |
|---|---|
| `docs/0*.md`、`docs/1*.md`（16 册文档） | `project-ref/` |
| `docs/adr/*.md` | `project-ref/adr/` |
| `dv-ias/perf/*`（k6/locust 脚本） | `project-ref/perf/` |
| `dv-ias/test/*.py`（E2E） | `project-ref/test/` |
| `dv-ias/scripts/*.sh` | `project-ref/scripts/` |

脚本内置**敏感信息扫描**（密码/密钥关键字命中即中止），保证学生仓库无生产凭证。

## 人工评估项（结构性变更时）

若项目发生**结构性变更**（新增子图、架构调整、新增真实事故案例），课程维护人应：

1. 评估是否更新 `docs/02-授课计划.md`（如第 9 次课企业日的新案例）
2. 视需要更新对应 PPT（改 `gen_ppt.py` 后重新生成）
3. 在课程仓库 `CHANGELOG.md` 记录一行
4. commit 格式：`sync(project): <摘要> [日期]`

## 仓库 CI

课程仓库推送后 GitHub Actions 自动重建 `word/` + `pdf/`（build-docs workflow），
无需本地转换即可向学生分发最新印刷版。

## 当前同步状态

- 2026-10-26：初始同步 —— 项目 docs 00-16 全量 + ADR-007 + perf/test/scripts 素材 ✅
