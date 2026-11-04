"""Create offline, parametric C4 SVG shapes; Python standard library only."""
import argparse
import json
import math
from pathlib import Path
import re
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
THEME = json.loads((ROOT / 'assets/c4-theme.json').read_text(encoding='utf-8'))
SHAPES = ('person', 'system', 'application', 'browser', 'directory', 'component', 'database', 'bucket', 'queue', 'boundary', 'deployment-node', 'infrastructure', 'group-boundary')
SVG = 'http://www.w3.org/2000/svg'
ET.register_namespace('', SVG)
ATTRIBUTION = 'C4 model and visual reference: Simon Brown, c4model.com, CC BY 4.0. Independently drawn adaptation.'

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
    root = ET.Element(f'{{{SVG}}}svg', {'viewBox': f'0 0 {width} {height}', 'width': str(width),
                       'height': str(height), 'role': 'img', 'aria-labelledby': 'shape-title shape-desc'})
    element(root, 'title', id='shape-title').text = title or shape.title()
    element(root, 'desc', id='shape-desc').text = description or 'Parametric C4 ' + shape
    element(root, 'metadata').text = ATTRIBUTION
    element(root, 'rect', x=0, y=0, width=width, height=height, fill=palette['background'])
    g = element(root, 'g', fill=colours['fill'], stroke=colours['stroke'], stroke_width=2)
    left, right, top, bottom = 20, width - 20, 24, height - 20
    text_top = 40
    if shape == 'person':
        radius = 24
        element(g, 'circle', cx=width / 2, cy=radius + 8, r=radius)
        top = 60
        element(g, 'rect', x=left, y=top, width=right-left, height=bottom-top, rx=25)
        text_top = top + 12
    elif shape == 'database':
        ry = 15
        element(g, 'path', d=f'M {left} {top+ry} A {(right-left)/2} {ry} 0 0 1 {right} {top+ry} '
                f'L {right} {bottom-ry} A {(right-left)/2} {ry} 0 0 1 {left} {bottom-ry} Z')
        element(g, 'ellipse', cx=width/2, cy=top+ry, rx=(right-left)/2, ry=ry)
        text_top = top + 2*ry + 8
    elif shape == 'bucket':
        ry, inset = 15, (right-left)*.12
        element(g, 'path', d=f'M {left} {top+ry} A {(right-left)/2} {ry} 0 0 1 {right} {top+ry} '
                f'L {right-inset} {bottom-ry} Q {width/2} {bottom+ry} {left+inset} {bottom-ry} Z')
        element(g, 'ellipse', cx=width/2, cy=top+ry, rx=(right-left)/2, ry=ry)
        left += inset+6
        right -= inset+6
        text_top = top + 2*ry + 8
    elif shape == 'infrastructure':
        element(g, 'ellipse', cx=width/2, cy=(top+bottom)/2, rx=(right-left)/2, ry=(bottom-top)/2)
        horizontal_inset=(right-left)*.15
        left+=horizontal_inset
        right-=horizontal_inset
        vertical_inset=(bottom-top)*.15
        text_top=top+vertical_inset
        bottom-=vertical_inset
    elif shape == 'queue':
        rx = 14
        element(g, 'path', d=f'M {left+rx} {top} H {right-rx} A {rx} {(bottom-top)/2} 0 0 1 {right-rx} {bottom} '
                f'H {left+rx} A {rx} {(bottom-top)/2} 0 0 1 {left+rx} {top} Z')
        element(g, 'ellipse', cx=left+rx, cy=(top+bottom)/2, rx=rx, ry=(bottom-top)/2)
        left += 2*rx
        right -= rx
    elif shape == 'directory':
        element(g, 'path', d=f'M {left} {top+20} V {top} H {left+width*.25} L {left+width*.25+14} {top+20} '
                f'H {right} V {bottom} H {left} Z')
        text_top = top + 35
    else:
        attrs = {'x':left, 'y':top, 'width':right-left, 'height':bottom-top}
        if shape in ('system','application','component','deployment-node','boundary'):
            attrs.update(rx=6)
        if shape in ('boundary','deployment-node','group-boundary'):
            attrs.update(fill='none')
        if shape == 'group-boundary':
            attrs.update(stroke_dasharray='2 5')
        element(g, 'rect', **attrs)
        if shape == 'browser':
            element(g, 'path', d=f'M {left} {top+22} H {right}', fill='none')
            for x in [left+10, left+20, left+30]:
                element(g, 'circle', cx=x, cy=top+11, r=2, fill=colours['stroke'])
            text_top = top + 34
        elif shape == 'component':
            for y in [top+15, top+37]:
                element(g, 'rect', x=left-8, y=y, width=19, height=12)
            left += 10
        elif shape == 'application':
            element(g, 'path', d=f'M {left+10} {top+8} l 8 6 l -8 6 m 14 0 h 10', fill='none')
            text_top = top + 34
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
    y = text_top + max(16, (available-len(lines)*19)/2 + 16)
    for line, bold in lines:
        element(root, 'text', x=(left+right)/2, y=y, fill=colours['text'],
                font_family='Arial, sans-serif', font_size=font, font_weight='bold' if bold else 'normal', text_anchor='middle').text = line
        y += 19
    return ET.tostring(root, encoding='unicode', xml_declaration=False)

def render_catalog(profile):
    height=math.ceil(len(SHAPES)/3)*250+60
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
    element(root, 'text', x=20, y=height-30, font_family='Arial, sans-serif', font_size=12,
            fill=THEME['profiles'][profile]['line']).text = 'Visual reference: Simon Brown · c4model.com · CC BY 4.0 · Independently drawn adaptation'
    return ET.tostring(root, encoding='unicode')

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--shape', choices=SHAPES, default='system')
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
        svg = render_catalog(args['profile']) if catalog else render_shape(**args)
    except (ValueError, KeyError) as error:
        parser.error(str(error))
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(svg, encoding='utf-8')
    print(output.resolve())

if __name__ == '__main__':
    main()
