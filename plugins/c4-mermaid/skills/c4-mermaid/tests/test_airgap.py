import importlib.util
from pathlib import Path
import socket
import tempfile
import unittest
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]


def load_script(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / "scripts" / (name + ".py"))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


VERIFIER = load_script("verify_bundle")
INSTALLER = load_script("install_skill")


class AirGapTests(unittest.TestCase):
    def test_verification_and_installation_without_network(self):
        with tempfile.TemporaryDirectory() as scratch:
            with patch.object(socket, "socket", side_effect=AssertionError("Network forbidden")) as connect:
                with patch.object(socket, "create_connection", side_effect=AssertionError("Network forbidden")) as create:
                    self.assertEqual(VERIFIER.verify(ROOT), [])
                    installed = INSTALLER.install(ROOT, Path(scratch) / "c4-mermaid")
                    self.assertEqual(VERIFIER.verify(installed), [])
                    connect.assert_not_called()
                    create.assert_not_called()

    def test_tampered_and_missing_resources_are_detected(self):
        with tempfile.TemporaryDirectory() as scratch:
            installed = INSTALLER.install(ROOT, Path(scratch) / "c4-mermaid")
            (installed / "references/c4-model.md").write_text("Altered model", encoding="utf-8")
            (installed / "assets/offline/mermaid.min.js").unlink()
            errors = VERIFIER.verify(installed)
            self.assertTrue(any("references/c4-model.md" in error for error in errors))
            self.assertTrue(any("mermaid.min.js" in error for error in errors))
            with self.assertRaises(ValueError):
                INSTALLER.install(installed, Path(scratch) / "second-install")

    def test_new_remote_links_and_broken_local_links_are_rejected(self):
        with tempfile.TemporaryDirectory() as scratch:
            installed = INSTALLER.install(ROOT, Path(scratch) / "c4-mermaid")
            guide = installed / "references/airgap.md"
            with guide.open("a", encoding="utf-8") as output:
                output.write("\n[Remote](https://invalid.example/resource)\n[Missing](absent-guide.md)\n")
            VERIFIER.write_manifest(installed)
            errors = VERIFIER.verify(installed)
            self.assertTrue(any("Non-local reference" in error for error in errors))
            self.assertTrue(any("Missing local reference" in error for error in errors))

    def test_svg_remote_resources_are_rejected(self):
        with tempfile.TemporaryDirectory() as scratch:
            installed = INSTALLER.install(ROOT, Path(scratch) / "c4-mermaid")
            svg = installed / "assets/graphics/person.svg"
            svg.write_text('<svg xmlns="http://www.w3.org/2000/svg"><image href="remote-image.svg"/></svg>', encoding="utf-8")
            VERIFIER.write_manifest(installed)
            self.assertTrue(any("External SVG resource" in error for error in VERIFIER.verify(installed)))


if __name__ == "__main__":
    unittest.main()
