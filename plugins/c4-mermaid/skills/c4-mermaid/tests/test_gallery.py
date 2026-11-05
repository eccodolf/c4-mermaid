import hashlib
import json
from pathlib import Path
import re
import unittest
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
GALLERY = ROOT / 'assets/examples/game-session-monitor'


class GalleryTests(unittest.TestCase):
    def test_four_real_formats_and_native_directions_agree_with_source(self):
        metadata = json.loads((GALLERY / 'metadata.json').read_text(encoding='utf-8'))
        self.assertEqual(len(metadata['diagrams']), 7)
        for diagram in metadata['diagrams']:
            with self.subTest(diagram=diagram['id']):
                self.assertEqual(set(diagram['artifacts']), {'png', 'svg', 'mermaid', 'drawio'})
                for filename, digest in diagram['sha256'].items():
                    self.assertEqual(hashlib.sha256((GALLERY / filename).read_bytes()).hexdigest(), digest)
                png = (GALLERY / diagram['artifacts']['png']).read_bytes()
                self.assertEqual(png[:8], b'\x89PNG\r\n\x1a\n')
                self.assertGreater(int.from_bytes(png[16:20], 'big'), 0)
                self.assertGreater(int.from_bytes(png[20:24], 'big'), 0)
                svg = ET.parse(GALLERY / diagram['artifacts']['svg']).getroot()
                self.assertTrue(svg.tag.endswith('}svg'))
                self.assertIn('Legend', ''.join(svg.itertext()))
                native = ET.parse(GALLERY / diagram['artifacts']['drawio']).getroot()
                self.assertEqual(native.tag, 'mxfile')
                self.assertFalse(any('image=' in cell.get('style', '') for cell in native.iter('mxCell')))
                self.assertIsNotNone(native.find(".//object[@id='meta_legend']"))
                source = (GALLERY / diagram['artifacts']['mermaid']).read_text(encoding='utf-8')
                if source.startswith('drawioC4'):
                    expected = re.findall(r'^Rel\((\w+),\s*(\w+),', source, re.M)
                    cells = [obj.find('mxCell') for obj in native.iter('object') if obj.get('c4ModelType') == 'relationship']
                elif 'classDiagram' in source:
                    expected = re.findall(r'^\s*(\w+)\s+\.\.>\s+(\w+)\s*:', source, re.M)
                    cells = [obj.find('mxCell') for obj in native.iter('object') if obj.get('notation') == 'uml-dependency']
                else:
                    expected = [('life_' + a, 'life_' + b) for a, b in re.findall(r'^\s*(\w+)(?:-->>|->>)(\w+)\s*:', source, re.M)]
                    cells = [obj.find('mxCell') for obj in native.iter('object') if obj.get('notation') == 'uml-sequence-message']
                self.assertEqual([(cell.get('source'), cell.get('target')) for cell in cells], expected)
                for cell in cells:
                    fields = dict(part.split('=', 1) for part in cell.get('style', '').split(';') if '=' in part)
                    self.assertNotIn(fields.get('endArrow', 'none'), ('none', ''))
                    self.assertEqual(fields.get('startArrow', 'none'), 'none')


if __name__ == '__main__':
    unittest.main()
