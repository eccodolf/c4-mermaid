# Mandatory external-system coverage

Apply this check to every delivered System Landscape, System Context, and Container view. It supplements the C4 review checklist and does not require generating a view the user did not request. Read the [abstraction mapping](c4-model.md) first: external means outside the selected logical system boundary, including another team's system inside the same organization.

## Build the expected set from evidence

Extend the element and relationship registers with every evidenced system that exchanges information with the selected system or its children, in either direction. Include confirmed authentication, payment, business, notification, file-exchange, telemetry, and other technical integrations when they are external software systems. Check active clients/producers, inbound integrations/webhooks, runtime configuration, and supplied architecture facts; an installed library alone is not evidence of an integration.

Identify each external system with a stable ID, name, ownership/boundary rationale, relevant environment, evidence, and known relationship endpoints. Do not confuse a protocol, event name, SDK, hosting node, or the system's own logical data store with another software system. Do not classify every cloud-hosted store as an external system merely because another vendor operates the hardware.

Derive the expected set before reviewing the drawing. Building the set only from already-drawn nodes cannot detect omissions. Use the same evidence baseline and environment across related views; keep proposed integrations separate from existing ones.

## Determine the required nodes by view

| View | Required system coverage |
| --- | --- |
| System Context | Every external system directly connected to the focal system or any of its containers/components, rolled up to system-level interactions |
| Container | The same external-system set as the focal system's Context view, with the focal system's internal containers expanded and external systems remaining identifiable |
| Landscape | All systems in the selected portfolio/organization scope plus every external system directly connected to them; take the union of their external-system sets |

A system may be external to one focal system while remaining inside the Landscape's organization or portfolio. Show it with the correct ownership grouping; do not force an external stereotype or color that contradicts that view's scope. Internal container interactions do not become new external systems when zooming out.

A vendor's own downstream dependency is not automatically a direct dependency of the focal system. Include it only when the chosen Landscape scope or supplied evidence makes it relevant. A system genuinely outside the declared portfolio/focal-system scope can be excluded with a recorded reason; an active integration of an in-scope system cannot be dismissed as out of scope to hide an omission.

## Reconcile the diagrams

For each expected system, verify an actual software-system node with the correct stable identity in each applicable Mermaid source and its rendered output. A mention in a protocol label, description, legend, prose, or another view does not count. A generic "External services" box does not cover several independently identified systems.

Preserve known cross-boundary relationships and their direction when moving between levels. In a Container view, use the evidenced calling/receiving container. If the system integration is confirmed but that container is unknown, still show the external system and add a clear companion note identifying the unresolved caller/receiver. Keep the known system-level relationship in the evidence register; do not attach a guessed edge to a container or frame. Record the relationship-resolution limit separately from node coverage.

Use a compact coverage matrix:

`system ID | name | evidence | relevant scope/environment | Landscape node | Context node | Container node | missing nodes / relationship limits`

Record the actual node ID or `MISSING` for each applicable delivered view. For an undelivered view, state `NOT GENERATED`; do not mark it passed. For a genuinely irrelevant scope, use `N/A` with the boundary reason. If several focal systems or diagrams exist, give each diagram its own column or row group; a node in one Container view does not prove coverage in another.

Compare expected and represented sets. Every missing required node is `FIX`; restore it and repeat layout, relationship, and export review. Keep labels readable and use compact rows, additional space, or a complete overview plus explicitly identified detail views instead of hiding dependencies to make a diagram fit. A deliberately filtered fragment must be identified as partial and cannot pass completeness as a full Landscape, Context, or Container diagram.

If the inspected repository or description may be incomplete, distinguish "all known in-scope systems represented" from exhaustive discovery. Report the evidence limit as `NOT VERIFIED` where it prevents a completeness claim. An unexplained missing system is never a pass. Complete checklist gates A4/A5 for each applicable view.

## Fictional consistency example

Suppose Orders uses Payments and Identity, and Inventory independently uses Shipping. The Orders Context and Container views both need Payments and Identity. A Landscape covering Orders and Inventory also needs Shipping. Shipping does not belong in the Orders views solely because it appears in that larger Landscape. If Identity is confirmed but its calling Orders container is unknown, retain Identity in the Container diagram and disclose the unknown endpoint.
