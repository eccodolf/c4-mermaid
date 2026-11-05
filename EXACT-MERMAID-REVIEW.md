# Exact Mermaid rendering review

Version **1.3.0**, reviewed 2026-11-05.

The previous Mermaid path could approximate the supplied draw.io glyphs. The bundled `drawioC4` extension now parses editable C4 statements through Mermaid 12.3.0 and renders them with the original draw.io 32.6.10 native engine, original C4 definitions, and the user-supplied canonical styles. It does not replace the architecture with image cells or embedded native XML. Layout metadata contains positions, routing, presentation subtypes, and coverage IDs; architecture facts remain in the C4 statements.

## Evidence

- All **12 supplied element/scope variants** match the actual draw.io desktop export's vector primitive signatures: paths, caps, corners, orientation, fill, stroke, dash pattern, and rotation. The native reference is bound to the reviewed source model by SHA-256.
- Live browser checks repeat those comparisons in light and dark modes. Export freezes canonical light colors and uses standalone SVG primitives and text; no image or foreignObject substitutions remain.
- All **nine example sources** render and export with visible legends. Raster previews were visually reviewed for text fit, readable arrows, containment, and compact placement.
- The native renderer measures actual SVG text glyph bounds, checks shape-safe interiors, and rejects detected overlaps, unrelated blocks crossed by arrows, and relationship labels on scope contours or captions. Manual review remains mandatory.
- Nine invalid input cases are rejected, including semantic metadata overrides, wrong store glyphs, overlapping blocks, text overflow, missing layout, plain stock C4, generic flowcharts, remote directives, and a blank legend. Rendering recovers after rejection.
- Network requests observed during browser testing: **zero**. SVG clip references are fragment-local, with no source-machine paths or external resources.
- **26 Python tests**, the air-gap source guard, bundle integrity checks, skill validation, and both strict Claude packaging validators pass. Generated plugin resources match the standalone bundle.

The live browser harness uses an already-provisioned local Playwright module and Microsoft Edge. Test tools are not downloaded by the skill or required by its local viewer. See [the reproducible runtime checks](references/exact-mermaid.md).

## Compatibility boundary

The complete local viewer includes the extension and native engine; no draw.io desktop application is needed for this Mermaid path. An unmodified GitHub, ChatGPT, editor, or Mermaid CLI preview does not automatically load the extension. Supply the exact exported SVG in those hosts and retain `.mmd` plus its positioned model for editing. Missing native-renderer capability must never trigger a simplified fallback.

The separate native `.drawio` export remains editable and uses the same canonical source templates. The historical [native save review](DRAWIO-REVIEW.md) records the earlier desktop export and round-trip checks. Python-generated parameterized glyph samples are layout aids, not authoritative exact Mermaid deliverables.

## Upstream provenance

Runtime source and licenses are frozen in [the local provenance record](assets/drawio-c4/provenance.json), with the original Apache-2.0 notices. Repository-only source links: [Mermaid external diagrams](https://mermaid.js.org/config/setup/mermaid/interfaces/Mermaid.html#registerexternaldiagrams), [pinned draw.io core](https://github.com/jgraph/drawio/blob/c72c9a98b7a6ce392556ed04c05e0ff19f43f5c3/src/main/webapp/mxgraph/mxClient.js). The installed air-gapped skill does not fetch these pages.
