import hashlib
import json
from pathlib import Path
import sys
import unittest
import xml.etree.ElementTree as ET

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from model_to_mermaid import to_mermaid
from capture_fidelity import signature


class ExactMermaidTests(unittest.TestCase):
    def test_source_remains_editable_without_duplicating_names_in_layout(self):
        model=json.loads((ROOT/'assets/drawio/shapes.json').read_text(encoding='utf-8'))
        model['pages'][0]['elements'][2]['name']='A&B "Q" <svc> \\ P'
        source=to_mermaid(model)
        self.assertTrue(source.startswith('drawioC4 container\n'))
        self.assertIn('A&amp;B &quot;Q&quot; &lt;svc&gt; &bsol; P',source)
        layout=json.loads(next(line.split(':',1)[1] for line in source.splitlines() if line.startswith('%% drawio-layout:')))
        for geometry in layout['nodes'].values():
            self.assertLessEqual(set(geometry),{'x','y','width','height','parent','subtype'})

    def test_exact_mermaid_vectors_match_actual_drawio_export(self):
        model=json.loads((ROOT/'assets/drawio/shapes.json').read_text(encoding='utf-8'))
        nodes={node['id']:node for node in model['pages'][0]['elements']}
        reference=json.loads((ROOT/'assets/drawio-c4/native-fidelity.json').read_text(encoding='utf-8'))
        document=ET.parse(ROOT/'assets/drawio/shapes-mermaid.svg').getroot()
        self.assertEqual(document.get('data-c4-native-renderer'),'drawio-32.6.10')
        groups={element.get('data-c4-id'):element for element in document.iter() if element.get('data-c4-id')}
        self.assertEqual(set(groups),set(reference['shapes']))
        for identifier,group in groups.items():
            with self.subTest(identifier=identifier):
                geometry=next(child for child in group if child.get('data-c4-shape'))
                self.assertEqual(signature(geometry,nodes[identifier]['x'],nodes[identifier]['y']),reference['shapes'][identifier]['primitives'])
        self.assertFalse(any(element.tag.rsplit('}',1)[-1] in ('image','foreignObject') for element in document.iter()))

    def test_runtime_is_pinned_to_the_unchanged_native_sources(self):
        provenance=json.loads((ROOT/'assets/drawio-c4/provenance.json').read_text(encoding='utf-8'))
        runtime=provenance['mermaid_native_runtime']
        self.assertEqual(runtime['drawio_version'],'32.6.10')
        for name,digest in runtime['files'].items():
            self.assertEqual(hashlib.sha256((ROOT/'assets/drawio-c4'/name).read_bytes()).hexdigest(),digest,name)
        source=(ROOT/'assets/drawio-c4/Shapes.js').read_text(encoding='utf-8')
        extracted=(ROOT/'assets/drawio-c4/native-builtins.js').read_text(encoding='utf-8')
        for start,end in [('function CylinderShape3(',"mxCellRenderer.registerShape('cylinder3', CylinderShape3);"),('function HexagonShape()',"mxCellRenderer.registerShape('hexagon', HexagonShape);")]:
            a=source.index(start);b=source.index(end,a)+len(end)
            self.assertIn(source[a:b],extracted)

    def test_native_reference_is_bound_to_the_reviewed_model(self):
        reference=json.loads((ROOT/'assets/drawio-c4/native-fidelity.json').read_text(encoding='utf-8'))
        self.assertEqual(reference['source_model_sha256'],hashlib.sha256((ROOT/'assets/drawio/shapes.json').read_bytes()).hexdigest())
        self.assertEqual(len(reference['shapes']),12)


if __name__=='__main__':unittest.main()
