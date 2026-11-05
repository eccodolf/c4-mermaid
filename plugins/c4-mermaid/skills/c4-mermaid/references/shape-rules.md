# Semantic shapes and the draw.io C4 palette

Choose the C4 abstraction from evidence before selecting geometry. A technology name alone cannot determine the abstraction. A managed store owned by another system remains an external software system in the focal context; an in-process storage adapter is a component. External status changes scope/color, never the abstraction.

| Model type | Subtype | draw.io C4 geometry |
| --- | --- | --- |
| person | none | Person2 silhouette with circular head |
| software-system | none | Rounded Software System block |
| container | application | Rounded Container block |
| container | browser | Web Browser Container2 window |
| container | database, bucket, directory | Data Container cylinder |
| container | queue | Message Bus Container: horizontal cylinder |
| container | microservice | Native Microservice Container hexagon |
| component | none | Rounded Component block |
| system-boundary, container-boundary | none | Transparent logical frame |
| deployment-node | none | Transparent placement frame, local adaptation |
| infrastructure-node | none | Infrastructure ellipse, local adaptation |
| group | none | Dotted organizational frame, local adaptation |

The library's Component is a rounded block, not a UML tabbed component. A general application is a plain container, not a terminal window. The C4 library uses its data-container cylinder for stores: do not substitute a bucket silhouette or folder tab. Keep the explicit subtype in the register and visible technology/responsibility so these data-store roles remain distinguishable. Other entries in the frozen palette, including mobile and microservice containers, use only their actual native templates when supported and justified. The helper supports the microservice subtype; unsupported mobile/code/sequence notation must be authored faithfully in the local editor.

The [mandatory supplied palette](canonical-assets.md) controls runtime styles. The historical upstream [frozen palette](../assets/drawio-c4/library.json) contains actual styles and geometry snapshots extracted from draw.io C4 32.6.10. The unchanged source files, commit, hashes, license, and modifications are [bundled locally](sources.md). Native export helpers use frozen data; the exact Mermaid extension executes the pinned original draw.io JavaScript engine locally, with no remote resource loading.

`drawio-c4` derives role colors from those actual C4 styles. Container, Component, and external-system text is darkened to meet 4.5:1 contrast. Person2 formulas retain a circular head at different sizes. The optional Python sample helper parameterizes browser geometry from its paint snapshot and follows cylinder3 for data/message-bus samples; these samples are layout aids. Exact Mermaid executes the original painter instead. Logical frames retain the supplied gray dashed rounded contour and bottom caption. Placement/group primitives are explicit additions. Visible kind labels, metadata, selected geometry, and the legend must agree.

Use `python scripts/render_shape.py --type container --subtype database --profile drawio-c4 --output database.svg` for a typed sample. See `--help` for size, labels, catalogs, and overrides. Unsupported type/subtype combinations and conflicting kinds fail validation. The draw.io exporter uses the supplied native shape identifiers and style definitions; the diagram remains separate editable cells and edges without a lazy library dependency.

The [exact Mermaid extension](exact-mermaid.md) renders the original native draw.io geometry directly. No glyph simplification is permitted. Use its exported SVG in hosts without extension support; a separate native file is not a substitute for accurate Mermaid output.

Review circular heads, cylinder caps/orientation, browser controls, rounded blocks, readable visible kinds, at least 4.5:1 text contrast, reserved bottom scope captions, and safe interior label areas. Recheck after changing text or size. Every C4 architecture diagram and C4 notation catalog must contain a visible native color-key legend explaining the shapes, colors, borders, arrows, and adaptations actually used. Code and sequence views require their own notation-specific legends. Individual reusable glyph files are element assets, not complete architecture diagrams.
