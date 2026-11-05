"""Native compact color-key table for each draw.io page."""
import xml.etree.ElementTree as ET
import html

ROLE_NAMES = {"person":"Person", "external-person":"External Person", "system":"Software System", "external":"External Software System", "external-secondary":"External Software System", "container":"Container", "component":"Component", "infrastructure":"Placement / infrastructure"}


def add_legend(root, roles, palette, x, y, width, notes, add_object, wrap_label):
    rows = list(dict.fromkeys(roles))
    row_height = 30
    table_width = min(360, width)
    cell = add_object(root, "meta_legend", "Legend", style=f"shape=table;startSize=30;container=1;collapsible=0;childLayout=tableLayout;fontSize=16;align=left;verticalAlign=top;fillColor=none;strokeColor=none;fontColor={palette['line']};fontStyle=1;spacingLeft=6;spacing=0;", c4Type="annotation")
    ET.SubElement(cell, "mxGeometry", x=str(x), y=str(y), width=str(table_width), height=str(30+len(rows)*row_height), **{"as":"geometry"})
    for index, role in enumerate(rows):
        identifier = "meta_legend_row_"+str(index)
        row = ET.SubElement(root, "mxCell", id=identifier, parent="meta_legend", value="", vertex="1", style="shape=tableRow;horizontal=0;startSize=0;strokeColor=none;fillColor=none;collapsible=0;")
        ET.SubElement(row, "mxGeometry", y=str(30+index*row_height), width=str(table_width), height=str(row_height), **{"as":"geometry"})
        colour = palette["roles"][role]
        key = ET.SubElement(root, "mxCell", id=identifier+"_key", parent=identifier, vertex="1", value=ROLE_NAMES[role], c4LegendRole=role, style=f"shape=partialRectangle;html=1;whiteSpace=wrap;connectable=0;strokeColor=none;fillColor={colour['fill']};fontColor={colour['text']};top=0;left=0;bottom=0;right=0;align=left;spacingLeft=10;fontSize=13;")
        ET.SubElement(key, "mxGeometry", width=str(table_width), height=str(row_height), **{"as":"geometry"})
    side_by_side = width >= 740
    notes_x = x+table_width+30 if side_by_side else x
    notes_y = y+30 if side_by_side else y+30+len(rows)*row_height+18
    notes_width = min(680,width-table_width-30) if side_by_side else width
    lines = [line for paragraph in notes.splitlines() for line in wrap_label(paragraph, notes_width, 13)]
    note = add_object(root, "meta_notation", '<br>'.join(html.escape(line) for line in lines), style=f"text;html=1;whiteSpace=wrap;overflow=hidden;align=left;verticalAlign=top;fontFamily=Arial;fontSize=13;fontColor={palette['line']};fillColor=none;strokeColor=none;", c4Type="annotation")
    ET.SubElement(note, "mxGeometry", x=str(notes_x), y=str(notes_y), width=str(notes_width), height=str(len(lines)*18+12), **{"as":"geometry"})
    return max(y+30+len(rows)*row_height,notes_y+len(lines)*18+12)+24
