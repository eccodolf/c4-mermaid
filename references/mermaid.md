# Mermaid notation, compact layout, and compatibility

## Visual profiles and shapes

Always use the [mandatory supplied assets](canonical-assets.md) as the C4 notation source. Apply their dark-blue Person, blue System, cyan Container, light-cyan Component, and muted external-role colors. Use explicit labels and readable font contrast. Native draw.io exact shapes and a visible color-key legend are mandatory companions; Mermaid cannot import native draw.io assets.

Use the [semantic mapping](shape-rules.md): rounded blocks, person2, cylinder3 stores/message buses, the microservice hexagon, browser container, and gray dashed rounded logical scopes with bottom captions. Mermaid-native geometry and label positions may differ; disclose each applicable adaptation. Never describe invented folder/bucket/terminal/UML-component artwork as the supplied C4 assets.

## Native C4

```text
Person(actor, "Customer", "Places orders")
System(orders, "Orders", "Accepts customer orders")
System_Ext(payments, "Payments", "Authorizes payments")
System_Boundary(system_scope, "Orders system") { ... }
Container(api, "Orders API", "Node.js", "Accepts orders")
ContainerDb(store, "Orders store", "PostgreSQL schema", "Stores orders")
ContainerQueue(topic, "orders.created", "Kafka topic", "Stores OrderCreated events")
Container_Boundary(api_scope, "Orders API") { ... }
Component(handler, "Order endpoint", "HTTP handler", "Validates requests")
Rel(api, store, "Writes orders", "PostgreSQL protocol")
UpdateElementStyle(api, $bgColor="#FFFFFF", $fontColor="#1168BD", $borderColor="#1168BD")
UpdateRelStyle(api, store, $textColor="#444444", $lineColor="#666666")
UpdateLayoutConfig($c4ShapeInRow="3", $c4BoundaryInRow="1")
```

Style **element IDs**, not C4 type names. Style every meaningful node explicitly. `System_Boundary` describes a system; `Container_Boundary` describes a container. Do not copy a semantically misleading boundary macro just because another tool's example parses it.

- Native C4 does not promise full C4-PlantUML compatibility. Do not copy `!include`, `SHOW_LEGEND`, `LAYOUT_WITH_LEGEND`, `AddElementTag`, or `Lay_R`.
- Do not mix flowchart `classDef`, `style`, or `-->` with C4 macros.
- Relationship direction macros are not reliable hard layout constraints. Declaration order and `UpdateLayoutConfig` affect placement. Target-supported YAML `config.c4.c4ShapeMargin` and `c4ShapePadding` provide spacing; tune `UpdateRelStyle` offsets only after rendering.
- Do not solve one collision by moving a label far away from its relationship. Create a corridor, shorten wording without losing meaning, reorder blocks, or choose a better renderer/layout.
- Prefer separately directed, clearly labeled relationships over `BiRel` in static views.
- `C4Dynamic` uses declaration order for sequence. Do not rely on arbitrary `RelIndex` numbers. Use `sequenceDiagram` for appropriate branching/parallelism. Avoid raw semicolons in sequence notes/messages, or escape them using supported entity syntax.
- `C4Deployment` uses `Deployment_Node(...) { ... }` and placed `Container`/store elements. Do not invent a `ContainerInstance` Mermaid macro.
- Native Component/Container may lack the original UML, browser, folder, terminal, or bucket glyph. Native frames and line styles also differ. Explain the adaptation; separate SVG assets do not change native Mermaid's shapes.
- Native C4 has no built-in legend command. Supply a visible companion key; the offline viewer includes its legend field in SVG exports. Never disguise legend samples as architecture systems.

## Compact block layout: required construction strategy

1. Choose a dominant reading direction from the actual interactions. Group siblings inside their correct parent contour in short rows or a balanced grid. Prefer a roughly balanced interior to a single excessively long chain or many sparse rows.
2. Give blocks consistent dimensions where their content permits. Reserve space for name, explicit type/technology, and a concise responsibility. Wrap at sensible words. Increase a block or shorten wording before shrinking text.
3. Use modest, consistent inter-block gaps and boundary padding. Increase only the corridor that needs a relationship label. Do not inflate every margin to compensate for one difficult arrow.
4. Place highly connected siblings near each other. Align edges and use direct or orthogonal routes where useful. Minimize crossings; route around unrelated blocks and keep arrowheads outside label areas.
5. Keep labels beside the correct segment and their protocol lines together. Avoid labels on boundary titles or on other relationships. A shape that visually contains its own text is expected; text crossing a foreign shape is a failure.
6. Trim excessive interior whitespace after routing. Confirm the parent frame hugs the block arrangement with usable padding. Place a short legend below/alongside the diagram; do not let an unconnected legend column determine the full architecture's height.
7. Re-render after every relevant edit. Compare the actual layout to a more compact candidate where waste is evident. Reject compaction that harms readability or changes real containment. If native layout cannot meet these requirements, use flowchart or split into focused, mutually consistent views.

Compactness is a constrained design objective, not a fixed global node-count/area ratio. Different label lengths and routes need different space. Do not fabricate groups or invisible architecture dependencies merely to coerce layout. Any layout-only connector must be demonstrably invisible in export, separated from the evidence model, and justified; prefer ordinary layout settings first.

## Portable flowchart representation

Use `flowchart`, `subgraph`, `classDef`, `class`, `style`, and `linkStyle default`. Quote edge labels: `a -->|"Sends POST /orders - HTTP(S); assumption A1"| b`. Dashed example: `a -.->|"Subscribes to events"| b`. Unquoted punctuation can break parsing.

| C4 element | Portable shape | Adaptation |
|---|---|---|
| Person | `actor(["Customer<br/>[Person]<br/>Places orders"])` | Capsule replaces the person glyph |
| System/Container/Component | `api["Orders API<br/>[Container: Node.js]<br/>Accepts orders"]` | Plain block without specialized icons |
| Store/topic | `store[("Orders<br/>[Container: PostgreSQL]<br/>Stores orders")]` | Cylinder with an explicit store type |
| Logical boundary | `subgraph scope["Orders [Software System]"]` | Style and name the frame explicitly |

Copy the selected palette into classes. A canonical logical frame is gray, dashed, rounded, and captioned at the bottom; organizational grouping is explicitly distinct. Deployment frames identify placement. A dark export needs an explicit background and readable legend colors.

Prefer the compact `container-flowchart.mmd` arrangement. Its companion legend is available through `%% legend:` comments and must be displayed with the diagram; it is not optional. If an in-diagram key is required, use a small clearly marked group and check that it does not stretch the layout.

## Sources, rendering, and vectors

Use stable ASCII snake_case IDs and clear labels. Do not use `end` as an ID. Escape labels with target-supported syntax rather than injecting user HTML. Check every line break in the actual diagram type.

`assets/templates` contains context, container, component, code, landscape, dynamic, sequence, deployment, and flowchart examples. They are fictional, not evidence about the user's repository. Examples do not authorize inventing their participants or messages in another model.

Open `assets/offline/viewer.html`, load a `.mmd`, render, and export SVG with the visible key. No CDN, Node installation, server, or external font is required for normal use. If Mermaid CLI is already available, `mmdc -i input.mmd -o output.svg -b white` is another local option. Bundled rendering does not prove compatibility with an older target renderer.

The viewer preserves SVG whitespace, checks text against diagram bounds, checks external labels against other labels/nodes, and checks internal label bounds where the renderer exposes its block geometry. Detected text problems block export. Manually check remaining shape-specific containment, edge routes, arrowheads, compactness, legend, and intended export size. The detector is supplemental and conservative; it does not certify the diagram or the entire mandatory checklist. Check exported SVG in the intended viewer/rasterizer: lost spaces can join words, and restored spaces can reveal text overflow. Use explicit supported line breaks and recheck instead of accepting either problem.

Generate a vector component with `python scripts/render_shape.py --shape component --title "Order intake" --kind Component --technology Python --width 440 --height 260 --profile drawio-c4 --output component.svg`. `--fill`, `--stroke`, and `--text-color` override colors; `--catalog` renders all fourteen parameterized variants. The generator rejects text exceeding available height and recalculates geometry rather than stretching it.
