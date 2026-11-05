# Harness packaging audit

Checked 2026-11-05. Current plugin version: `1.4.0`. Native installation checks below establish the `1.0.1` packaging baseline. Packaging contracts are unchanged; the current bundle includes the exact native painter, PNG export, a metadata-described example gallery, and mandatory four-format delivery. Version `1.4.0` repeats both strict Claude validators and all resource/manifest identity tests. This audit concerns connected distribution and native package discovery; it is separate from the offline skill instructions. No model inference was needed for these checks.

| Harness | Required package contract | Result and evidence |
| --- | --- | --- |
| Codex / ChatGPT Desktop | `.agents/plugins/marketplace.json`, a plugin manifest, and packaged `skills/<name>/SKILL.md` | Repository marketplace uses a local source within its checkout. Portable and Codex compatibility manifests are included. Native HTTPS marketplace registration and plugin installation were verified in an isolated profile. |
| Claude Code | Standalone `.claude/skills/<name>/SKILL.md`, or native `.claude-plugin/marketplace.json` plus a standard plugin `skills/` tree | Added native marketplace and plugin manifests. Claude Code `2.1.233` passed both strict validators, registered the local marketplace, installed version `1.0.1`, and listed it enabled in an isolated profile. The cached skill passed integrity verification. |
| Kimi Code CLI | A complete named skill directory, discovered in a skill root or selected by `--skills-dir` | Directory layout, frontmatter, native user/project destinations, and resource integrity pass the shared tests. The explicit parent directory is `plugins/c4-mermaid/skills`. Native Kimi CLI execution was not tested because that runtime is not installed. |
| DeepSeek Harness | A complete skill directory provided by the filesystem skill provider | The installed `@deepseek-ai/dsh-skill-filesystem` `0.2.1-rc.2` discovered and loaded the generated skill with its resource directory intact. User/project installation paths also pass the shared tests. |

Kimi's executable-tool `plugin.json` and DSH's application/plugin composition mechanisms are distinct from a portable instruction skill. This package does not register the OpenAI manifest as a native plugin in those hosts or install unnecessary executable-tool adapters. Use the standalone skill installer for Kimi and DSH.

The standalone Claude invocation is `/c4-mermaid`; the plugin invocation is `/c4-mermaid:c4-mermaid`. Native resource paths stay within the installed skill directory. All three plugin manifests share name, version, description, and author, and packaging tests compare the generated skill against its canonical source. No hooks, MCP servers, tool permissions, or credentials are added.

## Reproduce local checks

```sh
python scripts/verify_bundle.py
python -m unittest discover -s tests -v
claude plugin validate . --strict
claude plugin validate plugins/c4-mermaid --strict
```

The repository tests cover offline operation, integrity failures, all eight native user/project installation destinations, marketplace sources, manifest consistency, and packaged-resource identity. They do not certify model reasoning or every renderer in every host. Local profiles used for native installation tests are isolated from the user's normal configuration.

## Primary requirements consulted

- [OpenAI plugin packaging](https://developers.openai.com/plugins/build/plugins): repository marketplaces, plugin structure, and compatibility manifests.
- [Claude plugin manifest reference](https://code.claude.com/docs/en/plugins-reference) and [marketplace reference](https://code.claude.com/docs/en/plugins/marketplace-reference): native file locations, contained component paths, metadata, and local plugin sources.
- [Kimi Agent Skills](https://github.com/MoonshotAI/kimi-cli/blob/main/docs/en/customization/skills.md) and [Kimi Plugins](https://github.com/MoonshotAI/kimi-cli/blob/main/docs/en/customization/plugins.md): skill directory discovery versus executable tools.
- [DeepSeek Harness Skills](https://github.com/deepseek-ai/deepseek-harness/blob/master/docs/subsystems/skills.md): filesystem roots, frontmatter, resource directories, and provider loading.

These source links are bibliography for the repository audit. The installed air-gapped skill uses the local summaries in `references/harnesses.md` and does not fetch these pages.
