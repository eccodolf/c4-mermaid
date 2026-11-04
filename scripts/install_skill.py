#!/usr/bin/env python3
"""Copy this portable skill to a native harness discovery directory."""

import argparse
import importlib.util
from pathlib import Path
import shutil


ROOTS = {
    "codex": ".agents/skills",
    "claude": ".claude/skills",
    "kimi": ".kimi/skills",
    "deepseek": ".dsh/skills",
}
ENTRIES = ("SKILL.md", "README.md", ".gitattributes", "bundle-manifest.json", "agents", "references", "assets", "scripts", "tests")


def destination_for(target, scope, project_root, home=None):
    base = Path(home) if home is not None else Path.home()
    if scope == "project":
        base = Path(project_root)
    return base / ROOTS[target] / "c4-mermaid"


def install(source, destination):
    source = Path(source).resolve()
    destination = Path(destination).expanduser().resolve()
    if not (source / "SKILL.md").is_file():
        raise ValueError("Source does not contain SKILL.md.")
    if destination.exists():
        raise FileExistsError(f"Installation already exists: {destination}")
    if destination == source or destination in source.parents:
        raise ValueError("Destination must not contain the source bundle.")
    for name in ENTRIES:
        entry = source / name
        if destination == entry or entry in destination.parents:
            raise ValueError("Destination must not be inside a copied resource.")
    for name in ENTRIES:
        if not (source / name).exists():
            raise ValueError(f"Incomplete skill bundle: missing {name}")
    spec = importlib.util.spec_from_file_location("c4_bundle_verifier", source / "scripts/verify_bundle.py")
    verifier = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(verifier)
    errors = verifier.verify(source)
    if errors:
        raise ValueError("Bundle verification failed: " + "; ".join(errors))
    destination.mkdir(parents=True)
    for name in ENTRIES:
        entry = source / name
        if entry.is_dir():
            shutil.copytree(
                entry, destination / name,
                ignore=shutil.ignore_patterns("__pycache__", "*.pyc", "*.pyo"),
            )
        else:
            shutil.copy2(entry, destination / name)
    return destination


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target", required=True, choices=ROOTS)
    parser.add_argument("--scope", choices=("user", "project"), default="user")
    parser.add_argument("--project-root", type=Path, default=Path.cwd())
    parser.add_argument("--dest", type=Path, help="Exact destination skill directory; overrides scope.")
    args = parser.parse_args()
    destination = args.dest or destination_for(args.target, args.scope, args.project_root)
    try:
        installed = install(Path(__file__).resolve().parent.parent, destination)
    except (OSError, ValueError) as error:
        parser.exit(1, f"Installation failed: {error}\n")
    print(f"Installed c4-mermaid for {args.target}: {installed}")
    print("Start a new harness session if the skill is not yet visible.")


if __name__ == "__main__":
    main()
