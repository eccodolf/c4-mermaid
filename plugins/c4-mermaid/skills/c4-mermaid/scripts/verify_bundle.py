#!/usr/bin/env python3
"""Verify a transferred skill bundle using local files and the standard library."""

import argparse
import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import xml.etree.ElementTree as ET


BUNDLE_ENTRIES = ("SKILL.md", "README.md", ".gitattributes", "agents", "references", "assets", "scripts", "tests")
MANIFEST = "bundle-manifest.json"
NAMESPACES = ("http://www.w3.org/2000/svg", "http://www.w3.org/1999/xlink", "http://www.w3.org/XML/1998/namespace", "http://www.w3.org/1999/xhtml")
REMOTE = re.compile(r"(?:https?|wss?|ftp)://|(?<!:)//[A-Za-z]", re.I)


def bundle_files(root):
    files = {}
    for name in BUNDLE_ENTRIES:
        entry = root / name
        if not entry.exists():
            raise ValueError(f"Missing bundle entry: {name}")
        for file in entry.rglob("*") if entry.is_dir() else [entry]:
            if not file.is_file() or "__pycache__" in file.parts or file.suffix in (".pyc", ".pyo"):
                continue
            if file.is_symlink() or root not in file.resolve().parents:
                raise ValueError(f"Resource escapes the bundle: {file}")
            files[file.relative_to(root).as_posix()] = hashlib.sha256(file.read_bytes()).hexdigest()
    return dict(sorted(files.items()))


def write_manifest(root):
    root = Path(root).resolve()
    manifest = {"format": 1, "mermaid_version": "12.3.0", "files": bundle_files(root)}
    with (root / MANIFEST).open("w", encoding="utf-8", newline="\n") as output:
        output.write(json.dumps(manifest, indent=2) + "\n")


def local_target(root, origin, value, errors):
    if not value or value.startswith("#"):
        return
    target = value.split("#", 1)[0]
    if re.match(r"[a-z][a-z0-9+.-]*:|//", target, re.I):
        errors.append(f"Non-local reference in {origin.relative_to(root)}: {value}")
        return
    resolved = (origin.parent / target).resolve()
    if resolved != root and root not in resolved.parents:
        errors.append(f"Reference escapes bundle in {origin.relative_to(root)}: {value}")
    elif not resolved.exists():
        errors.append(f"Missing local reference in {origin.relative_to(root)}: {value}")


class ViewerReferences(HTMLParser):
    def __init__(self):
        super().__init__()
        self.resources = []
        self.policy = ""

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "meta" and attrs.get("http-equiv", "").lower() == "content-security-policy":
            self.policy = attrs.get("content", "")
        for name in ("src", "href"):
            if name in attrs:
                self.resources.append(attrs[name])


def verify(root):
    root = Path(root).resolve()
    errors = []
    actual = bundle_files(root)
    manifest = json.loads((root / MANIFEST).read_text(encoding="utf-8"))
    if manifest.get("format") != 1 or manifest.get("mermaid_version") != "12.3.0":
        errors.append("Unsupported manifest format or Mermaid version.")
    expected = manifest.get("files", {})
    for name in sorted(set(actual) | set(expected)):
        if actual.get(name) != expected.get(name):
            errors.append(f"Integrity mismatch: {name}")
    for name in actual:
        file = root / name
        if file.suffix == ".md":
            text = file.read_text(encoding="utf-8")
            if REMOTE.search(text):
                errors.append(f"External URL in authored instructions: {name}")
            for target in re.findall(r"\[[^\]\n]*\]\(([^)\n]+)\)", text):
                local_target(root, file, target, errors)
        if file.suffix == ".svg":
            try:
                document = ET.parse(file)
            except ET.ParseError as error:
                errors.append(f"Invalid SVG in {name}: {error}")
                continue
            for element in document.iter():
                for key, value in element.attrib.items():
                    if key.rsplit("}", 1)[-1] in ("href", "src") and not value.startswith("#"):
                        errors.append(f"External SVG resource in {name}: {value}")
            text = file.read_text(encoding="utf-8")
            for namespace in NAMESPACES:
                text = text.replace(namespace, "")
            if REMOTE.search(text):
                errors.append(f"Remote identifier outside SVG namespaces: {name}")
    viewer = root / "assets/offline/viewer.html"
    text = viewer.read_text(encoding="utf-8")
    parser = ViewerReferences()
    parser.feed(text)
    for target in parser.resources:
        local_target(root, viewer, target, errors)
    for directive in ("default-src 'none'", "connect-src 'none'", "font-src 'none'", "frame-src 'none'", "worker-src 'none'", "object-src 'none'"):
        if directive not in parser.policy:
            errors.append(f"Missing viewer restriction: {directive}")
    if "assertAirGapSource(requestedSource)" not in text:
        errors.append("Viewer does not check source before rendering.")
    theme = root / "assets/c4-theme.json"
    local_target(root, theme, json.loads(theme.read_text(encoding="utf-8"))["reference"], errors)
    for name in ("mermaid.min.js", "airgap-guard.js", "LICENSE.mermaid", "LICENSE.CC-BY-4.0"):
        if not (root / "assets/offline" / name).is_file():
            errors.append(f"Missing offline resource: {name}")
    templates = root / "assets/templates"
    if len(list(templates.glob("*.mmd"))) != 9:
        errors.append("Expected nine bundled Mermaid examples.")
    for source in templates.glob("*.mmd"):
        if not source.with_suffix(".svg").is_file():
            errors.append(f"Missing SVG preview: {source.name}")
    for name in ("library.json", "mxC4.js", "Sidebar-C4.js", "Shapes.js", "provenance.json", "LICENSE.drawio", "NOTICE.txt"):
        if not (root / "assets/drawio-c4" / name).is_file():
            errors.append(f"Missing draw.io C4 resource: {name}")
    for name in ("container", "shapes"):
        directory = root / "assets/drawio"
        for suffix in (".json", ".drawio", ".svg"):
            if not (directory / (name + suffix)).is_file():
                errors.append(f"Missing draw.io fixture: {name}{suffix}")
        native = directory / (name + ".drawio")
        if native.is_file():
            try:
                document = ET.parse(native).getroot()
                if document.tag != "mxfile" or not document.findall("./diagram/mxGraphModel/root/object"):
                    errors.append(f"Not an uncompressed native editable fixture: {name}")
                for cell in document.iter("mxCell"):
                    style = cell.get("style", "")
                    readable_style = re.sub(r"stencil\([A-Za-z0-9+/=]+\)", "stencil(embedded)", style)
                    if "image=" in style or REMOTE.search(readable_style):
                        errors.append(f"Image or remote dependency in draw.io fixture: {name}")
            except ET.ParseError as error:
                errors.append(f"Invalid draw.io fixture {name}: {error}")
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parent.parent)
    parser.add_argument("--write-manifest", action="store_true", help="Maintainer only: record an intentionally reviewed bundle update.")
    args = parser.parse_args()
    try:
        if args.write_manifest:
            write_manifest(args.root)
        errors = verify(args.root)
    except (OSError, ValueError, ET.ParseError, KeyError) as error:
        parser.exit(1, f"Bundle verification failed: {error}\n")
    if errors:
        parser.exit(1, "Bundle verification failed:\n" + "\n".join(errors) + "\n")
    print("Bundle verified: hashes, local links, SVG resources, viewer restrictions, and nine examples.")


if __name__ == "__main__":
    main()
