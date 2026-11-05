#!/usr/bin/env python3
"""Export a positioned C4 model to editable, self-contained draw.io XML."""

import argparse
import base64
import html
import json
import math
from pathlib import Path
import re
from urllib.parse import quote, unquote
import xml.etree.ElementTree as ET
import zlib

from render_shape import wrap_label, THEME, SVG
from drawio_assets import native_geometry, geometry_matches, style_for
from drawio_legend import add_legend
from shape_policy import FRAMES, contrast_ratio, kind_for, normalize, shape_for

VIEWS = ("landscape", "context", "container", "component", "dynamic", "deployment", "shape-catalog")


def visible_kind(element_type):
    return {"system-boundary":"Software System", "container-boundary":"Container"}.get(element_type, kind_for(element_type))


def encode_xml(value):
    encoded = quote(value, safe="~()*!.'-_").encode("utf-8")
    compressor = zlib.compressobj(wbits=-15)
    return base64.b64encode(compressor.compress(encoded) + compressor.flush()).decode("ascii")


def decode_xml(value):
    return unquote(zlib.decompress(base64.b64decode(value), -15).decode("utf-8"))


def rectangle(node):
    return tuple(node[key] for key in ("x", "y", "width", "height"))


def intersects(a, b):
    return min(a[0]+a[2], b[0]+b[2])-max(a[0], b[0]) > 1 and min(a[1]+a[3], b[1]+b[3])-max(a[1], b[1]) > 1


def segment_hits(a, b, box):
    x, y, w, h = box
    x, y, w, h = x+1, y+1, w-2, h-2
    dx, dy = b[0]-a[0], b[1]-a[1]
    lo, hi = 0.0, 1.0
    for p, q in ((-dx, a[0]-x), (dx, x+w-a[0]), (-dy, a[1]-y), (dy, y+h-a[1])):
        if abs(p) < 1e-9:
            if q < 0:
                return False
        elif p < 0:
            lo = max(lo, q/p)
        else:
            hi = min(hi, q/p)
        if lo > hi:
            return False
    return hi-lo > 1e-6


def edge_layout(edge, boxes):
    points = []
    for endpoint in ("source", "target"):
        x, y, w, h = boxes[edge[endpoint]]
        port = edge.get(endpoint + "_port", [.5, .5])
        if len(port) != 2 or any(not isinstance(v, (int, float)) or not math.isfinite(v) or not 0 <= v <= 1 for v in port):
            raise ValueError("Ports must contain two finite coordinates within 0..1.")
        points.append((x+w*port[0], y+h*port[1]))
    route = [points[0]] + [tuple(point) for point in edge.get("points", [])] + [points[1]]
    if any(len(point) != 2 or any(not isinstance(v, (int, float)) or not math.isfinite(v) for v in point) for point in route):
        raise ValueError("Relationship waypoints must contain finite x/y coordinates.")
    lengths = [math.dist(a, b) for a, b in zip(route, route[1:])]
    distance = sum(lengths)/2
    anchor = route[0]
    for a, b, length in zip(route, route[1:], lengths):
        if distance <= length and length:
            fraction = distance/length
            anchor = (a[0]+fraction*(b[0]-a[0]), a[1]+fraction*(b[1]-a[1]))
            break
        distance -= length
    lines = [edge["action"]] + (["[" + edge["technology"] + "]"] if edge.get("technology") else [])
    if any(len(line) > 44 for line in lines):
        raise ValueError("Relationship label is too long: " + edge["id"])
    width = max(len(line)*7 for line in lines) + 12
    height = len(lines)*16+4
    dx, dy = edge.get("label_offset", [0, -24])
    if any(not isinstance(v, (int, float)) or not math.isfinite(v) for v in (dx, dy)):
        raise ValueError("Relationship label offsets must be finite.")
    return route, (anchor[0]+dx-width/2, anchor[1]+dy-height/2, width, height)


def label_lines(node):
    shape = shape_for(node["type"], node.get("subtype"))
    width, height = node["width"], node["height"]
    left = 58 if shape == "microservice" else 30 if shape == "queue" else width*.17 if shape == "infrastructure" else 14
    top = min(width,height)*.45+10 if shape == "person" else height*.1+16 if shape == "browser" else 40 if shape in ("database","bucket","directory") else height*.16 if shape == "infrastructure" else 14
    bottom = height*.16 if shape == "infrastructure" else 25 if shape in ("database","bucket","directory") else 14
    kind = visible_kind(node["type"])
    if node.get("technology"):
        kind += ": " + node["technology"]
    fields = [(node["name"], True), ("[" + kind + "]", False)]
    if node.get("description"):
        fields.append((node["description"], False))
    lines = [(line, bold) for value, bold in fields for line in wrap_label(value, width-2*left, 14)]
    if node["type"] not in FRAMES and len(lines)*18 > height-top-bottom:
        raise ValueError("Text does not fit " + node["id"] + "; increase size or shorten wording.")
    if node["type"] in FRAMES and len(lines)*18 > 44:
        raise ValueError("Frame title/type exceeds its header: " + node["id"])
    return lines, left, top, bottom


def validate_page(page):
    if page.get("view") not in VIEWS or not page.get("title") or not isinstance(page.get("legend"), str) or not page["legend"].strip():
        raise ValueError("Every page needs a supported view, title, and visible legend.")
    nodes = {}
    for node in page["elements"]:
        identifier = node["id"]
        if not re.fullmatch(r"[A-Za-z][A-Za-z0-9_]*", identifier) or identifier.startswith("meta_") or identifier in nodes:
            raise ValueError("Invalid or duplicate element ID: " + identifier)
        selected_shape = shape_for(node["type"], node.get("subtype"))
        if node.get("shape", selected_shape) != selected_shape:
            raise ValueError("Explicit shape conflicts with C4 type/subtype: " + identifier)
        if not node.get("name") or any(not isinstance(node[key], (int, float)) or not math.isfinite(node[key]) for key in ("x", "y", "width", "height")):
            raise ValueError("Element needs a name and finite geometry: " + identifier)
        if min(node["x"], node["y"]) < 0 or node["width"] < 180 or node["height"] < 140:
            raise ValueError("Element geometry is too small or negative: " + identifier)
        if not node.get("parent") and node["y"] < 80:
            raise ValueError("Reserve the top 80 pixels for the title: " + identifier)
        label_lines(node)
        nodes[identifier] = node
    if not nodes:
        raise ValueError("Every page needs elements.")
    def absolute(identifier, chain=()):
        if identifier in chain:
            raise ValueError("Cyclic containment: " + identifier)
        node = nodes[identifier]
        x, y, w, h = rectangle(node)
        parent = node.get("parent")
        if parent:
            if parent not in nodes or nodes[parent]["type"] not in FRAMES:
                raise ValueError("Missing or non-frame parent: " + identifier)
            px, py, pw, ph = absolute(parent, chain + (identifier,))
            footer = 64 if nodes[parent]["type"] in ("system-boundary", "container-boundary") else 20
            if x < 20 or y < 20 or x+w > pw-20 or y+h > ph-footer:
                raise ValueError("Child exceeds parent or its footer/padding: " + identifier)
            x, y = x+px, y+py
        return x, y, w, h
    boxes = {identifier: absolute(identifier) for identifier in nodes}
    if page["view"] in ("context", "landscape") and any(node["type"] not in ("person", "software-system", "group") for node in nodes.values()):
        raise ValueError("Context/Landscape views keep systems collapsed.")
    if page["view"] == "container":
        if sum(node["type"] == "system-boundary" for node in nodes.values()) != 1:
            raise ValueError("A Container view expands one system boundary.")
        if any(node["type"] not in ("person", "software-system", "container", "system-boundary", "group") for node in nodes.values()):
            raise ValueError("A Container view does not decompose components or deployment nodes.")
        for node in nodes.values():
            if node["type"] == "container":
                ancestor = node.get("parent")
                while ancestor and nodes[ancestor]["type"] != "system-boundary":
                    ancestor = nodes[ancestor].get("parent")
                if not ancestor:
                    raise ValueError("Internal containers must be inside the focal system: " + node["id"])
    if page["view"] == "component":
        if sum(node["type"] == "container-boundary" for node in nodes.values()) != 1:
            raise ValueError("A Component view expands one container boundary.")
        for node in nodes.values():
            if node["type"] == "component":
                ancestor = node.get("parent")
                while ancestor and nodes[ancestor]["type"] != "container-boundary":
                    ancestor = nodes[ancestor].get("parent")
                if not ancestor:
                    raise ValueError("Components need their focal container parent: " + node["id"])
    if page["view"] in ("context", "container", "landscape"):
        expected = page.get("expected_external_systems")
        if not isinstance(expected, list):
            raise ValueError("Provide expected_external_systems from the evidence register (an empty list is explicit).")
        if len(set(expected)) != len(expected):
            raise ValueError("Expected external-system IDs must be unique.")
        missing = [identifier for identifier in expected if identifier not in nodes or nodes[identifier]["type"] != "software-system"]
        if missing:
            raise ValueError("Missing external software-system nodes: " + ", ".join(missing))
        undeclared = [node["id"] for node in nodes.values() if node.get("external") and node["type"] == "software-system" and node["id"] not in expected]
        if undeclared:
            raise ValueError("External-system register omits declared external nodes: " + ", ".join(undeclared))
    values = list(nodes.values())
    for i, node in enumerate(values):
        for other in values[i+1:]:
            if node.get("parent") == other.get("parent") and intersects(boxes[node["id"]], boxes[other["id"]]):
                raise ValueError("Sibling blocks overlap: " + node["id"] + " / " + other["id"])
    edge_ids = set(nodes)
    routes, labels = [], []
    for edge in page.get("relationships", []):
        if edge["id"] in edge_ids or not re.fullmatch(r"[A-Za-z][A-Za-z0-9_]*", edge["id"]):
            raise ValueError("Duplicate relationship ID: " + edge["id"])
        edge_ids.add(edge["id"])
        for key in ("source", "target"):
            if edge[key] not in nodes or nodes[edge[key]]["type"] in FRAMES:
                raise ValueError("Relationship must attach to a real element: " + edge["id"])
        if not edge.get("action"):
            raise ValueError("Relationship needs an action: " + edge["id"])
        route, label = edge_layout(edge, boxes)
        for node in nodes.values():
            if node["type"] in FRAMES:
                # Label boxes must not mask the frame title or contour.
                x, y, w, h = boxes[node["id"]]
                borders = [(x, y, w, 3), (x, y+h-3, w, 3), (x, y, 3, h), (x+w-3, y, 3, h), (x, y+h-54, w, 54) if node["type"] in ("system-boundary", "container-boundary") else (x, y, w, 54)]
                if any(intersects(label, border) for border in borders):
                    raise ValueError("Relationship label overlaps a frame/header: " + edge["id"])
                continue
            box = boxes[node["id"]]
            if intersects(label, box):
                raise ValueError("Relationship label overlaps a block: " + edge["id"] + " / " + node["id"])
            if node["id"] not in (edge["source"], edge["target"]) and any(segment_hits(a, b, box) for a, b in zip(route, route[1:])):
                raise ValueError("Relationship crosses an unrelated block: " + edge["id"] + " / " + node["id"])
        if any(intersects(label, other) for other in labels):
            raise ValueError("Relationship labels overlap: " + edge["id"])
        routes.append(route)
        labels.append(label)
    if any(segment_hits(a, b, label) for label in labels for route in routes for a, b in zip(route, route[1:])):
        raise ValueError("A relationship route crosses a label; adjust waypoints/label_offset.")
    return nodes, boxes


def add_object(root, identifier, label, *, style, parent="1", vertex=True, **metadata):
    obj = ET.SubElement(root, "object", id=identifier, label=label, **metadata)
    attrs = {"style": style, "parent": parent, "vertex" if vertex else "edge": "1"}
    cell = ET.SubElement(obj, "mxCell", attrs)
    return cell


def export_model(model):
    profile = model.get("profile", "drawio-c4")
    if profile != "drawio-c4":
        raise ValueError("Native architecture output must use the supplied draw.io C4 palette.")
    palette = THEME["profiles"][profile]
    file = ET.Element("mxfile", host="c4-mermaid-offline", agent="c4-mermaid", compressed="false")
    pages = model["pages"]
    if not pages:
        raise ValueError("At least one page is required.")
    for index, page in enumerate(pages):
        nodes, boxes = validate_page(page)
        diagram = ET.SubElement(file, "diagram", id="page_" + str(index+1), name=page["title"])
        graph = ET.SubElement(diagram, "mxGraphModel", dx="1200", dy="800", grid="1", gridSize="10", page="0", pageScale="1", background=palette["background"])
        root = ET.SubElement(graph, "root")
        ET.SubElement(root, "mxCell", id="0")
        ET.SubElement(root, "mxCell", id="1", parent="0")
        full_width = max(box[0]+box[2] for box in boxes.values()) + 20
        bottom = max(box[1]+box[3] for box in boxes.values())
        used_roles = []
        for node in nodes.values():
            shape = shape_for(node["type"], node.get("subtype"))
            default_role = "infrastructure" if node["type"] in ("deployment-node", "infrastructure-node", "group") else "system" if node["type"] in FRAMES else "person" if shape == "person" else "component" if shape == "component" else "system" if shape == "system" else "container"
            role = node.get("role", ("external-person" if node["type"] == "person" else "external") if node.get("external") else default_role)
            colour = palette["roles"][role]
            if node["type"] not in FRAMES:
                used_roles.append(role)
            lines, left, top, padding_bottom = label_lines(node)
            label = '<div style="line-height:18px">' + '<br>'.join('<b>'+html.escape(line)+'</b>' if bold else html.escape(line) for line, bold in lines) + '</div>'
            fields = native_geometry(node["type"], node.get("subtype"), bool(node.get("external"))).copy()
            fields.update(html="1", whiteSpace="wrap", overflow="hidden", fontFamily="Arial", fontSize="14", fontColor=colour["text"], spacing="0", spacingLeft=str(left), spacingRight=str(left), spacingTop=str(10 if shape == "person" else 0 if shape in ("database", "bucket", "directory") else top), spacingBottom=str(0 if shape in ("database", "bucket", "directory") else padding_bottom), align="center", verticalAlign="middle", resizable="1", metaEdit="1")
            if profile != "drawio-c4" or node["type"] in ("deployment-node", "infrastructure-node", "group"):
                fields.update(fillColor=colour["fill"], strokeColor=colour["stroke"])
            if node["type"] in FRAMES:
                fields.update(fillColor="none", container="1", collapsible="0", connectable="0", align="left", spacingLeft="12", spacingRight="12", spacingTop="10", spacingBottom="10", fontColor="#333333")
                if node["type"] not in ("system-boundary", "container-boundary"):
                    fields["verticalAlign"] = "top"
                else:
                    fields["verticalAlign"] = "bottom"
            style = ";".join(key+"="+value for key,value in fields.items())+";"
            native_type = {"person":"Person", "software-system":"Software System", "container":"Container", "component":"Component", "system-boundary":"SystemScopeBoundary", "container-boundary":"ContainerScopeBoundary"}.get(node["type"], kind_for(node["type"]))
            cell = add_object(root, node["id"], label, style=style, parent=node.get("parent", "1"), c4Type=native_type, c4ModelType=node["type"], c4Name=node["name"], c4Technology=node.get("technology", ""), c4Description=node.get("description", ""), c4Subtype=node.get("subtype", ""), c4Shape=shape, c4Role=role)
            if node["type"] in FRAMES:
                cell.set("connectable", "0")
                if node["type"] in ("system-boundary", "container-boundary"):
                    root[-1].set("c4Application", visible_kind(node["type"]))
            ET.SubElement(cell, "mxGeometry", {**{key: str(node[key]) for key in ("x", "y", "width", "height")}, "as": "geometry"})
        for edge in page.get("relationships", []):
            label = html.escape(edge["action"]) + ("<br>[" + html.escape(edge["technology"]) + "]" if edge.get("technology") else "")
            fields = style_for("Relationship with description and technology").copy()
            fields.update(edgeStyle="none", fontSize="12", fontFamily="Arial", labelBackgroundColor=palette["background"])
            style = ";".join(key+"="+value for key,value in fields.items())+";"
            if edge.get("dashed"):
                style += "dashed=1;"
            for endpoint, prefix in (("source_port", "exit"), ("target_port", "entry")):
                if endpoint in edge:
                    px, py = edge[endpoint]
                    endpoint_node = nodes[edge["source" if endpoint == "source_port" else "target"]]
                    if endpoint_node.get("subtype") == "queue":
                        # Native cylinder direction=south rotates its connection coordinate space.
                        px, py = py, 1-px
                    if not 0 <= px <= 1 or not 0 <= py <= 1:
                        raise ValueError("Ports must be within 0..1.")
                    style += f"{prefix}X={px};{prefix}Y={py};{prefix}Perimeter=0;"
            def ancestors(identifier):
                result = []
                while nodes[identifier].get("parent"):
                    identifier = nodes[identifier]["parent"]
                    result.append(identifier)
                return result
            target_ancestors = ancestors(edge["target"])
            edge_parent = next((identifier for identifier in ancestors(edge["source"]) if identifier in target_ancestors), "1")
            px, py = boxes[edge_parent][:2] if edge_parent != "1" else (0, 0)
            cell = add_object(root, edge["id"], label, style=style, parent=edge_parent, vertex=False, c4Type="Relationship", c4ModelType="relationship")
            cell.set("source", edge["source"])
            cell.set("target", edge["target"])
            geometry = ET.SubElement(cell, "mxGeometry", relative="1", **{"as": "geometry"})
            dx, dy = edge.get("label_offset", [0, -24])
            ET.SubElement(geometry, "mxPoint", x=str(dx), y=str(dy), **{"as": "offset"})
            if edge.get("points"):
                points = ET.SubElement(geometry, "Array", **{"as": "points"})
                for x, y in edge["points"]:
                    ET.SubElement(points, "mxPoint", x=str(x-px), y=str(y-py))
        footer_y = add_legend(root, used_roles, palette, 20, bottom+36, full_width-40, page["legend"], add_object, wrap_label)
        annotations = [("meta_title", page["title"], 10, 50, 20), ("meta_attribution", "C4: Simon Brown, CC BY 4.0. draw.io C4 palette, Apache-2.0.", None, 30, 11)]
        for identifier, value, y, height, font in annotations:
            lines = [line for paragraph in value.splitlines() for line in wrap_label(paragraph, full_width-40, font)]
            height = height or len(lines)*18+16
            y = footer_y if y is None else y
            cell = add_object(root, identifier, '<br>'.join(html.escape(line) for line in lines), style=f"text;html=1;whiteSpace=wrap;overflow=hidden;align=left;verticalAlign=top;fontFamily=Arial;fontSize={font};fontColor={palette['line']};strokeColor=none;fillColor=none;", c4Type="annotation")
            if identifier == "meta_title":
                obj = root[-1]
                obj.set("c4View", page["view"])
                obj.set("c4ExpectedExternalSystems", json.dumps(page.get("expected_external_systems", [])))
            ET.SubElement(cell, "mxGeometry", x="20", y=str(y), width=str(full_width-40), height=str(height), **{"as": "geometry"})
            if identifier != "meta_title":
                footer_y = y+height+20
    return ET.tostring(file, encoding="unicode", xml_declaration=False)


def check_file(path):
    document = ET.parse(path).getroot()
    if document.tag != "mxfile":
        raise ValueError("Expected native mxfile XML, not an image or renamed SVG.")
    total_nodes = total_edges = 0
    for diagram in document.findall("diagram"):
        graph = diagram.find("mxGraphModel")
        if graph is None and diagram.text:
            graph = ET.fromstring(decode_xml(diagram.text))
        if graph is None:
            raise ValueError("Missing page graph.")
        objects = graph.findall("./root/object") + graph.findall("./root/UserObject")
        raw_ids = [element.get("id") for element in graph.iter() if element.get("id") is not None]
        if len(raw_ids) != len(set(raw_ids)):
            raise ValueError("Duplicate saved cell ID.")
        object_map = {obj.get("id"): obj for obj in objects}
        ids = set()
        nodes = {}
        edges = []
        role_colors = {}
        expected_external = []
        for obj in objects:
            identifier = obj.get("id")
            if identifier in ids:
                raise ValueError("Duplicate cell ID: " + str(identifier))
            ids.add(identifier)
            cell = obj.find("mxCell")
            if not identifier or cell is None:
                raise ValueError("Native object requires a stable ID and cell.")
            parent = cell.get("parent")
            chain = {identifier}
            while parent not in ("0", "1"):
                if parent in chain or parent not in object_map or object_map[parent].get("c4ModelType", object_map[parent].get("c4Type")) not in FRAMES:
                    raise ValueError("Invalid or cyclic saved containment: " + identifier)
                chain.add(parent)
                parent = object_map[parent].find("mxCell").get("parent")
            style = cell.get("style", "")
            fields = dict(part.split("=",1) for part in style.split(";") if "=" in part)
            if obj.get("link") or re.search(r"https?://|file://", style, re.I):
                raise ValueError("Linked or remote resources are not allowed in offline draw.io output.")
            if "shape=image" in style or "image=" in style:
                raise ValueError("Image cells do not satisfy native C4 editability.")
            if not obj.get("label"):
                raise ValueError("Missing label: " + str(identifier))
            element_type = obj.get("c4ModelType", obj.get("c4Type"))
            if element_type == "annotation":
                if identifier == "meta_title":
                    expected_external = json.loads(obj.get("c4ExpectedExternalSystems", "[]"))
                continue
            if element_type == "relationship":
                edges.append(cell)
                continue
            shape = shape_for(element_type, obj.get("c4Subtype") or None)
            plain = html.unescape(re.sub(r"<[^>]+>", "", obj.get("label", "")))
            if not any(normalize(value).startswith(normalize(visible_kind(element_type))) for value in re.findall(r"\[([^\]]*)\]", plain)):
                raise ValueError("Visible type label disagrees with C4 metadata: " + str(identifier))
            background = graph.get("background", "#FFFFFF") if fields.get("fillColor") == "none" else fields.get("fillColor", "#FFFFFF")
            if contrast_ratio(fields.get("fontColor", "#152332"), background) < 4.5:
                raise ValueError("Text contrast is below 4.5:1: " + str(identifier))
            if obj.get("c4Shape") != shape:
                raise ValueError("C4 type/shape mismatch: " + str(identifier))
            if not geometry_matches(fields, element_type, obj.get("c4Subtype") or None):
                raise ValueError("Native C4 geometry/style differs from its declared type: " + str(identifier))
            if element_type in FRAMES and (fields.get("fillColor") != "none" or cell.get("connectable") != "0"):
                raise ValueError("Containment frames must be transparent and nonconnectable.")
            nodes[identifier] = element_type
            if element_type not in FRAMES:
                role = obj.get("c4Role")
                if not role:
                    raise ValueError("Missing legend role metadata: " + identifier)
                role_colors[role] = fields.get("fillColor")
        legend = object_map.get("meta_legend")
        if legend is None or not html.unescape(re.sub(r"<[^>]+>", "", legend.get("label", ""))).strip():
            raise ValueError("Every saved page must contain a visible legend.")
        legend_cell = legend.find("mxCell")
        legend_geometry = legend_cell.find("mxGeometry")
        if legend_cell.get("visible", "1") == "0" or legend_geometry is None or float(legend_geometry.get("width", "0")) <= 0 or float(legend_geometry.get("height", "0")) <= 0:
            raise ValueError("Saved legend must remain visible and have positive bounds.")
        legend_style = dict(part.split("=",1) for part in legend_cell.get("style", "").split(";") if "=" in part)
        if legend_style.get("noLabel") == "1" or any(legend_style.get(key) == "0" for key in ("opacity", "textOpacity")):
            raise ValueError("Saved legend text is hidden by its style.")
        legend_background = legend_style.get("fillColor", "none")
        if legend_background == "none":
            legend_background = graph.get("background", "#FFFFFF")
        if contrast_ratio(legend_style.get("fontColor", "#152332"), legend_background) < 4.5:
            raise ValueError("Saved legend text has insufficient contrast.")
        keys = {cell.get("c4LegendRole"):cell for cell in graph.findall("./root/mxCell") if cell.get("c4LegendRole")}
        if set(keys) != set(role_colors):
            raise ValueError("Legend color key does not cover the actual element roles.")
        for role, key in keys.items():
            fields = dict(part.split("=",1) for part in key.get("style", "").split(";") if "=" in part)
            if not key.get("value") or fields.get("fillColor") != role_colors[role] or key.get("visible", "1") == "0":
                raise ValueError("Legend key is missing, hidden, or has the wrong color: " + role)
            if contrast_ratio(fields.get("fontColor", "#152332"), fields["fillColor"]) < 4.5:
                raise ValueError("Legend color row has insufficient text contrast: " + role)
        for edge in edges:
            if edge.get("source") not in nodes or edge.get("target") not in nodes:
                raise ValueError("Dangling relationship endpoint.")
            if nodes[edge.get("source")] in FRAMES or nodes[edge.get("target")] in FRAMES:
                raise ValueError("Relationship is attached to a frame.")
        if any(identifier not in nodes or nodes[identifier] != "software-system" for identifier in expected_external):
            raise ValueError("A required external system is missing from the saved file.")
        if not nodes:
            raise ValueError("Page contains no typed native C4 elements.")
        total_nodes += len(nodes)
        total_edges += len(edges)
    if not document.findall("diagram"):
        raise ValueError("No diagram pages.")
    return {"pages": len(document.findall("diagram")), "elements": total_nodes, "relationships": total_edges}


def clean_svg(source, output):
    """Remove draw.io's optional online help fallback, retaining rendered geometry/text."""
    document = ET.parse(source).getroot()
    if document.tag != "{" + SVG + "}svg":
        raise ValueError("Expected an SVG export.")
    help_page = "https://www.drawio.com/doc/faq/svg-export-text-problems"
    removed = 0
    for parent in document.iter():
        for child in list(parent):
            if child.tag == "{" + SVG + "}switch":
                links = child.findall("{" + SVG + "}a")
                if len(links) == 1 and links[0].get("{http://www.w3.org/1999/xlink}href") == help_page:
                    parent.remove(child)
                    removed += 1
    for element in document.iter():
        for key, value in element.attrib.items():
            if key.rsplit("}", 1)[-1] in ("href", "src") and not value.startswith("#"):
                raise ValueError("SVG still contains a nonlocal resource/link.")
        # This SVG capability identifier is a format feature test, not a resource.
        element.attrib.pop("requiredFeatures", None)
    ET.register_namespace("", SVG)
    ET.register_namespace("xhtml", "http://www.w3.org/1999/xhtml")
    with Path(output).open("w", encoding="utf-8", newline="\n") as stream:
        ET.ElementTree(document).write(stream, encoding="unicode", xml_declaration=True)
    return {"removed_help_fallbacks": removed}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, help="Positioned C4 JSON model; see the bundled examples.")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--check", type=Path, help="Check native editable C4 cells in a generated/saved draw.io file.")
    parser.add_argument("--clean-svg", type=Path, help="Remove the draw.io online-help fallback from an exported SVG; requires --output.")
    args = parser.parse_args()
    try:
        if args.clean_svg:
            if not args.output or args.output.suffix.lower() != ".svg":
                parser.error("Use --clean-svg exported.svg --output offline.svg.")
            print(json.dumps(clean_svg(args.clean_svg, args.output)))
        elif args.check:
            print(json.dumps(check_file(args.check)))
        else:
            if not args.input or not args.output or args.output.suffix.lower() != ".drawio":
                parser.error("Use --input model.json --output diagram.drawio, or --check diagram.drawio.")
            value = export_model(json.loads(args.input.read_text(encoding="utf-8")))
            args.output.parent.mkdir(parents=True, exist_ok=True)
            with args.output.open("w", encoding="utf-8", newline="\n") as output:
                output.write(value)
            print(json.dumps(check_file(args.output)))
    except (ValueError, KeyError, OSError, ET.ParseError) as error:
        parser.exit(1, "draw.io export/check failed: " + str(error) + "\n")


if __name__ == "__main__":
    main()
