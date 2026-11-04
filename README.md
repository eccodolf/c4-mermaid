# C4 Mermaid

A Codex skill for analyzing an application repository or description and producing evidence-based C4 architecture diagrams in Mermaid.

- Correct mapping of software systems, containers, components, and code.
- Compact layouts inside boundaries, with readable text, labels, and arrows.
- Consistent shapes and colors based on the official C4 examples.
- Mandatory review against the C4 diagram checklist and additional evidence and visual checks.
- Nine editable Mermaid examples with reviewed SVG previews.
- Thirteen parameterized vector shapes and a local SVG generator.
- An offline viewer with bundled Mermaid 12.3.0, layout checks, and SVG export.

All skill instructions, references, templates, and viewer controls are in English. Project deliverables can use the language requested by the user.

## Install

Clone this repository into your Codex skills directory:

```sh
git clone https://github.com/eccodolf/c4-mermaid.git ~/.codex/skills/c4-mermaid
```

If `CODEX_HOME` is configured, use its `skills/c4-mermaid` directory instead. The skill will be available on the next turn.

Example request:

> Use $c4-mermaid to inspect this repository and create System Context and Container diagrams. Include the evidence, assumptions, rendered previews, and checklist verdicts.

## Resources

- [Skill instructions](SKILL.md)
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

## Attribution

C4 model and visual references: [Simon Brown, c4model.com](https://c4model.com/), licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). The bundle contains independently drawn adaptations and fictional examples. Preserve their attribution when redistributing adapted graphics.

Mermaid is distributed under the MIT license; its [license is included](assets/offline/LICENSE.mermaid). See [sources and provenance](references/sources.md) for details.
