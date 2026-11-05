# C4 Mermaid

Version: **1.2.0**.

A self-contained, air-gap-ready Agent Skill for **Codex, Claude Code, Kimi Code CLI, and DeepSeek Harness**. Analyze a local application repository or supplied description and produce evidence-based C4 architecture diagrams in Mermaid.

- Correct mapping of systems, containers, components, and code.
- Mandatory external-system coverage across Landscape, System Context, and Container views.
- Compact layouts inside boundaries, with readable text, labels, and arrows.
- Consistent shapes and colors based on the C4 examples.
- All 21 C4 review criteria plus evidence, layout, export, and air-gap gates.
- Nine editable Mermaid examples with reviewed SVG previews.
- Fourteen parametric vector variants and a local SVG generator.
- Mandatory user-supplied draw.io C4 assets, native XML templates, an importable shape library, and complete Apache-2.0 notices.
- Native editable draw.io export, typed shape checks, layout preflight, and round-trip examples.
- Mermaid 12.3.0 browser engine, local viewer, and complete license texts.
- Offline installation, tests, and SHA-256 integrity verification.

All authored material is in English. Project deliverables can use the user's requested language. No external page, package registry, CDN, icon service, or remote renderer is required. The agent application and inference backend must already be available inside the isolated environment; model weights and host runtimes are not included.

For connected installation through ChatGPT Desktop / Codex or Claude Code, the repository includes native marketplaces and a ready-to-install plugin. Repository-only setup instructions are in `DESKTOP-INSTALL.md`; the packaging audit is in `HARNESS-PACKAGING.md`. Both are separate from this offline skill bundle. The plugin contains the same complete skill and uses a local source within its checkout. Kimi and DSH use the standalone skill directory.

## Install from a transferred bundle

Extract the complete `c4-mermaid` directory from approved local media. From that directory, optionally verify and install using an already-installed Python 3.9 or newer:

```sh
python scripts/verify_bundle.py
python scripts/install_skill.py --target codex
```

| Target | User destination | Invoke |
| --- | --- | --- |
| `codex` | `~/.agents/skills/c4-mermaid` | `$c4-mermaid` |
| `claude` | `~/.claude/skills/c4-mermaid` | `/c4-mermaid` |
| `kimi` | `~/.kimi/skills/c4-mermaid` | `/skill:c4-mermaid` |
| `deepseek` | `~/.dsh/skills/c4-mermaid` | Ask to load `c4-mermaid` |

Choose the corresponding `--target`. Add `--scope project --project-root /path/to/application` for a project installation, or `--dest /configured/skills/c4-mermaid` for an exact custom directory. Installation verifies the bundle, makes no network calls, refuses an existing destination, and does not configure the harness. Start a new session if discovery is stale.

Without Python, copy the complete directory manually to the appropriate location and disclose that automated integrity verification was not performed. Updating also uses a transferred, verified bundle; no online updater is part of the workflow. See the [air-gap runbook](references/airgap.md) and [harness guide](references/harnesses.md).

Example request:

> Load the c4-mermaid skill. Using only this local repository and bundled references, create System Context and Container diagrams. Include evidence, assumptions, rendered previews, and checklist verdicts. Keep all processing inside the air gap.

## Local resources

- [Skill instructions](SKILL.md)
- [Air-gap operation and prerequisites](references/airgap.md)
- [Harness installation and invocation](references/harnesses.md)
- [Abstraction mapping](references/c4-model.md)
- [External-system coverage](references/external-systems.md)
- [Mandatory checklist](references/review-checklist.md)
- [Mermaid syntax and layout](references/mermaid.md)
- [C4 example analysis](references/official-examples.md)
- [Mandatory supplied C4 assets](references/canonical-assets.md)
- [Importable native shape library](assets/drawio-c4/native-c4.mxlibrary)
- [Semantic shape rules](references/shape-rules.md)
- [Editable draw.io delivery and verification](references/drawio.md)
- [Native shape catalog](assets/drawio/shapes.drawio) and [Container example](assets/drawio/container.drawio)
- [Mermaid sources and SVG previews](assets/templates/)
- [Vector catalog](assets/graphics/catalog-light.svg)
- [Offline viewer](assets/offline/viewer.html)
- [Sources, adaptations, and local licenses](references/sources.md)

## Render and verify offline

Open `assets/offline/viewer.html` in a permitted local browser. Load a `.mmd`, render, inspect it, and export SVG with its legend. The engine is included and uses installed font fallbacks. The viewer blocks network connections and rejects external-resource directives. Normal use requires no server, Python, Node, npm, or additional fonts. A permitted loopback-only fallback is described in the runbook.

```sh
python scripts/render_shape.py --help
python scripts/export_drawio.py --input assets/drawio/container.json --output orders.drawio
python scripts/export_drawio.py --check orders.drawio
python scripts/verify_bundle.py
python -m unittest discover -s tests
```

Automatic checks supplement visual review. An unrendered source remains a draft, and missing visual inspection is reported as `NOT VERIFIED`. Native Mermaid C4 cannot import the bundled SVG primitives as custom symbols; the notation guide identifies adaptations.

The integrity manifest detects changed/missing files; it is not a cryptographic signature. Runtime applications and model behavior are separate from package verification. Preserve the bundled legal notices when redistributing adaptations.
