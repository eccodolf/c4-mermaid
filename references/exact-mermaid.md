# Exact draw.io shapes in Mermaid

Use the bundled **drawioC4** Mermaid extension for C4 architecture. It registers through Mermaid's external-diagram API, parses the C4 statements with Mermaid 12.3.0, and paints their SVG with the unchanged draw.io 32.6.10 engine and supplied C4 definitions. No image cells, stretched icons, generic replacement glyphs, or approximate custom stencils are used. All twelve supplied element/scope variants are checked against an actual draw.io vector export.

## Generate and render

Build the same evidence-based positioned JSON model used by [drawio.md](drawio.md), including explicit types/subtypes, real containment, routes, external-system coverage, and a nonempty legend:

```sh
python scripts/model_to_mermaid.py --input model.json --output architecture.mmd
```

Open the bundled `assets/offline/viewer.html` in a permitted local browser, load the `.mmd`, render, inspect, and save SVG and PNG. The diagram itself contains its color-key legend and notation notes. No draw.io desktop installation, Node, npm, remote library, font download, or server is needed for this Mermaid rendering path. A local browser and the complete transferred bundle are required.

Sources begin with `drawioC4 context`, `drawioC4 container`, `drawioC4 component`, `drawioC4 dynamic`, or `drawioC4 deployment`. Landscape uses the context grammar and an explicit landscape view. Statements retain familiar `Person`, `System`, `Container`, `ContainerDb`, `ContainerQueue`, `Component`, scope, deployment, and `Rel` syntax. The generator adds one `%% drawio-layout:` JSON comment containing only geometry, routing, presentation subtypes, and the required external-system IDs. Names, technology, responsibilities, and relationship actions remain editable in the Mermaid statements rather than duplicated in an embedded image or native XML payload.

The positioned JSON is the layout/evidence source. Regenerate Mermaid and the mandatory native `.drawio` together after changing that model. Direct source edits are supported when they preserve the declared IDs, containment, and routing; increase bounds when longer text no longer fits. Encode quotation marks inside a C4 argument as `&quot;` and backslashes as `&bsol;`; the generator handles these escapes. Parser ambiguity must cause a correction, not silently lost label text.

Example resources: [exact Container Mermaid](../assets/drawio/container.mmd), [its SVG](../assets/drawio/container-mermaid.svg), [all supplied shapes](../assets/drawio/shapes.mmd), and [their exact Mermaid SVG](../assets/drawio/shapes-mermaid.svg). The historical filename `container-flowchart.mmd` is retained for compatibility; it now contains exact drawioC4 syntax, not a flowchart approximation.

## Runtime and host compatibility

The viewer includes Mermaid, `drawio-data.js`, `c4-drawio.js`, the original `mxClient.js` core, unchanged `mxC4.js`, and the selected original cylinder/hexagon definitions in `native-builtins.js`. The latter are extracted without rewriting their paint methods from the bundled upstream `Shapes.js`. Full notices and pinned hashes are [local](sources.md). Assets and engine files are loaded from the bundle only. Resource/style loading and graph editor controls are disabled. Export freezes the canonical light colors, removes invisible interaction targets, and contains ordinary SVG vector primitives and text.

For another local HTML host, load the same scripts in the viewer's order, set `mxLoadResources=false` and `mxLoadStylesheets=false` before the native core, and call `await C4Drawio.install(mermaid)` before `mermaid.render`. Use the complete bundle and an equivalent policy preventing external connections. Do not copy only one script or fetch missing dependencies at runtime.

An unmodified GitHub/ChatGPT/editor Mermaid preview does not install this extension. Use the exported SVG in that host and keep the `.mmd` as editable source. Do not promise that stock third-party previews can display these native shapes. An unavailable extension, missing layout, invalid subtype, or failed validation must stop exact rendering; no simplified C4/flowchart fallback is permitted.

Code diagrams and sequence lifelines retain their appropriate UML/sequence notation; they are not substitutes for C4 runtime elements. Use drawioC4 dynamic views when exact C4 participants are required. Parameterized Python glyph samples are layout aids, not the authoritative exact Mermaid output; deliver the native-engine SVG for fidelity-sensitive work.

## Required verification

Complete the [mandatory checklist](review-checklist.md). Verify the renderer stamp `data-c4-native-renderer="drawio-32.6.10"`, the canonical asset-source digest, correct type/subtype mapping, unchanged native paths/caps/corners, readable text, real arrow endpoints, compact containment, and a visible legend. Parsing alone does not pass. The viewer checks real native label bounds and routes and blocks detected overlaps.

`tests/test_exact_mermaid.py` verifies the shipped vector output against `assets/drawio-c4/native-fidelity.json`, captured from the actual draw.io exporter. The optional live `node tests/test_exact_mermaid.cjs` needs a pre-provisioned Playwright module and Chromium. Set `C4_PLAYWRIGHT_MODULE` and `C4_BROWSER_EXECUTABLE` to their local paths if necessary; `C4_TEST_OUTPUT` selects a local review directory. It renders all examples, compares all twelve native geometries in light/dark modes, checks escaped labels, rejects invalid/simplified inputs, and records external requests. It never installs or downloads a browser. Without those test tools, use the local viewer and report any unperformed automated check honestly.

Deliver all [four required formats](delivery-formats.md). SVG and PNG use the same reviewed export with its legend; native draw.io remains a separate editable graph. Verify every relationship arrowhead and its evidenced direction in each format.

The exact Mermaid grammar currently covers the C4 person/system/container/component primitives, boundaries, groups, and deployment nodes used by the templates. An `infrastructure-node` can be exported by the native JSON helper but has no implemented drawioC4 source macro; mobile-container presentation is also unsupported. Do not promise these unsupported exact-Mermaid variants or substitute another abstraction. Author a faithful supported representation when semantically valid, otherwise report the view as an incomplete draft.
