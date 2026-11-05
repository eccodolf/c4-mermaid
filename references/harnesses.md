# Harness compatibility

This is one portable Agent Skills directory, not four diverging prompts. Keep `SKILL.md`, `references/`, `assets/`, and `scripts/` together. `agents/openai.yaml` is optional Codex presentation metadata; the workflow does not depend on it. The shared frontmatter uses only `name` and `description`, with no vendor-specific substitution, forced model, tool allowlist, hooks, or flow execution.

## Install and invoke

### Packaging contracts

| Host | Native instruction package | Optional repository distribution | What not to substitute |
| --- | --- | --- | --- |
| Codex / ChatGPT Desktop | A complete skill directory | A marketplace at `.agents/plugins/marketplace.json` and a plugin with `skills/c4-mermaid/` | A bare repository URL without a marketplace is not a desktop plugin catalog |
| Claude Code | A complete skill directory | A marketplace at `.claude-plugin/marketplace.json`, plugin metadata at `.claude-plugin/plugin.json`, and `skills/c4-mermaid/` under the plugin root | The Codex marketplace JSON shape is not the Claude marketplace format |
| Kimi Code CLI | A complete `<name>/SKILL.md` directory in a skill root | A custom parent directory passed with `--skills-dir` | Kimi `plugin.json` declares executable tools; the OpenAI plugin manifest is not a Kimi skill loader |
| DeepSeek Harness | A skill directory read by the filesystem skill provider | Project/user skill roots or configured `customSkillDirs` | A Codex or Claude marketplace is not a DSH filesystem discovery configuration |

The repository's generated plugin contains the same portable skill directory and native manifests for Codex and Claude. Kimi and DSH consume the standalone skill; neither needs the repository marketplace. The generated `plugins/c4-mermaid/skills` directory is also a valid parent skill root where a host accepts an explicit directory. Do not point a host at the repository root when it expects a parent containing named skill folders.

Paths below are default local directories. `~` means the user's home directory; project paths are relative to the intended application repository. Installation does not configure credentials, models, plugins, or permissions.

| Harness | User installation | Project installation | Explicit invocation |
| --- | --- | --- | --- |
| Codex | `~/.agents/skills/c4-mermaid/` | `.agents/skills/c4-mermaid/` | `$c4-mermaid` followed by the task |
| Claude Code | `~/.claude/skills/c4-mermaid/` | `.claude/skills/c4-mermaid/` | `/c4-mermaid` followed by the task |
| Kimi Code CLI | `~/.kimi/skills/c4-mermaid/` | `.kimi/skills/c4-mermaid/` | `/skill:c4-mermaid` followed by the task |
| DeepSeek Harness (DSH) | `~/.dsh/skills/c4-mermaid/` | `.dsh/skills/c4-mermaid/` | Ask: `Load the c4-mermaid skill and analyze this application.` |

The optional `scripts/install_skill.py` copies the complete portable bundle to one chosen location. It requires Python 3.9 or newer, performs no downloads, and refuses to overwrite an existing installation. `--dest` selects an exact skill directory for a configured or legacy discovery root. It does not infer platform settings. To update an existing installation, transfer another reviewed bundle and copy changes deliberately.

### Codex

Use the discovered skill or explicitly invoke `$c4-mermaid`. Existing Codex setups may still expose skills from `~/.codex/skills` or a configured Codex home; use that already-discovered location rather than creating a duplicate. The table follows current documented `.agents/skills` discovery. Preserve `agents/openai.yaml` for the skill selector. If the update is not visible, restart the session.

### Claude Code

Use `/c4-mermaid` for a standalone installation, or `/c4-mermaid:c4-mermaid` for the repository plugin. The standalone directory needs no plugin manifest, `CLAUDE.md`, dynamic shell injection, or `${CLAUDE_SKILL_DIR}` substitution. The repository additionally ships native Claude marketplace/plugin manifests for plugin-based installation. Resolve resource paths from the loaded skill's location. The local paths in the table apply to Claude Code; Claude account and cloud skill deployment is a separate installation surface.

### Kimi Code CLI

Install the directory form, not a flattened Markdown file: references and offline assets are required. `/skill:c4-mermaid` loads it as a standard skill. It is not a Kimi flow skill; Mermaid examples are architecture output, not executable agent control flow. `kimi --skills-dir /path/to/skills` can select a custom parent skills directory and replaces automatic discovery. Restart after installation if necessary.

For example, `kimi --skills-dir /path/to/repository/plugins/c4-mermaid/skills` selects the packaged parent directory. Do not register `plugins/c4-mermaid/plugin.json` as a Kimi executable-tool plugin. Additional Kimi plugin tooling is unnecessary for this instruction-and-assets package.

### DeepSeek Harness

This target means the official `deepseek-ai/deepseek-harness` application, not the DeepSeek chat website or a bare model API. Its skill subsystem provides discovery; its model-facing `skill` tool loads a named skill. Use that mechanism when exposed, or read the installed `SKILL.md` and its referenced files directly. The host profile must provide file tools and any desired shell/browser tools. The package does not install a DSH plugin or reconfigure a profile. Custom DSH homes require an explicit destination. Start a new session if a skill catalog is stale.

## Capability-based execution

| Available capability | Action | Required disclosure |
| --- | --- | --- |
| File reading/search | Inspect repository evidence and selected references | State inspection scope and unsupported assumptions |
| Description only | Build the model from supplied facts | Mark unknown technologies, protocols, ownership, and relationships |
| Python | Run the optional vector generator using absolute resource/output paths | Do not require Python for Mermaid authoring |
| Browser or local renderer | Render using the target or bundled Mermaid version | Name the actual renderer/version; parsing is not visual review |
| Image/SVG inspection | Inspect the rendered diagram and its final export | Complete compactness, overlap, routing, and clipping checks |
| No renderer or no image inspection | Deliver supported source/model work with explicit limits | Mark affected gates `NOT VERIFIED`; an unrendered result is a draft |

A tool's presence does not imply it can open local HTML, inspect SVG, or export files. Use the offline viewer when the host permits it. If local file URLs are unavailable, an authorized loopback server can serve the bundle; do not bypass a security warning or publish a private application to obtain a preview. A host's optional Mermaid preview may omit legends or support a different syntax version; check its actual output. Preserve all evidence, C4 abstraction, compact layout, and mandatory checklist rules in every harness.

## Portability checks

Run `python -m unittest discover -s tests` from the repository to check installation into isolated user/project directories for all four targets, bundled resources, and refusal to overwrite existing files. These are packaging checks, not evidence of model behavior in every runtime. Apply the operating boundary and transfer procedure in [airgap.md](airgap.md). Validate a real diagram through the intended harness and renderer before reporting runtime-specific success.

Compatibility documentation checked against the locally summarized source documentation on 2026-11-05. Runtime versions and configured discovery roots may differ.

This revision passed the Codex skill validator and all eight isolated user/project installation cases. The installed DSH filesystem provider (`0.2.1-rc.2`) discovered and loaded the bundle with its resource directory intact. Full model-driven sessions in Claude Code, Kimi Code CLI, and DSH were not run; documentation compatibility and loader checks are not end-to-end behavioral certification.

## Exact Mermaid and native draw.io capabilities

All four harnesses use the [same exact Mermaid renderer](exact-mermaid.md). Host Mermaid previews must not substitute generic glyphs; open the bundled local viewer and deliver its SVG. The [native exporter and saving procedure](drawio.md) applies when native files are requested. Python provides model export and structural checks; a separately provisioned local draw.io editor provides native rendering and save/re-export verification. The exporter has no harness-specific API or network dependency. Without the editor or image inspection, report the corresponding D3/D4 gates as `NOT VERIFIED`.
