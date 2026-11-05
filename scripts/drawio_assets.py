"""Offline vector adapters for the pinned draw.io C4 palette (Apache-2.0)."""
import json
from pathlib import Path
import xml.etree.ElementTree as ET

ASSETS = Path(__file__).resolve().parents[1] / "assets/drawio-c4"
LIBRARY = json.loads((ASSETS / "library.json").read_text(encoding="utf-8"))
TEMPLATES = json.loads((ASSETS / "native-templates.json").read_text(encoding="utf-8"))
ENTRIES = {entry["name"]: entry for entry in TEMPLATES["entries"]}
SHAPES = ("person", "system", "application", "browser", "directory", "component", "database", "bucket", "queue", "microservice")


def style_for(name):
    return dict(part.split("=", 1) for part in ENTRIES[name]["style"].split(";") if "=" in part)


def default_profile():
    roles = {}
    for role, name in (("person", "Person"), ("external-person", "External Person"), ("system", "Software System"), ("container", "Container"), ("component", "Component"), ("external", "External Software System")):
        style = style_for(name)
        roles[role] = {"fill": style["fillColor"].upper(), "stroke": style["strokeColor"].upper(), "text": style["fontColor"].upper()}
        if role in ("container", "component", "external"):
            roles[role]["text"] = "#152332"
        if role == "external":
            roles[role]["text"] = "#000000"
    roles["external-secondary"] = roles["external"].copy()
    roles["infrastructure"] = {"fill":"#FFFFFF", "stroke":"#444444", "text":"#444444"}
    return {"background":"#FFFFFF", "line":"#404040", "boundary":"#666666", "roles":roles}


def entry_for(element_type, subtype=None, external=False):
    if element_type == "person":
        return "External Person" if external else "Person"
    if element_type == "software-system":
        return "External Software System" if external else "Software System"
    if element_type == "container":
        return {"application":"Container", "browser":"Web Browser Container", "database":"Data Container", "bucket":"Data Container", "directory":"Data Container", "queue":"Message Bus Container", "microservice":"Microservice Container"}[subtype]
    return {"component":"Component", "system-boundary":"System scope boundary", "container-boundary":"Container scope boundary"}.get(element_type)


def native_geometry(element_type, subtype=None, external=False):
    entry = entry_for(element_type, subtype, external)
    if entry:
        return style_for(entry)
    return {"shape":"ellipse"} if element_type == "infrastructure-node" else {"shape":"rectangle", "rounded":"0", "fillColor":"none", "dashed":"1" if element_type == "group" else "0", "dashPattern":"2 5"}


def geometry_matches(fields, element_type, subtype=None):
    expected = native_geometry(element_type, subtype)
    for key in ("shape", "rounded", "direction", "arcSize", "absoluteArcSize", "size", "fixedSize", "dashed", "dashPattern"):
        default = "rectangle" if key == "shape" else "east" if key == "direction" else "0" if key in ("rounded", "dashed", "absoluteArcSize", "fixedSize") else None
        actual, value = fields.get(key, default), expected.get(key, default)
        if actual != value:
            return False
    if element_type in ('system-boundary', 'container-boundary') and fields.get('verticalAlign') != 'bottom':
        return False
    return True


def append_geometry(parent, shape, left, top, right, bottom, colours, namespace):
    width, height = right-left, bottom-top
    def add(tag, attrs, fill="fill", stroke="stroke"):
        attrs.update(fill="none" if fill == "none" else colours[fill], stroke="none" if stroke == "none" else colours[stroke])
        attrs.update({"data-fill-role":fill, "data-stroke-role":stroke})
        return ET.SubElement(parent, "{"+namespace+"}"+tag, {key:str(value) for key,value in attrs.items()})
    if shape == "person":
        # Exact person2 dimensions from mxC4.js; unlike a stretched snapshot the head stays circular.
        size = min(width*.45, height*.45)
        radius = size/2
        body_top = top+size*.8
        add("rect", {"x":left,"y":body_top,"width":width,"height":bottom-body_top,"rx":radius})
        add("circle", {"cx":left+width/2,"cy":top+radius,"r":radius})
        return left+12, right-12, top+size+10, bottom
    if shape == "microservice":
        cut = min(50, width/2)
        add("path", {"d":f"M {left+cut} {top} L {right-cut} {top} L {right} {top+height/2} L {right-cut} {bottom} L {left+cut} {bottom} L {left} {top+height/2} Z"})
        return left+cut, right-cut, top+14, bottom-8
    if shape == "browser":
        # Replay a frozen paint snapshot of the actual draw.io C4 WebBrowserContainer2.
        source = LIBRARY["geometry"]["browser"]
        sx, sy = width/source["width"], height/source["height"]
        fill, stroke, path = "fill", "stroke", []
        for operation, *args in source["operations"]:
            if operation == "setFillColor":
                fill = "stroke" if args[0] == "stroke" else "fill"
            elif operation == "setStrokeColor":
                stroke = "stroke"
            elif operation == "begin":
                path = []
            elif operation in ("moveTo", "lineTo"):
                path.append(("M" if operation == "moveTo" else "L") + f" {left+args[0]*sx} {top+args[1]*sy}")
            elif operation == "arcTo":
                rx, ry, angle, large, sweep, x, y = args
                path.append(f"A {rx*sx} {ry*sy} {angle} {large} {sweep} {left+x*sx} {top+y*sy}")
            elif operation == "close":
                path.append("Z")
            elif operation in ("fillAndStroke", "fill", "stroke") and path:
                add("path", {"d":" ".join(path)}, fill if operation != "stroke" else "none", stroke if operation != "fill" else "none")
                # draw.io calls fill twice on the same browser interior; one paint suffices.
                path = []
        return left+12, right-12, top+height*22/220+14, bottom-8
    if shape in ("database", "bucket", "directory", "queue"):
        # C4 data containers use cylinder3, including file/object stores. No bucket/folder glyph is invented.
        horizontal = shape == "queue"
        w, h = (height, width) if horizontal else (width, height)
        size = min(h*.5, float(style_for("Data Container").get("size", 15)))
        def point(x, y):
            return (left+width-y, top+x) if horizontal else (left+x, top+y)
        def move(command, x, y):
            px, py = point(x,y)
            return f"{command} {px} {py}"
        def arc(x, y):
            px, py = point(x,y)
            rx, ry = (size,w/2) if horizontal else (w/2,size)
            return f"A {rx} {ry} 0 0 1 {px} {py}"
        path = [move("M",0,size),arc(w/2,0),arc(w,size),move("L",w,h-size),arc(w/2,h),arc(0,h-size),"Z"]
        add("path", {"d":" ".join(path)})
        add("path", {"d":" ".join([move("M",w,size),arc(w/2,2*size),arc(0,size)])}, "none")
        return (left+2*size+10,right-14,top+14,bottom-14) if horizontal else (left+14,right-14,top+2*size+10,bottom-size-10)
    # General container/system/component shapes are rounded blocks in the actual C4 palette.
    name = {"system":"Software System", "component":"Component"}.get(shape,"Container")
    arc = float(style_for(name).get("arcSize",10))/100*min(width,height)/2
    add("rect", {"x":left,"y":top,"width":width,"height":height,"rx":arc})
    return left+8, right-8, top+14, bottom-8
