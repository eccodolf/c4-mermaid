# Mermaid notation and exact geometry

Use the [exact drawioC4 renderer](exact-mermaid.md) for C4 diagrams. It is a Mermaid extension backed by the original native draw.io engine and supplied C4 styles. No simplified flowchart/native-C4 fallback is permitted.

## Authoring interface

Create the evidence-based positioned model described in [drawio.md](drawio.md), then run:

```sh
python scripts/model_to_mermaid.py --input model.json --output architecture.mmd
```

Source starts with `drawioC4 context`, `container`, `component`, `dynamic`, or `deployment`. Familiar C4 `Person`, `Person_Ext`, `System`, `System_Ext`, `Container`, `ContainerDb`, `ContainerQueue`, `Component`, boundary, placement, and `Rel` statements hold the editable architecture facts. One `%% drawio-layout:` comment supplies node bounds, parent IDs, supported container subtypes, relationship routing/ports/offsets, view, and external-system IDs. `%% legend:` comments become a visible color key and notation notes in the SVG.

Use stable ASCII IDs and preserve identities across views. Names, technology, responsibilities, and actions stay in the statements; layout metadata must not override them or change their abstractions. A generic Container may explicitly use the application, browser, or microservice presentation subtype. ContainerDb retains the data-store geometry; ContainerQueue retains the native message-bus geometry. Justify presentation subtypes with evidence, never solely with installed technology.

The supplied palette controls full shapes and colors: Person2; rounded System/Container/Component blocks; cylinder3 stores/message buses; the rounded microservice hexagon; WebBrowserContainer2; and gray dashed rounded logical scopes with bottom captions. Organizational and deployment notation remains distinct. Apply [shape-rules.md](shape-rules.md) and the mandatory [canonical asset policy](canonical-assets.md).

## Render and inspect offline

Open `assets/offline/viewer.html` in a permitted local browser, load source, render, inspect, and save SVG. The renderer includes actual native geometry and text, its legend, and fixed light colors. Missing native runtime/layout or detected overflow/overlap blocks export. Complete the [mandatory checklist](review-checklist.md); browser checks do not prove architecture discovery or every possible route correct.

A stock Mermaid CLI or third-party preview without the extension is not a compatible exact renderer. Use the exported SVG there, preserving the editable `.mmd`. Do not substitute capsules, generic rectangles, approximate icons, images, or stretched snapshots. The legacy filename `container-flowchart.mmd` now contains exact drawioC4 syntax and is not a generic flowchart alternative.

Code views use appropriate `classDiagram` or `erDiagram` notation; there is no C4Code keyword. Supporting sequence views use native sequence lifelines. These express UML/code/message semantics rather than replacing C4 runtime elements. Use drawioC4 dynamic when native C4 participant shapes are required. Nine fictional examples are included; their names and integrations are not evidence about a user's application.

The model converter escapes quotation marks and backslashes for the C4 parser. For direct edits use `&quot;` and `&bsol;` inside arguments; use explicit supported line breaks. Rendered text must agree with the source. Increase bounds or revise wording when text does not fit; do not hide, shrink, or truncate it to pass validation.
