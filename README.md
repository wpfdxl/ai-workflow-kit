# AI Workflow Kit

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

Language-agnostic workflow for AI-assisted feature delivery:

**Requirement → Design Doc → API Contract → Implementation**

Each stage is a file contract. Humans review before the next stage, so the AI only codes against approved context.

中文说明见下方；English summary at the top for discoverability.

---

## Why

AI coding fails most often because context is fuzzy. This kit fixes that by:

1. Freezing each stage into markdown / JSON files
2. Requiring human review between stages
3. Separating **workflow** (language-neutral) from **rules** (`profiles/` per stack)

Copy this repository next to any codebase, pick or generate a profile, then run features through the SOP.

## Features

- 4-stage SOP + templates, prompts, checklists
- Pluggable stack profiles (Go Kratos DDD, FastAPI, Express, Gin, ThinkPHP-style, …)
- `bootstrap/step0` — ask an AI to generate rules for *your* language/framework
- `workspace/` + `doc/` + `archive/` — in-progress vs archived work
- Built-in HFDoc Viewer (`doc/sbdoc_web.py`) for API JSON preview
- Cursor rule: `.cursor/rules/workflow.mdc`

## Quick start（推荐：Clone → 让 AI 初始化）

```bash
git clone <this-repo-url> ai-workflow-kit
cd ai-workflow-kit
# Open this folder in Cursor / your AI IDE
```

1. Paste [`bootstrap/init_接入我的项目.md`](bootstrap/init_接入我的项目.md) to the AI and fill **你的项目信息**（language, framework, `code_root`, …）.
2. The AI creates `profiles/<your-id>/`, updates `PROJECT.md`, and **deletes unrelated samples** (`profiles/*-sample/`, `workspace/_example_*`, matching `doc/` demos).
3. Check [`docs/哪些可以删.md`](docs/哪些可以删.md). Example chat: [`docs/示例对话_初始化.md`](docs/示例对话_初始化.md).
4. Start a real feature under `workspace/<需求名>/` (same name as `doc/<需求名>/`), then run stages via `workspace/_prompts/`.
5. Preview APIs:

```bash
cd doc
python3 sbdoc_web.py --port 9122
```

Guides: [`docs/GETTING_STARTED.md`](docs/GETTING_STARTED.md) · [`docs/入门指南.md`](docs/入门指南.md) · [`docs/PUBLISH.md`](docs/PUBLISH.md)

## Layout

```
ai-workflow-kit/
├── PROJECT.md                 # active profile + code_root
├── bootstrap/                 # step0: generate a new profile
├── profiles/                  # per-stack RULES / coding_order / checklist
├── workspace/                 # feature workbench
│   ├── _templates/ _prompts/ _checklists/
│   ├── _example_*             # 开箱演示；init 后可删
│   └── INDEX.md
├── doc/                       # API JSON + HFDoc Viewer
│   └── archive/
└── archive/                   # archived feature docs
```

初始化后保留/删除清单：[`docs/哪些可以删.md`](docs/哪些可以删.md)。

## Workflow SOP

| Stage | Input | Who | Output |
|---|---|---|---|
| 0 Profile | Your stack description | AI + you | `profiles/<id>/` + `PROJECT.md` |
| 1 Design | `00_需求.md` | AI | `01_开发方案.md` |
| 2 Review design | `01` | You | Approved design |
| 3 API docs | Approved `01` | AI | `02_接口文档.md` + `doc/<feature>/*.json` |
| 4 Code | `01` + `02` + profile | AI | Code + checklists |

Archive when done:

```bash
mkdir -p archive doc/archive
rm -f workspace/<feature>/*接口文档.json
mv workspace/<feature> archive/<feature>
[ -d "doc/<feature>" ] && mv "doc/<feature>" "doc/archive/<feature>"
# update workspace/INDEX.md
```

## Profiles

See [`profiles/README.md`](profiles/README.md). Default in `PROJECT.md`: `go125-kratos-ddd-sample`.

Samples are **illustrative**, not corporate standards. Replace them with your own via step0.

## Contributing

See [`CONTRIBUTING.md`](CONTRIBUTING.md).

## License

[MIT](LICENSE)

---

## 中文摘要

把「需求 → 开发方案 → 接口文档 → 编码」做成**分层文件契约**。  

**接入你的工程**：Clone → 打开本目录 → 把 [`bootstrap/init_接入我的项目.md`](bootstrap/init_接入我的项目.md) 发给 AI（填技术栈与 `code_root`）→ 自动生成规范并删掉无关示例 → 再开真实需求。  

对话范例：[`docs/示例对话_初始化.md`](docs/示例对话_初始化.md)。可删清单：[`docs/哪些可以删.md`](docs/哪些可以删.md)。
