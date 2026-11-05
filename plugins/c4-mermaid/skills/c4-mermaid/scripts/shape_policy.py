"""C4 abstraction/subtype to visual-shape mapping shared by local exporters."""

SHAPE_KINDS = {
    "person": "Person", "system": "Software System", "application": "Container",
    "browser": "Container", "directory": "Container", "component": "Component",
    "database": "Container", "bucket": "Container", "queue": "Container",
    "boundary": "Boundary", "deployment-node": "Deployment Node",
    "infrastructure": "Infrastructure Node", "group-boundary": "Group",
}
TYPE_SHAPES = {
    "person": "person", "software-system": "system", "component": "component",
    "system-boundary": "boundary", "container-boundary": "boundary",
    "deployment-node": "deployment-node", "infrastructure-node": "infrastructure",
    "group": "group-boundary",
}
CONTAINER_SHAPES = ("application", "browser", "directory", "database", "bucket", "queue")
FRAMES = ("system-boundary", "container-boundary", "deployment-node", "group")


def normalize(value):
    return "".join(character for character in value.lower() if character.isalnum())


def validate_kind(shape, kind):
    expected = SHAPE_KINDS[shape]
    accepted = {normalize(expected)}
    if shape == "boundary":
        accepted.update(("systemboundary", "containerboundary"))
    if kind and normalize(kind) not in accepted:
        raise ValueError(f"Shape {shape!r} represents {expected}, not {kind!r}. Put technology in its own field.")
    return kind or expected


def shape_for(element_type, subtype=None):
    if element_type == "container":
        if subtype not in CONTAINER_SHAPES:
            raise ValueError("Container subtype must be one of: " + ", ".join(CONTAINER_SHAPES))
        return subtype
    if element_type not in TYPE_SHAPES:
        raise ValueError("Unsupported C4 type: " + str(element_type))
    if subtype is not None:
        raise ValueError("Only containers use the subtype field.")
    return TYPE_SHAPES[element_type]


def kind_for(element_type):
    return {"system-boundary": "System Boundary", "container-boundary": "Container Boundary"}.get(
        element_type, "Container" if element_type == "container" else SHAPE_KINDS[TYPE_SHAPES[element_type]])


def contrast_ratio(first, second):
    def luminance(colour):
        if len(colour) != 7 or not colour.startswith("#"):
            raise ValueError("Contrast check requires explicit six-digit colors.")
        values = [int(colour[i:i+2],16)/255 for i in (1,3,5)]
        values = [value/12.92 if value <= .04045 else ((value+.055)/1.055)**2.4 for value in values]
        return sum(value*weight for value,weight in zip(values,(.2126,.7152,.0722)))
    lighter, darker = sorted((luminance(first),luminance(second)), reverse=True)
    return (lighter+.05)/(darker+.05)
