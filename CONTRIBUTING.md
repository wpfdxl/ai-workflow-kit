# Contributing

Thanks for helping improve AI Workflow Kit.

## What fits here

- Language-agnostic workflow fixes (templates, prompts, checklists, INDEX/archive flow)
- New **sample** profiles under `profiles/` (keep them short and illustrative)
- HFDoc Viewer fixes in `doc/sbdoc_web.py`
- Docs / translations

## What does not fit

- Company-specific product rules or private business table names
- Dumping an entire internal monorepo’s coding standards as the default profile
- Unrelated application source code (point `PROJECT.md` `code_root` at your app instead)

## How to add a profile

1. Copy a close sample under `profiles/<new-id>/`
2. Fill `RULES.md` using `bootstrap/RULES_TEMPLATE.md` section order
3. Add `coding_order.md` and `checklist_编码自检.md`
4. Document it in `profiles/README.md`
5. Optionally add `workspace/_example_*` + `doc/<name>/` for a full walkthrough

Or use `bootstrap/step0_生成项目规范.md` with an AI and PR the generated folder.

## PR checklist

- [ ] No secrets / private URLs
- [ ] Sample profiles stay generic
- [ ] README / profile list updated if you add a sample
- [ ] Viewer still runs: `cd doc && python3 sbdoc_web.py --port 9122`
