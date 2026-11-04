# C4 Mermaid

A portable Agent Skill for **Codex, Claude Code, Kimi Code CLI, and DeepSeek Harness**, analyzing an application repository or description and producing evidence-based C4 architecture diagrams in Mermaid.

- Correct mapping of software systems, containers, components, and code.
- Compact layouts inside boundaries, with readable text, labels, and arrows.
- Consistent shapes and colors based on the official C4 examples.
- Mandatory review against the C4 diagram checklist and additional evidence and visual checks.
- Nine editable Mermaid examples with reviewed SVG previews.
- Thirteen parameterized vector shapes and a local SVG generator.
- An offline viewer with bundled Mermaid 12.3.0, layout checks, and SVG export.

All skill instructions, references, templates, and viewer controls are in English. Project deliverables can use the language requested by the user.

## Install

Clone the repository, then install the same bundle for the chosen harness. Python 3.9 or newer is needed only for this optional installer and the vector generator:

```sh
git clone https://github.com/eccodolf/c4-mermaid.git
cd c4-mermaid
python scripts/install_skill.py --target codex
```

Choose one target, or repeat for the harnesses you use:

| Target | User destination | Invoke |
| --- | --- | --- |
| `codex` | `~/.agents/skills/c4-mermaid` | `$c4-mermaid` |
| `claude` | `~/.claude/skills/c4-mermaid` | `/c4-mermaid` |
| `kimi` | `~/.kimi/skills/c4-mermaid` | `/skill:c4-mermaid` |
| `deepseek` | `~/.dsh/skills/c4-mermaid` | Ask to load `c4-mermaid` |

For example, `python scripts/install_skill.py --target claude` installs for Claude Code. Add `--scope project --project-root /path/to/application` for a project installation, or `--dest /configured/skills/c4-mermaid` for an exact custom destination. The installer refuses to overwrite an existing folder and does not change harness settings. Start a new session if discovery has not refreshed.

Without Python, clone directly into the desired destination from the table. Keep the complete directory together. For updates, run `git pull --ff-only` in a direct installation; for copied installations, copy reviewed changes into the existing skill directory. Do not install duplicate copies into overlapping discovery roots.

See [harness compatibility](references/harnesses.md) for primary documentation links, legacy Codex paths, Kimi discovery options, and DeepSeek Harness profile requirements. DeepSeek support targets the official DSH application, not the standalone model API or chat website.

Example request:

> Load the c4-mermaid skill. Inspect this repository and create System Context and Container diagrams. Include the evidence, assumptions, rendered previews, and checklist verdicts.

The modeling workflow is identical across harnesses. Rendering and visual review depend on available host tools; missing capabilities are reported as `NOT VERIFIED`, and unrendered diagrams remain drafts.

## Resources

- [Skill instructions](SKILL.md)
- [Harness compatibility and invocation](references/harnesses.md)
- [Abstraction mapping](references/c4-model.md)
- [Mandatory review checklist](references/review-checklist.md)
- [Mermaid guidance](references/mermaid.md)
- [Official example analysis](references/official-examples.md)
- [Editable examples and SVG previews](assets/templates/)
- [Vector shape catalog](assets/graphics/catalog-light.svg)

## Offline tools

Open `assets/offline/viewer.html` in a browser. Load an example from `assets/templates/` or paste Mermaid source, render it, review the result, and export SVG with its visible legend. The engine is included locally; no CDN or network fonts are required. Automatic checks supplement mandatory visual review and do not prove every layout correct.

Generate a standalone parameterized shape using Python's standard library:

```sh
python scripts/render_shape.py --help
```

Native Mermaid C4 cannot import the bundled SVG shapes as custom symbols. The skill documents faithful notation where supported and explicit adaptations where needed.

## Validation

Run `python -m unittest discover -s tests` to check isolated installation paths for all four harnesses, copied-resource integrity, and overwrite protection. Packaging checks do not establish runtime/model behavior on every platform. The bundled SVG previews were reviewed with Mermaid 12.3.0; use the mandatory checklist on new diagrams in your actual renderer.

## Attribution

C4 model and visual references: [Simon Brown, c4model.com](https://c4model.com/), licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). The bundle contains independently drawn adaptations and fictional examples. Preserve their attribution when redistributing adapted graphics.

Mermaid is distributed under the MIT license; its [license is included](assets/offline/LICENSE.mermaid). See [sources and provenance](references/sources.md) for details.
