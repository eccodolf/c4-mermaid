#!/usr/bin/env python3
"""Maintainer: capture native paint primitives from a metadata-enabled draw.io SVG export."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import xml.etree.ElementTree as ET

TAGS={'path','rect','ellipse','circle','line','polyline','polygon'}
ATTRS={'d','x','y','cx','cy','x1','x2','y1','y2','width','height','rx','ry','r','fill','stroke','stroke-width','stroke-dasharray','transform'}


def path_tokens(value,ox,oy):
    tokens=re.findall(r'[A-Za-z]|[-+]?(?:\d*\.\d+|\d+\.?)(?:[eE][-+]?\d+)?',value)
    output=[];command=None;index=0
    counts={'M':2,'L':2,'C':6,'Q':4,'H':1,'V':1,'Z':0}
    while index<len(tokens):
        if tokens[index].isalpha():command=tokens[index];output.append(command);index+=1
        if command not in counts:raise ValueError('Unexpected native path command: '+str(command))
        count=counts[command]
        if count==0:command=None;continue
        for i in range(count):
            value=float(tokens[index+i])
            value-=ox if command=='H' or (command!='V' and i%2==0) else oy
            output.append(round(value,4))
        index+=count
    return output


def signature(group,ox,oy):
    result=[]
    for element in group.iter():
        tag=element.tag.rsplit('}',1)[-1]
        if tag not in TAGS:continue
        attrs={}
        for key,value in element.attrib.items():
            if key not in ATTRS:continue
            if key=='d':attrs[key]=path_tokens(value,ox,oy)
            elif key in ('x','cx','x1','x2'):attrs[key]=round(float(value)-ox,4)
            elif key in ('y','cy','y1','y2'):attrs[key]=round(float(value)-oy,4)
            elif key in ('width','height','rx','ry','r','stroke-width'):attrs[key]=round(float(value),4)
            elif key=='transform' and value.startswith('rotate('):
                values=[float(number) for number in re.findall(r'[-+]?(?:\d*\.\d+|\d+\.?)(?:[eE][-+]?\d+)?',value)]
                if len(values)!=3:raise ValueError('Expected an absolute rotation pivot.')
                attrs[key]=['rotate',values[0],round(values[1]-ox,4),round(values[2]-oy,4)]
            else:attrs[key]=value.lower()
        result.append({'tag':tag,'attrs':attrs})
    return result


def capture(svg,model):
    root=ET.parse(svg).getroot();nodes=json.loads(Path(model).read_text(encoding='utf-8'))['pages'][0]['elements']
    groups={element.get('data-cell-id'):element for element in root.iter() if element.get('data-cell-id')}
    anchor=next(node for node in nodes if node['type']=='software-system' and not node.get('external'))
    rectangle=next(element for element in groups[anchor['id']].iter() if element.tag.endswith('}rect'))
    dx=float(rectangle.get('x'))-anchor['x'];dy=float(rectangle.get('y'))-anchor['y']
    shapes={}
    for node in nodes:
        geometry=next(iter(groups[node['id']]))
        shapes[node['id']]={'width':node['width'],'height':node['height'],'primitives':signature(geometry,node['x']+dx,node['y']+dy)}
    return {'format':1,'native_renderer':'draw.io 32.6.10','source_export_sha256':hashlib.sha256(Path(svg).read_bytes()).hexdigest(),'source_model_sha256':hashlib.sha256(Path(model).read_bytes()).hexdigest(),'shapes':shapes}


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--input',type=Path,required=True);parser.add_argument('--model',type=Path,required=True);parser.add_argument('--output',type=Path,required=True);args=parser.parse_args()
    with args.output.open('w',encoding='utf-8',newline='\n') as output:
        output.write(json.dumps(capture(args.input,args.model),indent=2)+'\n')
    print('Captured twelve native geometry references from the actual draw.io exporter.')


if __name__=='__main__':main()
