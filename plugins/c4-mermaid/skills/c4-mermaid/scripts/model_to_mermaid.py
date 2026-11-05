#!/usr/bin/env python3
"""Create editable C4Drawio Mermaid source using the exact offline renderer."""
import argparse
import html
import json
from pathlib import Path
from export_drawio import validate_page


def quoted(value):
    # C4's lexer does not reliably preserve backslash-escaped quotation marks.
    text=html.escape(str(value),quote=False).replace('"','&quot;').replace('\\','&bsol;').replace('\n','<br/>')
    return json.dumps(text, ensure_ascii=False)


def to_mermaid(model, page_index=0):
    page = model['pages'][page_index]
    validate_page(page)
    view = page['view']
    kind = {'context':'C4Context','landscape':'C4Context','container':'C4Container','component':'C4Component','dynamic':'C4Dynamic','deployment':'C4Deployment','shape-catalog':'C4Container'}[view]
    elements = page['elements']
    nodes = {node['id']:node for node in elements}
    layout = {'view':view,'nodes':{},'edges':[],'expected_external_systems':page.get('expected_external_systems',[])}
    for node in elements:
        layout['nodes'][node['id']] = {key:node[key] for key in ('x','y','width','height','parent','subtype') if key in node}
    for edge in page.get('relationships',[]):
        layout['edges'].append({key:edge[key] for key in ('id','source','target','source_port','target_port','points','label_offset','dashed') if key in edge})
    lines = ['drawioC4 '+{'C4Context':'context','C4Container':'container','C4Component':'component','C4Dynamic':'dynamic','C4Deployment':'deployment'}[kind],'title '+page['title']]
    def write_node(node, depth=0):
        prefix='  '*depth; identifier=node['id']; name=quoted(node['name']); technology=quoted(node.get('technology','')); description=quoted(node.get('description',''))
        element_type=node['type']
        if element_type in ('system-boundary','container-boundary','group','deployment-node'):
            macro={'system-boundary':'System_Boundary','container-boundary':'Container_Boundary','group':'Enterprise_Boundary','deployment-node':'Deployment_Node'}[element_type]
            extra=', '+technology+', '+description if element_type=='deployment-node' else ''
            lines.append(f'{prefix}{macro}({identifier}, {name}{extra}) {{')
            if not any(child.get('parent')==identifier for child in elements):
                # The native Mermaid grammar needs a statement inside a sample scope.
                lines.append(prefix+'  UpdateLayoutConfig($c4ShapeInRow="3")')
            for child in elements:
                if child.get('parent')==identifier:write_node(child,depth+1)
            lines.append(prefix+'}')
        else:
            if element_type=='person':macro='Person_Ext' if node.get('external') else 'Person'; args=f'{identifier}, {name}, {description}'
            elif element_type=='software-system':macro='System_Ext' if node.get('external') else 'System'; args=f'{identifier}, {name}, {description}'
            elif element_type=='container':macro='ContainerDb' if node['subtype'] in ('database','bucket','directory') else 'ContainerQueue' if node['subtype']=='queue' else 'Container'; args=f'{identifier}, {name}, {technology}, {description}'
            elif element_type=='component':macro='Component';args=f'{identifier}, {name}, {technology}, {description}'
            else:raise ValueError('Use a supported C4 element type: '+element_type)
            lines.append(f'{prefix}{macro}({args})')
    for node in elements:
        if not node.get('parent'):write_node(node)
    for edge in page.get('relationships',[]):
        lines.append(f'Rel({edge["source"]}, {edge["target"]}, {quoted(edge["action"])}, {quoted(edge.get("technology",""))})')
    lines.append('%% drawio-layout: '+json.dumps(layout,ensure_ascii=False,separators=(',',':')))
    lines.extend('%% legend: '+line for line in page['legend'].splitlines())
    return '\n'.join(lines)+'\n'


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input',type=Path,required=True)
    parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--page',type=int,default=0)
    args=parser.parse_args()
    try:
        source=to_mermaid(json.loads(args.input.read_text(encoding='utf-8')),args.page)
        args.output.parent.mkdir(parents=True,exist_ok=True)
        with args.output.open('w',encoding='utf-8',newline='\n') as output:
            output.write(source)
    except (ValueError,KeyError,IndexError,OSError) as error:parser.exit(1,str(error)+'\n')
    print(args.output)


if __name__=='__main__':main()
