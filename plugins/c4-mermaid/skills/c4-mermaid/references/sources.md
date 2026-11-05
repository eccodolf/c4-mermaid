# Sources, attribution, and provenance

This bundle contains the complete task-specific guidance needed for offline use. All operational references below are local. Original source names identify authorship and research provenance; they are not instructions to retrieve pages.

## C4 material

Original author: Simon Brown. Original publication: C4 model, source identifier `c4model.com`. Consulted 2026-11-05: Abstractions; Software System; Container; Component; Code; Microservices; Queues and topics; Abstraction FAQ; Diagram examples; Notation; Software architecture diagram review checklist; System Context; Container view; Component view; Code view; Landscape; Dynamic; Deployment; and the interactive banking example.

The original site and visual examples are licensed under Creative Commons Attribution 4.0 International. The [complete license text](../assets/offline/LICENSE.CC-BY-4.0) is included locally, including its warranty disclaimer. Preserve attribution and the indication of modifications when redistributing adaptations.

The [mapping guide](c4-model.md) contains the classification rules. The [example analysis](official-examples.md) records observations from ten original diagrams and eight keys. The [review checklist](review-checklist.md) includes all 21 official criteria in condensed wording. Application diagrams are fictional order-system examples. Optional alternate palettes and the user's compact-layout/no-overlap requirements are identified as adaptations. Banking-model SVGs and vendor logos are not included.

## draw.io C4 assets

The bundle includes actual draw.io C4 palette assets from `jgraph/drawio`, tag `v32.6.10`, commit `c72c9a98b7a6ce392556ed04c05e0ff19f43f5c3`. Original source files [mxC4.js](../assets/drawio-c4/mxC4.js), [Sidebar-C4.js](../assets/drawio-c4/Sidebar-C4.js), and [Shapes.js](../assets/drawio-c4/Shapes.js) are retained unchanged. The [palette snapshot](../assets/drawio-c4/library.json) freezes actual C4 style entries and selected paint operations. Python adapters interpret local data; no vendor script is executed at runtime.

Copyright notices remain in the sources. The complete [Apache-2.0 license](../assets/drawio-c4/LICENSE.drawio), [adaptation notice](../assets/drawio-c4/NOTICE.txt), and [pinned provenance/hashes](../assets/drawio-c4/provenance.json) are included. Modifications include parameterized browser geometry, safe text regions, darker text for contrast, and frame-header placement. Person2 retains its original circular-head formulas; data and message-bus containers follow cylinder3; general applications and components use the C4 rounded blocks. Mermaid-native examples use Mermaid's own glyphs. No third-party theme or alternate vendor asset collection is included.

## draw.io verification

Native editable XML uses inline vector stencils rather than remote libraries or image cells. The examples were rendered to SVG/PNG and native XML re-exported through locally provisioned draw.io desktop 32.6.10. The application itself is not redistributed here. [drawio.md](drawio.md) describes the supported model, saving procedure, offline requirements, and verification limits.

## Mermaid engine

Bundled engine: Mermaid 12.3.0, the official npm browser distribution maintained by the Mermaid project (`mermaid-js/mermaid`). Its [MIT license](../assets/offline/LICENSE.mermaid) is included verbatim. The [notation guide](mermaid.md) and nine paired source/SVG examples document the supported use needed by this skill.

The engine is frozen in this bundle. No installation script resolves packages, installs a CLI, downloads a renderer, registers remote icons, or fetches an update. Intentional upgrades require a reviewed replacement bundle, regenerated integrity manifest, and revalidation of examples outside the operational air gap.

## Harness compatibility

The [local harness guide](harnesses.md) summarizes installation and invocation from: OpenAI's Build skills and Package your plugin documentation; Anthropic's Extend Claude with skills, Plugin manifest reference, and Marketplace reference; MoonshotAI Kimi Code CLI Agent Skills and Plugins documentation; and DeepSeek Harness Skills subsystem documentation. Documentation was consulted on 2026-11-05. The installed DSH filesystem provider version used for the loader check was `0.2.1-rc.2`.

These summaries are sufficient to use the bundle in a preconfigured compatible harness. They do not include the agent runtimes or model weights and do not promise that a hosted service runs without a network connection. See the [air-gap runbook](airgap.md).

## Identifiers and integrity

Full third-party license texts and the unchanged vendor engine may contain inert source identifiers. SVG/XML namespace identifiers identify formats; they do not fetch resources. All authored instruction links point within this bundle. The [local verifier](../scripts/verify_bundle.py) checks the transferred files against `bundle-manifest.json`; hashes establish integrity, not publisher authenticity.
