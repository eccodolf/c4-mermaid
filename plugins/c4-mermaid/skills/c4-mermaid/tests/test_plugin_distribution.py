import importlib.util
import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("verify_distribution", ROOT / "scripts/verify_bundle.py")
VERIFIER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(VERIFIER)


@unittest.skipUnless((ROOT / ".agents/plugins/marketplace.json").is_file(), "Repository marketplace is outside the standalone skill bundle")
class PluginDistributionTests(unittest.TestCase):
    def test_marketplace_uses_in_repository_plugin(self):
        marketplace = json.loads((ROOT / ".agents/plugins/marketplace.json").read_text(encoding="utf-8"))
        self.assertEqual(marketplace["name"], "eccodolf-c4-mermaid")
        self.assertEqual(len(marketplace["plugins"]), 1)
        source = marketplace["plugins"][0]["source"]
        self.assertEqual(source, {"source": "local", "path": "./plugins/c4-mermaid"})
        self.assertTrue((ROOT / source["path"] / "plugin.json").is_file())

    def test_portable_and_compatibility_manifests_agree(self):
        plugin = ROOT / "plugins/c4-mermaid"
        portable = json.loads((plugin / "plugin.json").read_text(encoding="utf-8"))
        compatibility = json.loads((plugin / ".codex-plugin/plugin.json").read_text(encoding="utf-8"))
        for key in ("name", "version", "description", "author"):
            self.assertEqual(portable[key], compatibility[key])
        self.assertEqual(compatibility["skills"], "./skills/")
        self.assertNotIn("apps", portable["extensions"]["com.openai"])
        self.assertNotIn("hooks", portable["extensions"]["com.openai"])

    def test_claude_marketplace_and_manifest(self):
        marketplace = json.loads((ROOT / ".claude-plugin/marketplace.json").read_text(encoding="utf-8"))
        self.assertEqual(marketplace["name"], "eccodolf-c4-mermaid")
        self.assertEqual(marketplace["owner"]["name"], "eccodolf")
        self.assertEqual(marketplace["plugins"][0]["source"], "./plugins/c4-mermaid")
        plugin = ROOT / marketplace["plugins"][0]["source"]
        claude = json.loads((plugin / ".claude-plugin/plugin.json").read_text(encoding="utf-8"))
        portable = json.loads((plugin / "plugin.json").read_text(encoding="utf-8"))
        for key in ("name", "version", "description", "author"):
            self.assertEqual(claude[key], portable[key])
        self.assertTrue((plugin / "skills/c4-mermaid/SKILL.md").is_file())
        self.assertNotIn("hooks", claude)
        self.assertNotIn("mcpServers", claude)

    def test_packaged_skill_is_complete_and_matches_source(self):
        packaged = ROOT / "plugins/c4-mermaid/skills/c4-mermaid"
        self.assertEqual(VERIFIER.verify(packaged), [])
        self.assertEqual(VERIFIER.bundle_files(packaged), VERIFIER.bundle_files(ROOT))
        self.assertEqual((packaged / VERIFIER.MANIFEST).read_bytes(), (ROOT / VERIFIER.MANIFEST).read_bytes())


if __name__ == "__main__":
    unittest.main()
