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

The [mandatory supplied palette](canonical-assets.md) controls runtime styles. The historical upstream [frozen palette](../assets/drawio-c4/library.json) contains actual styles and geometry snapshots extracted from draw.io C4 32.6.10. The unchanged source files, commit, hashes, license, and modifications are [bundled locally](sources.md). Runtime helpers interpret frozen data with Python's standard library; they never load remote shapes or execute vendor JavaScript.

`drawio-c4` derives role colors from those actual C4 styles. Container, Component, and external-system text is darkened to meet 4.5:1 contrast. Person2 formulas retain a circular head at different sizes. Browser geometry is parameterized from its paint snapshot; data and message-bus geometry follows cylinder3. Logical frames retain the supplied gray dashed rounded contour and bottom caption. Placement/group primitives are explicit additions. Visible kind labels, metadata, selected geometry, and the legend must agree.

Use `python scripts/render_shape.py --type container --subtype database --profile drawio-c4 --output database.svg` for a typed sample. See `--help` for size, labels, catalogs, and overrides. Unsupported type/subtype combinations and conflicting kinds fail validation. The draw.io exporter uses the supplied native shape identifiers and style definitions; the diagram remains separate editable cells and edges without a lazy library dependency.

Mermaid uses its own glyphs and cannot import these SVG symbols into native C4 syntax. Disclose Mermaid shape adaptations and always provide the exact native draw.io companion for C4 architecture. Never claim that Mermaid itself rendered the draw.io geometry.

Review circular heads, cylinder caps/orientation, browser controls, rounded blocks, readable visible kinds, at least 4.5:1 text contrast, reserved bottom scope captions, and safe interior label areas. Recheck after changing text or size. Every architecture diagram and notation catalog must contain a visible native color-key legend explaining the shapes, colors, borders, arrows, and adaptations actually used. Individual reusable glyph files are element assets, not complete architecture diagrams.
