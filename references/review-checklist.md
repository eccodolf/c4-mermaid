# Mandatory diagram review

Run this checklist for **each diagram before delivery**, including revisions and exports. Mark every item `PASS`, `FIX`, `NOT VERIFIED`, or `N/A` with a reason. Resolve `FIX` items and rerun affected checks. A draft with a verification limit must be identified as such; do not silently mark unknown checks as passed.

## Official C4 criteria

Adapted, in condensed wording, from Simon Brown's software architecture diagram review checklist, CC BY 4.0. All 21 criteria are included below. Attribution and the full license text are provided [locally](sources.md).

### General

- [ ] G1. A meaningful title is present.
- [ ] G2. The diagram type is clear.
- [ ] G3. Its scope is clear.
- [ ] G4. This diagram contains its own visible notation key in the exported artifact; source comments, another diagram, or accompanying prose alone do not count.

### Elements

- [ ] E1. Every element is named.
- [ ] E2. Every element's abstraction is identifiable.
- [ ] E3. Responsibilities are understandable.
- [ ] E4. Relevant technology is explicit.
- [ ] E5. Element abbreviations are explained.
- [ ] E6. Element colors have clear meanings.
- [ ] E7. Shapes have clear meanings.
- [ ] E8. Icons have clear meanings.
- [ ] E9. Border styles have clear meanings.
- [ ] E10. Size differences have clear meanings.

### Relationships

- [ ] R1. Every arrow explains its intent.
- [ ] R2. Wording agrees with direction.
- [ ] R3. Relevant communication technology is explicit.
- [ ] R4. Relationship abbreviations are explained.
- [ ] R5. Relationship colors are explained.
- [ ] R6. Arrowhead meanings are clear.
- [ ] R7. Line-style meanings are clear.

## Additional mandatory gates for this skill

These extend the official checklist with the user's requirements; they are not claimed as additional official C4 rules.

- [ ] A1. Every abstraction and parent is justified in the evidence register; logical, organizational, and deployment boundaries are distinct.
- [ ] A2. The selected view expands only its intended scope and agrees with related views.
- [ ] A3. Unknowns, assumptions, and proposed changes are explicit; no dependency is inferred solely from installed packages.
- [ ] A4. Every evidenced, in-scope external system is represented by an identifiable system node in each applicable delivered Landscape, System Context, and Container view; the coverage matrix has no unexplained missing nodes.
- [ ] A5. Related Context/Container views retain the same external-system set, and Landscape retains the union for its scope; known cross-boundary relationships remain consistent, and unknown container endpoints are disclosed without omitting systems or inventing callers.
- [ ] L1. Siblings form compact, balanced block rows/grids inside each contour; there are no avoidable empty rows, giant gaps, or oversized frames.
- [ ] L2. Internal padding and routing corridors preserve the readability of names, types, responsibilities, and protocols.
- [ ] L3. Text neither overlaps other text nor covers a foreign shape; text inside its own block fits without clipping.
- [ ] L4. Every label is visibly associated with its arrow; arrowheads and directions remain clear, and routes avoid unrelated blocks.
- [ ] L5. The legend is compact and readable without stretching the architecture into a long strip; visual grouping does not invent semantic containment.
- [ ] V1. Every Mermaid source was rendered with a named version; actual output was inspected, not only parsed.
- [ ] V2. The final exported artifact was checked at its intended size, including title, legend, fonts, bounds, and notation adaptations.
- [ ] O1. All evidence, tools, inference, rendering, and review remained inside the air gap; no external resource was fetched.
- [ ] O2. The transferred bundle passed its local integrity and resource checks, or the verification limit is explicitly reported.
- [ ] S1. Evidence-based abstraction and explicit container subtype agree with the visible type, metadata, and selected glyph; technology or external status has not silently changed the abstraction.
- [ ] S2. Person heads, storage caps/orientation, rounded component/container blocks, and browser headers render correctly; text fits their safe interior regions after resizing. Mermaid shape adaptations are disclosed.
- [ ] S3. Text, including transparent-frame headers, has at least 4.5:1 contrast against its actual background; decorations do not obscure text.
- [ ] S4. The mandatory supplied XML/templates are used; the native library and original source digest are present locally; provenance, adaptation notice, and Apache-2.0 license are preserved.
- [ ] D1. For every C4 architecture view, every architecture element and relationship is a separate native editable cell using the supplied C4 shape/style; no flattened image substitutes for the graph.
- [ ] D2. Saved pages retain stable unique IDs, correct native parents and relative coordinates, typed geometry, named labels, valid endpoints, and intended edge directions.
- [ ] D3. The actual saved file was rendered and inspected in a named local draw.io version; no text overlaps/clips, unrelated-block crossings, hidden captions, or unreadable frame titles remain.
- [ ] D4. Native editor save/re-export and recheck preserve page/element/edge counts, IDs, parents, labels, types, endpoints, and the required external-system set; changed layouts receive another visual review.
- [ ] D5. The `.drawio`, positioned source, preview, requested Mermaid companion, evidence, coverage matrix, and per-view verdict are delivered together without remote resources.

D1-D5 are mandatory for C4 architecture views. For Code/sequence notation use the appropriate native UML/sequence shapes and state helper limitations. Apply S4 to actual draw.io C4 adaptations, not unrelated Mermaid-native symbols. Read [shape-rules.md](shape-rules.md) and [drawio.md](drawio.md) for the checks and exporter limits.

For missing technologies, assess whether the unknown is stated honestly and report the coverage limit. Do not substitute a guessed technology to satisfy E4/R3. Use `N/A` only when a criterion truly does not apply, not when it was skipped.

Keep a compact per-view verdict in the result or accompanying review record: view/scope, rendering version, official criteria status, mapping/layout status, and unresolved limits. Do not paste a large unchecked questionnaire in place of performing the review.

Apply A4/A5 using [external-systems.md](external-systems.md). Record actual node IDs, missing systems, scope exclusions, undelivered views, and discovery/relationship limits. Use `N/A` for diagram types outside these three views; it cannot excuse a relevant external system missing from one of them.
