# Air-gapped operation

## Operating boundary

Everything this skill teaches or renders is included in this directory: abstraction mapping, seven C4 view scopes, all 21 diagram review criteria, extra acceptance gates, Mermaid syntax guidance, nine source/SVG examples, thirteen parametric shapes, palettes, rendering engine, and license texts. All instruction links resolve to local files. Original source names are attribution, not retrieval instructions.

The package does not include an agent application, model weights, operating system, browser, Python interpreter, or a general-purpose headless browser. Provision those inside the isolated environment before using the skill. Python 3.9 or newer is optional for installation, verification, tests, and vector generation. Mermaid rendering uses the included JavaScript engine in an already-installed browser and does not require Python, Node, npm, a package registry, or a server.

An entire agent workflow is air-gapped only when its inference, tools, telemetry, and storage remain inside that environment. A cloud-only Codex, Claude, Kimi, or DeepSeek service does not become local by loading this package. Skill-format compatibility with a harness is separate from that harness's deployment capabilities. Use an already-provisioned local or in-enclave backend; do not change provider credentials or assume that a local proxy has no upstream connection.

## Transfer and install

1. Transfer the complete `c4-mermaid` directory through the environment's approved media process. A ZIP must contain that directory with `SKILL.md` at its root. Do not transfer only the Markdown entry point.
2. Extract it locally. Keep `bundle-manifest.json`, `README.md`, `agents/`, `references/`, `assets/`, `scripts/`, and `tests/` together.
3. From the extracted directory, run `python scripts/verify_bundle.py`. It checks SHA-256 hashes, required resources, local instruction links, SVG resources, and the viewer's network restrictions. It performs no downloads. Without Python, use the files directly and mark automated integrity verification `NOT VERIFIED`.
4. Run `python scripts/install_skill.py --target codex`, choosing `claude`, `kimi`, or `deepseek` when appropriate. The installer verifies the bundle before copying it and refuses to overwrite an existing directory. The [harness guide](harnesses.md) gives native user/project paths and invocation commands. Manual directory copying is also sufficient.
5. Start a new harness session if discovery is stale. Run `python -m unittest discover -s tests` for optional local packaging checks.

The manifest detects corruption and unexpected changes; it is not a signature or proof of origin. Establish provenance through the approved transfer process. Do not regenerate a manifest to conceal a failed transfer check. `python scripts/verify_bundle.py --write-manifest` is an explicit maintainer operation after reviewing an intentional bundle update.

To update, transfer and verify another complete reviewed bundle. Do not run a Git fetch, package-manager install, or automatic updater inside the isolated environment. Preserve local customizations deliberately; the installer does not merge or remove them.

## Analyze and draw

Use local files and supplied statements as evidence. The repository does not need its dependencies installed or its application running. Do not fetch missing submodules, package documentation, schemas, API specifications, icons, or cloud configuration. Record unavailable evidence as unknown and distinguish observed behavior from a proposal. The [mapping guide](c4-model.md), [notation guide](mermaid.md), and [example analysis](official-examples.md) contain the required method.

Use the bundled Mermaid engine for reproducible syntax support. Do not add include directives, clickable links, remote images, icon packs, remote styles, or font URLs to diagram source. Spell a hostname as plain text when useful; the offline viewer rejects resource schemes and resource directives before rendering. The SVG shape generator uses only Python's standard library and creates vector geometry directly.

## Render and inspect

Open `assets/offline/viewer.html` in a permitted local browser. Select a `.mmd` file, inspect the preview, complete the [mandatory checklist](review-checklist.md), and save SVG with its visible legend. No internet connection is needed. The viewer uses installed font fallbacks and does not download fonts; inspect actual text fit on the target machine because local font metrics may differ.

If the environment permits loopback HTTP but cannot open local HTML, an operator can run `python -m http.server 8766 --bind 127.0.0.1 --directory .` from the bundle root, then open the local loopback address on port 8766 at path `/assets/offline/viewer.html`. Keep the server on loopback and stop it after use. This is optional local interprocess access, not an external service. Do not use it to bypass a host security warning or policy.

The viewer restricts browser connections, frames, workers, fonts, and remote media with a content security policy, and rejects resource-bearing diagram input. This does not isolate the agent application or replace the environment's network boundary. No remote renderer or online fallback is part of this workflow.

If rendering is unavailable, deliver an explicitly unrendered draft and mark V1/V2 as `NOT VERIFIED`. If rendering works but visual inspection is unavailable, report that limit; syntax success is not a reviewed layout. Compact containment, readable text/arrows, and final-export review remain mandatory.

## Attribution and inert identifiers

[Sources and provenance](sources.md) identifies the original authors and adaptations. Full [CC BY 4.0](../assets/offline/LICENSE.CC-BY-4.0) and [Mermaid MIT](../assets/offline/LICENSE.mermaid) texts are bundled. Third-party license text and the unchanged engine may contain source identifiers; XML namespace identifiers in SVG are format identifiers. None is an instruction to access a website or a runtime download dependency. Preserve legal notices when redistributing the bundle.
