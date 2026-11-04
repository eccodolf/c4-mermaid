# Correct C4 abstraction mapping

Use the hierarchy in the [official abstractions](https://c4model.com/abstractions): software system -> containers -> components -> code elements. People interact with systems; they are not an extra containment level.

## Classify before drawing

| Abstraction | Classification test | Required evidence | Do not infer from |
|---|---|---|---|
| Person | A human actor, role, or persona interacts with software | Supplied workflow, requirements, or interface use | A guessed customer/admin role |
| Software System | Delivers identifiable value and has a meaningful ownership/responsibility boundary | Purpose, ownership, and what implementation belongs inside | Repository, business capability, bounded context, department, or product name alone |
| Container | An application runtime or logical data store needed by the system | Entry point/process boundary, or controlled schema/bucket/queue and its use | Docker image, folder, library, package, or deployment host alone |
| Component | Related functionality behind an interface within one container runtime | Responsibility, interface/callers, implementation grouping, and parent runtime | Every class, route, React component, namespace, or folder by default |
| Code element | A language-level implementation building block within a component | Actual class, function, interface, enum, object, or relevant schema element | An invented runtime service |

Record the classification rationale and parent before choosing a shape. A convenient rectangle does not establish the abstraction. Resolve ambiguous words such as "service", "module", and "database" into their actual role. If evidence cannot distinguish a standalone worker from an in-process handler, mark the interpretation as tentative rather than asserting a new container.

## View scope

| View | Focus | Expanded elements | Supporting context |
|---|---|---|---|
| L1 System Context | One system | The system stays collapsed | Directly connected people and systems |
| L2 Container | One system | Applications and logical stores | Connected people and other systems |
| L3 Component | One container | Its functional components | Collapsed containers, systems, and people |
| L4 Code | One component | Significant code-level elements | Only what explains the implementation |
| Landscape | An organization or portfolio | People and systems | No single expanded focal system |
| Dynamic | One scenario | Existing model participants | Ordered runtime interactions |
| Deployment | One named environment | Nodes and placed instances | Relevant infrastructure services |

Use L3/L4 selectively. On L3, only one container is decomposed; its siblings remain collapsed. An optional outer system frame can retain the enclosing context. Connect relationships to actual participants, not an anonymous frame.

## Common classification traps

- **Repository != system.** A monorepo can contain several systems, and one system can span repositories. "External" means outside the selected system boundary, including another team's system within the same organization.
- **Runtime != hosting.** A browser SPA and a server API execute in different spaces. Server-rendered pages without a substantial client application may belong to one web container. A VM, Kubernetes pod, Docker container, or database server describes deployment placement; it is not an additional logical application merely because it appears in infrastructure configuration.
- **Library != running application.** Shared code can support components without becoming a network participant. A separately started worker is a candidate container. A handler registered in the API's event loop stays inside that API runtime.
- **Schema/bucket != provider.** Model the logical data store the system controls, even when hosted in a managed cloud service. Keep its physical server/cluster in Deployment. Distinguish a database schema from a server, connection pool, ORM, and repository component.
- **Component != packaging unit.** A component can cross source files or packages. A package can contain several components. Use interfaces and cohesive responsibilities, not a literal directory listing.
- **Microservice is not a fixed C4 level.** Services within one team's system may be groups of application/store containers. Separately owned services may be modeled as software systems from the relevant ownership perspective. Do not promote every API automatically, or treat a service's own schema as an in-process component.
- **Queue/topic != broker.** Model individual logical queues/topics as stores, or state the named channel on a direct interaction. A generic Kafka hub hides the producer/consumer coupling. The broker cluster belongs in Deployment when supported. An event named `OrderCreated` does not prove that the topic has that name.

## Relationships and consistency

Choose an explicit meaning for arrows. `worker -> topic: Subscribes to OrderCreated` represents a dependency; `topic -> worker: Delivers OrderCreated` represents data flow. Keep direction and wording aligned. Mark async behavior explicitly; dashed lines only mean what the legend says.

`API -> store: Reads and writes orders` can be one dependency. A static diagram need not add an HTTP response edge to every request. Dynamic views may show known replies and results; do not invent payloads for symmetry. Add webhooks only with evidence.

An internal L2 relationship does not become an external L1 relationship. Preserve aggregate external interactions when zooming out. If a system-level integration is known but its calling container is not, retain that uncertainty instead of arbitrarily assigning it to the API.

Deployment maps instances back to logical element IDs. Three replicas are three instances of one container. Name the environment, actual placement, and evidenced multiplicity. Development compose files do not establish production topology. A development mock can stand in for a logical external dependency without changing the static model's meaning.

React does not prove HTTPS, a database dependency does not identify its driver or ORM, and an installed payment SDK does not prove an active integration. State unknowns precisely and keep proposed behavior separate from observed behavior.
