# Getting Started

## Recommended: clone → one prompt to initialize

1. Clone this repo and open **this kit folder** in your AI IDE.
2. Paste [`bootstrap/init_接入我的项目.md`](../bootstrap/init_接入我的项目.md), fill in your stack + `code_root`.
3. The AI creates your profile, updates `PROJECT.md`, and removes demo samples.
4. Verify with [`哪些可以删.md`](哪些可以删.md). Example chat (Chinese): [`示例对话_初始化.md`](示例对话_初始化.md).

## Place the kit

Next to or inside your service repo. Point `PROJECT.md` → `code_root` at the code you will change.

## Profile only (no cleanup)

Use [`bootstrap/step0_生成项目规范.md`](../bootstrap/step0_生成项目规范.md) if samples are already gone.

## Start a feature

After init, create `workspace/<feature>/` + `doc/<feature>/` from `_templates` (same Chinese name). Do not rely on `_example_*` (usually deleted).

## Four stages

1. `workspace/_prompts/step1_生成开发方案.md`
2. Human review checklist
3. `step2_生成接口文档.md`
4. `step3_执行编码.md` + checklists

## Preview APIs

```bash
cd doc && python3 sbdoc_web.py --port 9122
```

## Archive

Move both `workspace/<feature>` and `doc/<feature>` into `archive/` and `doc/archive/`. Update `INDEX.md`.
