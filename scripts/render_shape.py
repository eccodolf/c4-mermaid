"""Create offline, parametric C4 SVG shapes; Python standard library only."""
import argparse
import json
import math
from pathlib import Path
import re
import xml.etree.ElementTree as ET
from shape_policy import kind_for, normalize, shape_for, validate_kind
from drawio_assets import SHAPES as DRAWIO_SHAPES, append_geometry, default_profile

ROOT = Path(__file__).resolve().parents[1]
THEME = json.loads((ROOT / 'assets/c4-theme.json').read_text(encoding='utf-8'))
THEME['profiles']['drawio-c4'] = default_profile()
SHAPES = ('person', 'system', 'application', 'browser', 'directory', 'component', 'database', 'bucket', 'queue', 'boundary', 'deployment-node', 'infrastructure', 'group-boundary')
SVG = 'http://www.w3.org/2000/svg'
ET.register_namespace('', SVG)
ATTRIBUTION = 'C4 reference: Simon Brown, c4model.com, CC BY 4.0. Shape assets adapted from draw.io C4, Apache-2.0; bundled source revisions and license included.'

def element(parent, tag, **attrs):
    return ET.SubElement(parent, f'{{{SVG}}}{tag}', {key.replace('_', '-'): str(value) for key, value in attrs.items()})

def wrap_label(value, width, font):
    """Wrap words using conservative Arial advances; split only words wider than the box."""
    def advance(text):
        return sum(font*(.5 if char.isspace() else 1.1 if char in 'MWmw@%' or not char.isascii() else .8) for char in text)
    lines, current = [], ''
    for word in value.split():
        chunks, chunk = [], ''
        for char in word:
            if chunk and advance(chunk+char)>width:
                chunks.append(chunk)
                chunk=''
            chunk+=char
        chunks.append(chunk)
        for chunk in chunks:
            candidate=(current+' '+chunk).strip()
            if current and advance(candidate)>width:
                lines.append(current)
                current=chunk
            else:
                current=candidate
    if current:
        lines.append(current)
    return lines

def render_shape(shape, *, title='', kind='', technology='', description='', width=320, height=220,
                 profile='example-light', role=None, fill=None, stroke=None, text_color=None):
    if shape not in SHAPES:
        raise ValueError('Unknown shape: ' + shape)
    kind = validate_kind(shape, kind)
    if not isinstance(width, int) or not isinstance(height, int) or not 180 <= width <= 4000 or not 160 <= height <= 4000:
        raise ValueError('Width must be 180..4000 and height 160..4000 pixels.')
    palette = THEME['profiles'][profile]
    default_role = {'person':'person', 'system':'system', 'component':'component', 'boundary':'system',
                    'deployment-node':'infrastructure', 'infrastructure':'infrastructure', 'group-boundary':'infrastructure'}.get(shape, 'container')
    colours = palette['roles'][role or default_role].copy()
    for key, value in [('fill', fill), ('stroke', stroke), ('text', text_color)]:
        if value is not None:
            if not re.fullmatch(r'#[0-9A-Fa-f]{6}', value):
                raise ValueError('Colours must be six-digit hex, for example #1168BD.')
            colours[key] = value
    if shape in ('boundary','deployment-node','group-boundary') and text_color is None:
        colours['text'] = colours['stroke']
    root = ET.Element(f'{{{SVG}}}svg', {'viewBox': f'0 0 {width} {height}', 'width': str(width),
                       'height': str(height), 'role': 'img', 'aria-labelledby': 'shape-title shape-desc'})
    element(root, 'title', id='shape-title').text = title or shape.title()
    element(root, 'desc', id='shape-desc').text = description or 'Parametric C4 ' + shape
    element(root, 'metadata').text = ATTRIBUTION
    element(root, 'rect', x=0, y=0, width=width, height=height, fill=palette['background'])
    g = element(root, 'g', fill=colours['fill'], stroke=colours['stroke'], stroke_width=2)
    left, right, top, bottom = 20, width - 20, 24, height - 20
    text_top = 40
    if shape in DRAWIO_SHAPES:
        left, right, text_top, bottom = append_geometry(g, shape, left, top, right, bottom, colours, SVG)
    elif shape == 'infrastructure':
        element(g, 'ellipse', cx=width/2, cy=(top+bottom)/2, rx=(right-left)/2, ry=(bottom-top)/2)
        horizontal_inset=(right-left)*.15
        left+=horizontal_inset
        right-=horizontal_inset
        vertical_inset=(bottom-top)*.15
        text_top=top+vertical_inset
        bottom-=vertical_inset
    else:
        attrs = {'x':left, 'y':top, 'width':right-left, 'height':bottom-top}
        if shape in ('system','deployment-node','boundary'):
            attrs.update(rx=6)
        if shape in ('boundary','deployment-node','group-boundary'):
            attrs.update(fill='none')
        if shape == 'group-boundary':
            attrs.update(stroke_dasharray='2 5')
        element(g, 'rect', **attrs)
    font = 14
    lines = []
    default_kind = {'person':'Person', 'system':'Software System', 'component':'Component', 'boundary':'Boundary',
                    'deployment-node':'Deployment Node', 'infrastructure':'Infrastructure Node', 'group-boundary':'Group'}.get(shape, 'Container')
    for value, bold in [(title or shape.title(), True), (f'[{kind or default_kind}' + (': '+technology if technology else '') + ']', False), (description, False)]:
        for line in wrap_label(value, right-left-24, font):
            lines.append((line, bold))
    available = bottom - text_top - 12
    if len(lines)*19 > available:
        raise ValueError('Text does not fit: shorten labels or increase width/height.')
    y = text_top + (16 if shape in ('boundary','deployment-node','group-boundary') else max(16, (available-len(lines)*19)/2 + 16))
    for line, bold in lines:
        element(root, 'text', x=(left+right)/2, y=y, fill=colours['text'],
                font_family='Arial, sans-serif', font_size=font, font_weight='bold' if bold else 'normal', text_anchor='middle').text = line
        y += 19
    return ET.tostring(root, encoding='unicode', xml_declaration=False)

def render_catalog(profile):
    height=math.ceil(len(SHAPES)/3)*250+150
    root = ET.Element(f'{{{SVG}}}svg', {'viewBox':f'0 0 1020 {height}', 'width':'1020', 'height':str(height), 'role':'img'})
    element(root, 'title').text = 'C4 parametric vector shapes — ' + profile
    element(root, 'metadata').text = ATTRIBUTION
    background = THEME['profiles'][profile]['background']
    element(root, 'rect', x=0, y=0, width=1020, height=height, fill=background)
    for index, shape in enumerate(SHAPES):
        node = ET.fromstring(render_shape(shape, title=shape.title(), description='Offline SVG', profile=profile))
        node.set('x', str(index%3*340+10))
        node.set('y', str(index//3*250+10))
        # Independent accessibility IDs remain unique in the assembled catalogue.
        node.set('aria-labelledby', f'{shape}-title {shape}-desc')
        for child in node.iter():
            if child.get('id'):
                child.set('id', child.get('id').replace('shape-', shape+'-'))
        root.append(node)
    key = 'Legend: Draw.io C4 glyphs; person silhouette = Person; rounded blocks = System, Container or Component as labeled. Cylinder = data container (including file/object stores); horizontal cylinder = message bus. Solid frames = logical/placement scope; dotted frame = organization. Colors identify named roles; sizes fit text.'
    for index, line in enumerate(wrap_label(key, 980, 12)):
        element(root, 'text', x=20, y=height-110+index*18, font_family='Arial, sans-serif', font_size=12, fill=THEME['profiles'][profile]['line']).text = line
    element(root, 'text', x=20, y=height-20, font_family='Arial, sans-serif', font_size=12,
            fill=THEME['profiles'][profile]['line']).text = 'C4: Simon Brown · CC BY 4.0 · Shapes adapted from draw.io C4 · Apache-2.0'
    return ET.tostring(root, encoding='unicode')

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--shape', choices=SHAPES)
    parser.add_argument('--type', choices=('person','software-system','container','component','system-boundary','container-boundary','deployment-node','infrastructure-node','group'))
    parser.add_argument('--subtype', choices=('application','browser','directory','database','bucket','queue'))
    parser.add_argument('--catalog', action='store_true', help='Render all available shapes in one SVG')
    parser.add_argument('--title', default='')
    parser.add_argument('--kind', default='', help='Explicit C4 type, e.g. Container')
    parser.add_argument('--technology', default='')
    parser.add_argument('--description', default='')
    parser.add_argument('--width', type=int, default=320)
    parser.add_argument('--height', type=int, default=220)
    parser.add_argument('--profile', choices=THEME['profiles'], default=THEME['default_profile'])
    parser.add_argument('--role', choices=THEME['profiles']['example-light']['roles'])
    parser.add_argument('--fill')
    parser.add_argument('--stroke')
    parser.add_argument('--text-color')
    parser.add_argument('--output', type=Path, required=True)
    args = vars(parser.parse_args())
    output, catalog = args.pop('output'), args.pop('catalog')
    try:
        element_type, subtype = args.pop('type'), args.pop('subtype')
        if element_type:
            selected = shape_for(element_type, subtype)
            if args['shape'] and args['shape'] != selected:
                raise ValueError('Explicit shape conflicts with the C4 type/subtype.')
            args['shape'] = selected
            if args['kind'] and normalize(args['kind']) != normalize(kind_for(element_type)):
                raise ValueError('Explicit kind conflicts with the C4 type.')
            args['kind'] = kind_for(element_type)
        elif subtype:
            raise ValueError('--subtype requires --type container.')
        args['shape'] = args['shape'] or 'system'
        svg = render_catalog(args['profile']) if catalog else render_shape(**args)
    except (ValueError, KeyError) as error:
        parser.error(str(error))
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(svg, encoding='utf-8')
    print(output.resolve())

if __name__ == '__main__':
    main()
