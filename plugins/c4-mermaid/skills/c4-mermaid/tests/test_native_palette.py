import hashlib
import json
from pathlib import Path
import sys
import unittest
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'scripts'))
from drawio_assets import TEMPLATES, style_for
import export_drawio


class NativePaletteTests(unittest.TestCase):
    def test_runtime_templates_are_the_supplied_assets(self):
        source = ROOT/'assets/drawio-c4/reference-palette.drawio'
        self.assertEqual(hashlib.sha256(source.read_bytes()).hexdigest(), TEMPLATES['source_sha256'])
        objects = ET.parse(source).findall('.//object')
        self.assertEqual(len(objects), len(TEMPLATES['entries']))
        for obj, entry in zip(objects, TEMPLATES['entries']):
            self.assertEqual(style_for(entry['name']), dict(part.split('=',1) for part in obj.find('mxCell').get('style').split(';') if '=' in part))

    def test_importable_library_contains_independent_native_graphs(self):
        library = ET.parse(ROOT/'assets/drawio-c4/native-c4.mxlibrary').getroot()
        self.assertEqual(library.tag, 'mxlibrary')
        entries = json.loads(library.text)
        self.assertEqual(len(entries), 18)
        for entry in entries:
            graph = ET.fromstring(entry['xml'])
            ids = [element.get('id') for element in graph.iter() if element.get('id')]
            self.assertEqual(len(ids), len(set(ids)))
            self.assertEqual(graph.tag, 'mxGraphModel')
            for cell in graph.iter('mxCell'):
                self.assertNotIn('image=', cell.get('style',''))
                if cell.get('parent'):
                    self.assertIn(cell.get('parent'), ids)

    def test_canonical_assets_are_not_an_optional_export_profile(self):
        model = json.loads((ROOT/'assets/drawio/container.json').read_text(encoding='utf-8'))
        model['profile'] = 'example-light'
        with self.assertRaises(ValueError):
            export_drawio.export_model(model)


if __name__ == '__main__':
    unittest.main()
