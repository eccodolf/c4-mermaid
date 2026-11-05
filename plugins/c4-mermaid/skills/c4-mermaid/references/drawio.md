# Editable draw.io delivery

Read this reference when native draw.io is requested or when preparing the shared positioned model. The [canonical supplied assets](canonical-assets.md) are mandatory. Keep Mermaid as an editable companion when Mermaid is part of the request. Build both from the same evidence and identity registers. A picture pasted into a draw.io page, a renamed SVG, or one flattened image cell does not satisfy editable delivery.

## Native model and saving

Use uncompressed `mxfile` XML with one `diagram`/`mxGraphModel` per view. Each element is a separate native vertex with a stable ID, label, type metadata, explicit geometry, and its actual native draw.io C4 shape/style. Relationships are separate native edges attached to element IDs. Keep logical children under their real boundary parent, with coordinates relative to that parent. Place internal edges under their nearest common ancestor. Keep title, scope, visible legend, and attribution as editable annotations. Save `.drawio`, source model, `.mmd` when applicable, preview, evidence/assumptions, coverage matrix, and review verdict together.

The bundled standard-library helper exports a **positioned JSON model**, not arbitrary Mermaid text. Derive that model from the shared registers; never claim an automatic lossless Mermaid conversion. Start from [container.json](../assets/drawio/container.json) or [the shape catalog](../assets/drawio/shapes.json):

```sh
python scripts/export_drawio.py --input model.json --output architecture.drawio
python scripts/export_drawio.py --check architecture.drawio
```

The top level contains `profile` and `pages`. Each page needs `id`, `title`, `view`, `legend`, `elements`, and `relationships`. Elements need `id`, `type`, `name`, `x`, `y`, `width`, `height`; optional fields are `subtype`, `parent`, `description`, `technology`, and `external`. Coordinates are pixels; child coordinates are relative to the parent's origin. Containers require an explicit subtype from the [shape policy](shape-rules.md). Names and responsibilities must come from evidence.

Landscape, Context, and Container pages also require `expected_external_systems`: the complete list of evidenced in-scope system IDs. Each required ID must be a separate software-system node in that page. Use the full [coverage matrix procedure](external-systems.md), not only the exporter's input list; a script cannot discover an integration omitted from its input.

Relationships need `id`, `source`, `target`, and an action phrase in `action`; optionally `technology`, `source_port`, `target_port`, `points`, and `label_offset`. Ports are normalized `[x,y]` pairs in 0..1; choose perimeter ports. Waypoints use **global page coordinates**, including for nested edges; the exporter converts them into parent-relative XML. Label offsets are pixel `[dx,dy]` displacements from the route midpoint. Route arrows through reserved corridors and move captions into empty space. A native Message Bus rotates its port coordinate space: the helper converts global-facing normalized ports before writing `entryX/Y` or `exitX/Y`. Do not double-apply native person/store label margins. Logical frames reserve a bottom caption area. The helper rejects text overflow, sibling overlap, clipped children, unrelated-block crossings, and estimated label collisions with shapes, routes, or frame contours. These conservative checks supplement actual rendering.

Supported views are `landscape`, `context`, `container`, `component`, `dynamic`, `deployment`, and `shape-catalog`. Code diagrams and sequence notation require appropriate native UML/sequence cells authored in the editor or another local exporter; this helper deliberately rejects unsupported views. Do not flatten these views into a misleading C4 container page.

## Offline render, reopen, and review

A local draw.io desktop application must be provisioned before isolation; it is not included in this bundle. No online editor, remote shape library, font download, or plugin fetch is needed. Native local shapes and explicit colors keep the files self-contained. Preserve their license notices when redistributing adaptations.

1. Export the model and run `--check`. It checks native shape/style against supplied templates, label/type agreement, contrast, native editable cells, valid endpoints, frames, and saved external-system IDs.
2. Open the native file in the locally provisioned editor, or use its local export capability. Render every page to SVG or PNG. Inspect title, shape silhouettes, text, contours, captions, arrowheads, and the compact interior grid at the intended reading scale. Record the editor version. A structural check is not a visual certificate.
3. Save or re-export native XML from that editor and rerun `--check` on it. Confirm page, element, and edge counts; stable IDs; real parents; labels; endpoint direction; and coverage against the source register. Reopen/render the saved artifact and inspect again whenever editing changes geometry or routing.
4. Run every applicable official and additional item in the [mandatory checklist](review-checklist.md). If the editor or image inspection is unavailable, deliver a clearly labeled draft with `NOT VERIFIED` for native round-trip/visual gates.

draw.io may append an online-help fallback link to SVG exports. Remove that optional footer locally with `python scripts/export_drawio.py --clean-svg exported.svg --output offline.svg`. This preserves the rendered graph and rejects remaining nonlocal resource links. Inspect the cleaned SVG as the delivered artifact; retain the native `.drawio` separately. The bundled previews use this cleanup.

The included [12-element shape catalog](../assets/drawio/shapes.drawio) and [container example](../assets/drawio/container.drawio), with matching SVG previews, were exported and re-saved through draw.io desktop 32.6.10's local command-line exporter. This confirms native renderer compatibility and XML preservation for these fixtures; it does not certify future diagrams or interactive editing operations that were not performed.
