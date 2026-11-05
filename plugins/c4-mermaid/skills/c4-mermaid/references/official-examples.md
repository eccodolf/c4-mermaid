# Visual study of official C4 examples

This is historical analysis of the C4 site's examples. For actual output, the [mandatory supplied palette](canonical-assets.md) takes precedence over their original artwork, identity colors, and earlier vector adaptations described here.

On 2026-11-05, all ten original diagrams and eight separate keys linked from Diagrams were inspected as images, in addition to the interactive example. These are observations about those examples, not mandatory notation for every C4 project.

## Visual vocabulary

The light examples use white fill and colored outlines/text. Green identifies the customer, blue the Internet Banking elements, red the email service, and orange the core banking system. Landscape uses another accent for staff and another system. Identity colors persist across abstraction levels. Typography separates name, smaller explicit type/technology, and responsibility. Relationship wording sits near its line, with protocol information beneath. A title can be below a diagram; its position is not an invariant.

| Official view | Observed structure | Apply when modeling |
|---|---|---|
| System Context | One collapsed system, a person, and external systems | Show purpose and direct environment without internal applications |
| Container | Client, backend, static directory, schema, and bucket inside a system boundary | Separate runtime applications from controlled logical stores and external dependencies |
| Component | One backend expanded, surrounding containers collapsed, optional enclosing system frame | Expand one container while preserving its contextual parents and siblings |
| Code | UML interfaces/classes, selected methods, realization and multiplicity | Explain one component's implementation using code-level semantics |
| Landscape | Multiple systems/roles and organizational groups | Describe the portfolio without expanding one focal system |
| Dynamic | The same scenario in numbered collaboration and sequence styles, including replies | Preserve participant identity and actual message order, including known results |
| Deployment | Development, live, and an alternate AWS view with nested nodes, instances, infrastructure, and multiplicity | Name the environment and distinguish logical software from placement and infrastructure |

## Shapes from the keys

| Meaning | Example appearance | Offline shape |
|---|---|---|
| Person | Head and rounded body | `person` |
| Software system | Rounded rectangle | `system` |
| Server application | Block with terminal mark | `application` |
| Browser application | Window with a top bar | `browser` |
| Directory | Folder tab | `directory` |
| Component | Block with two small left tabs | `component` |
| Database/schema | Parallel-sided cylinder | `database` |
| Object-store bucket | Tapered bucket with oval top | `bucket` |
| Logical containment | Solid frame in the system's color | `boundary` |
| Deployment placement | Neutral solid frame and node type | `deployment-node` |
| Organization/group | Neutral dotted frame | `group-boundary` |
| Infrastructure | Neutral oval in Live, optional vendor shapes in the alternate AWS view | `infrastructure` |

`queue` is an explained addition to this bundle; it is not present in those banking images. Vendor icon sets are optional decorations with their own provenance, not a requirement to import remote assets.

A dashed arrow in the main keys means a relationship, not necessarily async communication. The Live key gives a separate meaning to a solid private-network connection. Apply a line distinction only with matching evidence and a legend. The examples reserve space for labels and routes; do not imitate a particular arrangement while losing readability or compact containment.

## Mermaid adaptation boundary

Mermaid can retain these abstractions and interactions but native C4 cannot reproduce every Structurizr glyph, frame, or line style. State shape adaptations. If precise vector artwork is requested, provide the parameterized SVG composition alongside editable Mermaid without claiming that SVG assets extend the native parser.

Attribution: C4 model and original visual references by Simon Brown, c4model.com, CC BY 4.0. The original banking images are not distributed in this bundle. Mermaid previews use Mermaid's renderer; the separate parametric graphics adapt local draw.io C4 assets under Apache-2.0. See [shape rules](shape-rules.md) and [provenance](sources.md).
