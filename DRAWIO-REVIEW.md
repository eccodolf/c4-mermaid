# draw.io C4 delivery audit — 1.2.0

Historical audit of version 1.2.0. Current behavior is documented in [README.md](README.md), [the current rendering review](EXACT-MERMAID-REVIEW.md), and [the four-format contract](references/delivery-formats.md).

At version 1.2.0, the skill delivered editable native draw.io architecture for its supported C4 views, using the supplied native draw.io C4 palette. Every diagram must include its own visible legend. The bundle contains no Structurizr assets, theme, or runtime adapter. The supplied XML is mandatory; its exact original bytes, 17 extracted templates, and an 18-entry importable native library are included.

## Asset source and adaptations

Pinned source: `jgraph/drawio`, tag `v32.6.10`, commit `c72c9a98b7a6ce392556ed04c05e0ff19f43f5c3`. The unchanged C4 sidebar, custom shapes, and built-in shapes source are retained under `assets/drawio-c4` with Apache-2.0 license, source hashes, and modification notice. A frozen snapshot contains the actual C4 palette entries and selected vector paint operations. Python uses local data and source-derived geometry; it never executes the vendor JavaScript or downloads a shape library.

Person uses the C4 person2 silhouette; browser uses C4 WebBrowserContainer2; systems, general applications, and components use the C4 rounded blocks. Data stores, including object/file stores, use cylinder3; message buses use its horizontal orientation. Placement/group primitives and reserved bottom logical-scope captions are documented adaptations. Font colors are adjusted where necessary for readable contrast. At that historical version, Mermaid-native output kept its renderer's own glyphs. This limitation was superseded in 1.3.0 by the exact native drawioC4 extension; simplified C4 fallback is now prohibited.

## Observed verification

- draw.io desktop 32.6.10 portable runtime: official release archive checksum matched; executable Authenticode valid, signed by draw.io Ltd. The runtime is used for authoring verification and is not bundled.
- Actual local SVG/PNG export and native XML save/re-export succeeded for the 12-element native shape catalog and the Container fixture with 8 elements and 6 relationships.
- Comparison before/after native re-export preserved IDs, labels, types, parents, endpoints, geometry, and expected external-system metadata.
- Actual previews were inspected: readable bottom logical-scope captions; correct C4 silhouettes; compact internal placement; labels fit; relationship captions avoid unrelated shapes, contours, and routes.
- SVG previews have the optional online-help footer removed locally; remaining external resource links are rejected. Cleaned previews retain the graph; native editable files are kept separately.
- Model checks reject unsupported/mismatched abstractions, text overflow, clipped children, sibling overlap, unrelated-block crossings, label collisions, and missing declared external systems.
- Saved-file checks verify native geometry/style fidelity, native parents, endpoint validity, visible kinds, contrast, external IDs, and a nonempty visible legend with positive bounds and readable text.
- The Mermaid viewer refuses blank legends; loading a source without legend comments clears the previous key. Every bundled Mermaid preview retains its own legend.

All 22 Python tests, the Node source/legend guard test, bundle integrity verification, skill validation, and strict Claude package validators passed for this version. Tests cover rejection behavior and preserved editable graph data; they do not certify future diagrams or model reasoning. Native round-trip testing used the desktop command-line exporter, not an interactive GUI editing session. Each new diagram still requires visual review in the target environment.

## Primary references

- [draw.io C4 notation and library](https://www.drawio.com/docs/diagram-types/c4-modelling/)
- [Pinned C4 palette source](https://github.com/jgraph/drawio/blob/c72c9a98b7a6ce392556ed04c05e0ff19f43f5c3/src/main/webapp/js/diagramly/sidebar/Sidebar-C4.js)
- [Pinned C4 shape source](https://github.com/jgraph/drawio/blob/c72c9a98b7a6ce392556ed04c05e0ff19f43f5c3/src/main/webapp/shapes/mxC4.js)
- [draw.io stencil format](https://github.com/jgraph/drawio/wiki/Shapes-and-Stencils)
- [draw.io file format](https://github.com/jgraph/drawio/wiki/File-Format)

These are repository audit citations. Operational skill references, assets, and licenses are bundled locally for air-gapped use.
