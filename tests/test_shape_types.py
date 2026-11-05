import sys
from pathlib import Path
import unittest
import xml.etree.ElementTree as ET

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import render_shape


class ShapeTypeTests(unittest.TestCase):
    def test_incompatible_type_cannot_be_hidden_in_shape_label(self):
        for shape, kind in (("database", "Person"), ("person", "Container"), ("component", "Software System"), ("queue", "Component")):
            with self.subTest(shape=shape, kind=kind), self.assertRaises(ValueError):
                render_shape.render_shape(shape, kind=kind)

    def test_person_head_remains_circular_at_different_aspect_ratios(self):
        for width, height in ((320, 240), (500, 220), (300, 480)):
            with self.subTest(width=width, height=height):
                root = ET.fromstring(render_shape.render_shape("person", width=width, height=height))
                circles = root.findall(".//{" + render_shape.SVG + "}circle")
                self.assertEqual(len(circles), 1)
                self.assertGreater(float(circles[0].get("r")), 0)


if __name__ == "__main__":
    unittest.main()
