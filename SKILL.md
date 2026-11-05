---
name: c4-mermaid
description: "Create evidence-based C4 diagrams in Mermaid from a local repository or description, with mandatory canonical draw.io C4 assets, editable native delivery, compact readable layouts, and air-gapped review."
---

# C4 Mermaid

Build an evidence-based architecture model first, then render it in Mermaid. Follow the bundled [C4 abstractions](references/c4-model.md) and [example analysis](references/official-examples.md), rather than treating a repository tree as an architecture. This skill and its bundled instructions, templates, graphics, and viewer are in English. Use the user's requested language for project deliverables when specified.

## Air-gapped operation

Use only transferred local repositories, supplied descriptions, and bundled resources. Read [airgap.md](references/airgap.md) for offline installation, verification, rendering, and host requirements. Do not browse, resolve citations, fetch Git remotes, use online editors, install packages, download models/fonts/icons, or call external services while using this skill. Missing local facts remain unknown. The complete method, checklist, notation guide, examples, engine, vector generator, and license texts are included; no external page is required.

The agent harness and inference backend must already run inside the isolated environment. This bundle does not turn a hosted assistant or cloud model into a local runtime. Use available local tools; if a required capability is absent, report the corresponding verification limit instead of reaching outside the air gap.

## Run in your harness

Use this same skill in Codex, Claude Code, Kimi Code CLI, or DeepSeek Harness. Read the relevant entry in [harnesses.md](references/harnesses.md) for installation, invocation, and capability limits. Resolve supporting paths relative to the directory containing this `SKILL.md`, not the application's working directory. Keep repository input, skill resources, and generated output paths distinct.

Use the host's available file search, file reading, shell, browser, and image inspection tools; no particular tool name, MCP server, model provider, or desktop app is required. The Python shape generator is optional and uses the standard library. Read references selectively; do not load the bundled JavaScript engine or all SVG examples into model context. If shell or visual inspection is unavailable, continue the supported modeling work and report the corresponding checklist items as `NOT VERIFIED`. A rendered SVG without visual inspection is not a visually reviewed diagram.

## Establish the model

1. Identify the system, audience, question, and available evidence. Normally start with L1 System Context and L2 Container. Add L3 for a selected container only when useful and supported. Do not automatically generate every view.
2. **Repository input:** read applicable instructions, project overview, manifests, entry points, runtime configuration, API/data clients, message producers and consumers. Prefer `rg --files` and targeted searches. Reconcile documentation with implementation and distinguish development, test, and production. Running the application is not normally necessary.
3. **Description input:** work from supplied facts without requiring a repository. Mark unspecified technology, ownership, or protocols as unknown. State boundary assumptions. Distinguish an existing architecture from a proposed design.
4. Before drawing, apply the mandatory mapping rules in [c4-model.md](references/c4-model.md). Build an element register: `id | name | abstraction | parent | responsibility | technology | classification rationale | evidence/status`. Build a relationship register: `source | target | action | protocol | evidence/status`. Evidence is a file and line, or a specific supplied statement. A package import or installed SDK alone does not prove an integration.
5. Keep identities and names consistent across views. A child view expands a named parent. An organizational grouping, code folder, Docker image, or deployment node is not automatically a C4 system, container, or component. Do not invent users, runtimes, workers, protocols, or callbacks to complete a familiar pattern.
6. For every delivered Landscape, System Context, and Container view, apply [external-systems.md](references/external-systems.md). Derive the complete in-scope external-system set from evidence and cross-boundary relationships, then reconcile it with actual nodes in each Mermaid source and rendered diagram. Keep a coverage matrix; a known relevant system missing from a view is a failure, even if another view shows it. Preserve a system with an unknown calling container and state that uncertainty instead of omitting it or inventing a caller.

## Select notation and layout

Read [mermaid.md](references/mermaid.md) before rendering. Consult the relevant view and shape entries in [official-examples.md](references/official-examples.md).

Apply [shape-rules.md](references/shape-rules.md) to every glyph: explicit C4 type and container subtype determine geometry. Visible type, metadata, and shape must agree. Always read [canonical-assets.md](references/canonical-assets.md) and use the supplied C4 assets. Deliver a native `.drawio` companion for each C4 architecture view; read [drawio.md](references/drawio.md), preserve actual native shapes, and render/round-trip the saved file. Mermaid remains the editable companion when requested; do not pretend that its approximations use native draw.io assets.

Use native `C4Context`, `C4Container`, `C4Component`, `C4Dynamic`, or `C4Deployment` when the target supports them. A landscape can use `C4Context` with the correct scope and title. Use `classDiagram` or `erDiagram` for Code; there is no `C4Code` syntax. A sequence representation is suitable for a runtime scenario.

When native C4 is unavailable or cannot satisfy the required readable, compact layout, use a styled `flowchart` preserving C4 semantics. Identify adapted shapes. Do not declare native C4 unsupported merely because the target renderer is unknown.

The supplied draw.io C4 palette is mandatory for this skill. Use native person2, rounded System/Container/Component blocks, cylinder3 stores/message buses, hexagonal microservices, WebBrowserContainer2, and gray dashed rounded logical scopes with bottom labels. External Person and external System have distinct colors. Use the bundled native color-key legend. Preserve readable font contrast and fit; C4 does not itself mandate this palette, but the user selected it. Distinguish logical, organizational, and deployment containment.

**Every diagram must include its own visible legend.** Explain its actual shapes, colors, border styles, arrows, and notation adaptations inside the exported artifact. Prose elsewhere or source comments alone do not satisfy this requirement.

**Compact block layout is mandatory.** Pack sibling blocks into a balanced grid or short dependency-oriented rows inside their boundary. Size the boundary around its contents and routing corridors. Remove avoidable empty rows, oversized gaps, stretched frames, and long disconnected legend strips. Preserve sufficient padding for all labels, arrowheads, and relationship routes. Compactness never permits overlapping text, an edge through an unrelated block, hidden labels, unreadably small fonts, or a label detached from its arrow. Render, inspect, and adjust; do not confuse smaller file dimensions with a better layout.

## Offline bundle

- `assets/templates/*.mmd`: editable, fictional examples, paired with reviewed `.svg` previews containing their visible keys. Load only the required example and replace its facts with project evidence.
- `assets/offline/viewer.html`: the included Mermaid engine, local file loading, layout checks, and SVG export without CDN or network fonts. File loading reads `%% legend:` comments into the visible export legend.
- `assets/c4-theme.json` and `assets/graphics/*.svg`: palette parameters and fourteen parameterized vector variants.
- `python scripts/render_shape.py --help`: generate a parameterized shape or catalog using the standard library. Geometry is recalculated for size and labels; it is not a stretched bitmap or a substitute for a Mermaid diagram.
- `assets/drawio-c4/`: the mandatory supplied XML, extracted native templates, importable `native-c4.mxlibrary`, pinned upstream source, and complete notices. Runtime styles come from the supplied templates. The `drawio-c4` profile is required.
- `assets/drawio/`: positioned JSON examples, native editable `.drawio` files, and previews. `scripts/export_drawio.py` exports and checks them using only Python's standard library. A local draw.io application is a separately provisioned rendering capability.

Native Mermaid cannot import these SVG symbols as custom C4 shapes. Preserve that distinction when offering a precise vector composition alongside editable Mermaid.

## Mandatory acceptance and delivery

Complete **every item** in [review-checklist.md](references/review-checklist.md) for **every delivered diagram**. It includes the official C4 review criteria plus evidence, abstraction, compactness, and rendering gates. An unchecked item is not a pass. Fix failures and repeat affected checks; state genuine verification limits.

Render every source with the target version when available, otherwise the bundled version, and inspect the actual result. Parsing alone is insufficient. Text must fit its own block, must not overlap other text or foreign blocks, and must remain visibly associated with its arrow. Check titles, boundaries, legends, arrowheads, crossings, and compact use of interior space. The viewer's external-label detector supplements manual inspection; it does not prove the whole layout correct. Do not send private repository contents to an online editor for validation.

Deliver editable Mermaid, previews/exports when available, a visible legend, significant assumptions, evidence, and a short checklist verdict for each view. Keep `.mmd` alongside saved SVG. If rendering was unavailable, explicitly report that the result is an unrendered draft. Do not claim exhaustive repository coverage after a partial inspection.

Always deliver the native `.drawio` and positioned source model for C4 architecture views. Verify all pages after native save/re-export: counts, stable IDs, parents, text, geometry, arrow endpoints, and external-system coverage. Report actual renderer/version and any unperformed visual or round-trip checks. Do not describe embedded pictures as editable architecture.

For Landscape, System Context, and Container diagrams, include or reference the external-system coverage matrix and report missing systems and evidence limits explicitly. A system mentioned only in prose, a legend, an arrow label, or another diagram is not a represented system node.

Sources, attribution, and offline dependency provenance: [sources.md](references/sources.md).
