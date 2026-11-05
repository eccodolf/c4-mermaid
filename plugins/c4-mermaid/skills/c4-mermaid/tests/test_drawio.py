import copy
import json
from pathlib import Path
import sys
import tempfile
import unittest
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import export_drawio as drawio
from shape_policy import contrast_ratio, shape_for
from drawio_assets import default_profile, style_for


class DrawioTests(unittest.TestCase):
    def setUp(self):
        self.model = json.loads((ROOT / "assets/drawio/container.json").read_text(encoding="utf-8"))

    def check_xml(self, document):
        with tempfile.TemporaryDirectory() as directory:
            file = Path(directory) / "test.drawio"
            file.write_text(ET.tostring(document, encoding="unicode"), encoding="utf-8")
            return drawio.check_file(file)

    def test_native_cells_and_real_containment(self):
        document = ET.fromstring(drawio.export_model(self.model))
        self.assertEqual(self.check_xml(document), {"pages": 1, "elements": 8, "relationships": 6})
        objects = {obj.get("id"): obj for obj in document.findall(".//object")}
        self.assertEqual(objects["db"].find("mxCell").get("parent"), "orders_scope")
        self.assertEqual(objects["api_db"].find("mxCell").get("parent"), "orders_scope")
        self.assertEqual(objects["api_payments"].find("mxCell").get("parent"), "1")
        self.assertEqual(objects["api_topic"].find(".//Array/mxPoint").get("x"), "690")
        for identifier, shape in (("web","mxgraph.c4.webBrowserContainer2"), ("db","cylinder3"), ("bucket","cylinder3"), ("topic","cylinder3")):
            self.assertIn("shape="+shape+";", objects[identifier].find("mxCell").get("style"))
        self.assertIn("entryX=0.5;entryY=1;", objects["api_topic"].find("mxCell").get("style"))
        frame = objects['orders_scope']
        fields = dict(part.split('=',1) for part in frame.find('mxCell').get('style').split(';') if '=' in part)
        self.assertEqual((fields['rounded'],fields['dashed'],fields['dashPattern'],fields['verticalAlign']), ('1','1','8 4','bottom'))
        self.assertEqual(frame.get('c4Type'), 'SystemScopeBoundary')
        self.assertEqual(frame.get('c4Application'), 'Software System')

    def test_all_catalog_types_and_compressed_page_round_trip(self):
        model = json.loads((ROOT / "assets/drawio/shapes.json").read_text(encoding="utf-8"))
        model["pages"][0]["elements"][1]["name"] = 'A & B <demo>'
        document = ET.fromstring(drawio.export_model(model))
        diagram = document.find("diagram")
        graph = diagram.find("mxGraphModel")
        diagram.remove(graph)
        diagram.text = drawio.encode_xml(ET.tostring(graph, encoding="unicode"))
        self.assertEqual(self.check_xml(document)["elements"], 12)
        self.assertEqual(len(set(shape_for(node["type"], node.get("subtype")) for node in model["pages"][0]["elements"])), 9)

    def test_native_tampering_is_rejected(self):
        for change in ("visible-kind", "geometry", "image", "contrast", "endpoint", "external", "parent"):
            document = ET.fromstring(drawio.export_model(self.model))
            objects = {obj.get("id"): obj for obj in document.findall(".//object")}
            node = objects["db"]
            if change == "visible-kind":
                node.set("label", node.get("label").replace("Container", "Person"))
            elif change == "geometry":
                cell = node.find("mxCell")
                cell.set("style", cell.get("style").replace("shape=cylinder3;", "shape=hexagon;"))
            elif change == "image":
                node.find("mxCell").set("style", "shape=image;image=data:fake")
            elif change == "contrast":
                cell = objects["orders_scope"].find("mxCell")
                cell.set("style", cell.get("style") + "fontColor=#FFFFFF;")
            elif change == "endpoint":
                objects["api_db"].find("mxCell").set("target", "orders_scope")
            elif change == "parent":
                node.find("mxCell").set("parent", "customer")
            else:
                document.find(".//root").remove(objects["payments"])
            with self.subTest(change=change), self.assertRaises(ValueError):
                self.check_xml(document)

    def test_layout_and_scope_failures_are_rejected(self):
        for change in ("overlap", "clipping", "text", "type", "external", "label", "route", "frame-endpoint"):
            model = copy.deepcopy(self.model)
            page = model["pages"][0]
            nodes = {node["id"]: node for node in page["elements"]}
            if change == "overlap":
                nodes["db"]["y"] = 90
            elif change == "clipping":
                nodes["db"]["x"] = 900
            elif change == "text":
                nodes["api"]["description"] = "Very long responsibility " * 100
            elif change == "type":
                nodes["db"]["shape"] = "person"
            elif change == "external":
                page["expected_external_systems"].append("identity")
            elif change == "label":
                page["relationships"][3]["label_offset"] = [0, 0]
            elif change == "route":
                page["relationships"][0]["points"] = [[800, 250]]
            else:
                page["relationships"][0]["target"] = "orders_scope"
            with self.subTest(change=change), self.assertRaises(ValueError):
                drawio.export_model(model)

    def test_default_theme_and_readable_adaptations(self):
        source = style_for("Person")
        profile = default_profile()["roles"]
        self.assertEqual(profile["person"]["fill"].lower(), source["fillColor"].lower())
        for kind in ("person", "system", "container", "component", "external"):
            with self.subTest(kind=kind):
                self.assertGreaterEqual(contrast_ratio(profile[kind]["text"], profile[kind]["fill"]), 4.5)

    def test_every_page_requires_a_saved_visible_legend(self):
        for value in (None, "", " \n\t"):
            model = copy.deepcopy(self.model)
            model["pages"][0]["legend"] = value
            with self.subTest(value=value), self.assertRaises(ValueError):
                drawio.export_model(model)
        for change in ("remove", "hide", "zero-size", "contrast", "style", "row"):
            document = ET.fromstring(drawio.export_model(self.model))
            root = document.find(".//root")
            legend = root.find("object[@id='meta_legend']")
            if change == "remove":
                root.remove(legend)
            elif change == "hide":
                legend.find("mxCell").set("visible", "0")
            elif change == "zero-size":
                legend.find(".//mxGeometry").set("height", "0")
            elif change == "row":
                root.remove(root.find("mxCell[@c4LegendRole]"))
            else:
                cell = legend.find("mxCell")
                cell.set("style", cell.get("style") + ("fontColor=#FFFFFF;" if change == "contrast" else "noLabel=1;"))
            with self.subTest(change=change), self.assertRaises(ValueError):
                self.check_xml(document)


if __name__ == "__main__":
    unittest.main()
