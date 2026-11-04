# Sources and provenance

Researched 2026-11-05. This is a task-specific application guide, not a copied manual. The visual review covered ten original diagrams and eight separate keys; see [official-examples.md](official-examples.md).

- [C4 model, Simon Brown](https://c4model.com/).
- [Abstractions](https://c4model.com/abstractions): the hierarchy used for classification.
- [Software System](https://c4model.com/abstractions/software-system), [Container](https://c4model.com/abstractions/container), [Component](https://c4model.com/abstractions/component), [Code](https://c4model.com/abstractions/code).
- [Microservices](https://c4model.com/abstractions/microservices), [Queues and topics](https://c4model.com/abstractions/queues-and-topics), [Abstraction FAQ](https://c4model.com/abstractions/faq).
- [Diagram examples](https://c4model.com/diagrams), [Notation](https://c4model.com/diagrams/notation), and the [mandatory review checklist](https://c4model.com/diagrams/checklist).
- [System Context](https://c4model.com/diagrams/system-context), [Container view](https://c4model.com/diagrams/container), [Component view](https://c4model.com/diagrams/component), [Code view](https://c4model.com/diagrams/code).
- [Landscape](https://c4model.com/diagrams/system-landscape), [Dynamic](https://c4model.com/diagrams/dynamic), [Deployment](https://c4model.com/diagrams/deployment).
- [Interactive example](https://c4model.com/example/#SystemContext), including Containers and Components, inspected in the browser.
- [Mermaid C4](https://mermaid.js.org/syntax/c4.html) and [Flowchart](https://mermaid.js.org/syntax/flowchart.html): supported syntax. Installed Mermaid configuration types were also checked for C4 spacing options.

The C4 site and example diagrams are by Simon Brown and licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Adaptations include independently constructed SVG primitives, optional alternate profiles, and fictional order-system examples. Preserve attribution when redistributing the adapted graphics. Structurizr viewer code, its original SVGs, the banking model, and vendor icons were not copied into this bundle.

`assets/offline/mermaid.min.js` is the official Mermaid 12.3.0 npm distribution from [mermaid-js/mermaid](https://github.com/mermaid-js/mermaid). Its MIT license is included as `LICENSE.mermaid`. The local viewer and vector generator have no network dependency. Engine upgrades are deliberate maintenance followed by template validation, not automatic downloads during skill execution.

The required compact block layout and no-overlap acceptance gates are user requirements. They supplement the official C4 checklist and do not claim that C4 prescribes a unique layout algorithm or universal color palette.

Harness discovery and invocation references for Codex, Claude Code, Kimi Code CLI, and DeepSeek Harness are linked in [harnesses.md](harnesses.md). The portable bundle keeps the common Agent Skills frontmatter and resolves resources relative to its own directory.
