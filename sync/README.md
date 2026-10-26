# 项目 → 课程仓库同步机制

> 本课程以真实项目 DV-IAS 为载体。**项目每次更新，课程仓库自动同步对应资料**，
> 保证学生学的是"活的项目"而不是过时讲义。

## 同步范围与映射

| 项目变更 | 同步到课程仓库 | 说明 |
|---|---|---|
| `docs/00~16*.md`（设计/报告/指南） | `project-ref/` | 学生自学引导文引用的原文 |
| `docs/adr/*.md` | `project-ref/` | 决策记录，第 9/11 次课案例 |
| `dv-ias/perf/*`（压测脚本） | `project-ref/perf/` | 第 14 次课素材 |
| `dv-ias/test/e2e_browser.py` | `project-ref/test/` | 第 15 次课素材 |
| `dv-ias/scripts/*` | `project-ref/scripts/` | 运维教学素材 |
| 项目大版本发布（如新子图上线） | 更新 `docs/02-授课计划.md` 对应课次素材行 + CHANGELOG | 由课程维护人执行 |

## 使用方法

```bash
# 在项目根目录（D:\projects\数字乡村）执行：
bash course/sync/sync-from-project.sh
# 脚本自动：拷贝上述范围 → git add → 生成带日期的 commit → 提示 push
```

## 更新约定

1. **文档类**：直接覆盖同步（`project-ref` 是只读镜像，学生不改）
2. **结构性变更**（新增子图/服务/大重构）：课程维护人评估是否调整授课计划后，在 `CHANGELOG.md` 记录
3. **敏感信息**：同步前脚本自动 grep 检查密码/密钥关键字，命中则中止并提示人工处理
4. 同步 commit message 格式：`sync(project): <项目变更摘要> [YYYY-MM-DD]`

## 自动化（可选）

若课程仓库托管在 GitHub，可在项目侧配置定时任务或手动触发本脚本后 push；
仓库 Actions 仅为构建 word/pdf（见 `.github/workflows/build-docs.yml`），不做自动 push，避免误同步。
