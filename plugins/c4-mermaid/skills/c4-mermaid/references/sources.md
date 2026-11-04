# Sources, attribution, and provenance

This bundle contains the complete task-specific guidance needed for offline use. All operational references below are local. Original source names identify authorship and research provenance; they are not instructions to retrieve pages.

## C4 material

Original author: Simon Brown. Original publication: C4 model, source identifier `c4model.com`. Consulted 2026-11-05: Abstractions; Software System; Container; Component; Code; Microservices; Queues and topics; Abstraction FAQ; Diagram examples; Notation; Software architecture diagram review checklist; System Context; Container view; Component view; Code view; Landscape; Dynamic; Deployment; and the interactive banking example.

The original site and visual examples are licensed under Creative Commons Attribution 4.0 International. The [complete license text](../assets/offline/LICENSE.CC-BY-4.0) is included locally, including its warranty disclaimer. Preserve attribution and the indication of modifications when redistributing adaptations.

The [mapping guide](c4-model.md) contains the classification rules. The [example analysis](official-examples.md) records observations from ten original diagrams and eight keys. The [review checklist](review-checklist.md) includes all 21 official criteria in condensed wording. Included graphics are independently drawn adaptations; application diagrams are fictional order-system examples. Optional alternate palettes and the user's compact-layout/no-overlap requirements are identified as adaptations. Original Structurizr viewer code, banking-model SVGs, and vendor icons are not included.

## Mermaid engine

Bundled engine: Mermaid 12.3.0, the official npm browser distribution maintained by the Mermaid project (`mermaid-js/mermaid`). Its [MIT license](../assets/offline/LICENSE.mermaid) is included verbatim. The [notation guide](mermaid.md) and nine paired source/SVG examples document the supported use needed by this skill.

The engine is frozen in this bundle. No installation script resolves packages, installs a CLI, downloads a renderer, registers remote icons, or fetches an update. Intentional upgrades require a reviewed replacement bundle, regenerated integrity manifest, and revalidation of examples outside the operational air gap.

## Harness compatibility

The [local harness guide](harnesses.md) summarizes installation and invocation from: OpenAI's Build skills documentation; Anthropic's Extend Claude with skills documentation; MoonshotAI Kimi Code CLI Agent Skills documentation; and DeepSeek Harness Skills subsystem documentation. Documentation was consulted on 2026-11-05. The installed DSH filesystem provider version used for the loader check was `0.2.1-rc.2`.

These summaries are sufficient to use the bundle in a preconfigured compatible harness. They do not include the agent runtimes or model weights and do not promise that a hosted service runs without a network connection. See the [air-gap runbook](airgap.md).

## Identifiers and integrity

Full third-party license texts and the unchanged vendor engine may contain inert source identifiers. SVG/XML namespace identifiers identify formats; they do not fetch resources. All authored instruction links point within this bundle. The [local verifier](../scripts/verify_bundle.py) checks the transferred files against `bundle-manifest.json`; hashes establish integrity, not publisher authenticity.
