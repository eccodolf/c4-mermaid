import hashlib
import importlib.util
from pathlib import Path
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("install_skill", ROOT / "scripts/install_skill.py")
INSTALLER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(INSTALLER)


class InstallationTests(unittest.TestCase):
    def test_native_user_and_project_installations_preserve_resources(self):
        expected_roots = {
            "codex": ".agents/skills", "claude": ".claude/skills",
            "kimi": ".kimi/skills", "deepseek": ".dsh/skills",
        }
        with tempfile.TemporaryDirectory() as scratch:
            home = Path(scratch) / "home"
            project = Path(scratch) / "application"
            for target, relative_root in expected_roots.items():
                for scope, base in (("user", home), ("project", project)):
                    with self.subTest(target=target, scope=scope):
                        destination = INSTALLER.destination_for(target, scope, project, home)
                        self.assertEqual(destination, base / relative_root / "c4-mermaid")
                        INSTALLER.install(ROOT, destination)
                        for name in INSTALLER.ENTRIES:
                            source = ROOT / name
                            files = source.rglob("*") if source.is_dir() else [source]
                            for file in files:
                                if not file.is_file() or "__pycache__" in file.parts:
                                    continue
                                copied = destination / file.relative_to(ROOT)
                                self.assertEqual(
                                    hashlib.sha256(file.read_bytes()).digest(),
                                    hashlib.sha256(copied.read_bytes()).digest(),
                                )
                        self.assertFalse((destination / ".git").exists())
                        self.assertTrue((destination / "tests/test_install_skill.py").is_file())

    def test_existing_installation_is_preserved(self):
        with tempfile.TemporaryDirectory() as scratch:
            destination = Path(scratch) / "c4-mermaid"
            destination.mkdir()
            sentinel = destination / "SKILL.md"
            sentinel.write_text("Existing custom skill", encoding="utf-8")
            with self.assertRaises(FileExistsError):
                INSTALLER.install(ROOT, destination)
            self.assertEqual(sentinel.read_text(encoding="utf-8"), "Existing custom skill")

    def test_custom_destination_and_recursion_guard(self):
        with tempfile.TemporaryDirectory() as scratch:
            destination = Path(scratch) / "custom skills" / "c4-mermaid"
            INSTALLER.install(ROOT, destination)
            self.assertTrue((destination / "references/harnesses.md").is_file())
        for destination in (ROOT, ROOT / "assets/nested-install"):
            with self.subTest(destination=destination), self.assertRaises((ValueError, FileExistsError)):
                INSTALLER.install(ROOT, destination)


if __name__ == "__main__":
    unittest.main()
