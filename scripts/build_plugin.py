#!/usr/bin/env python3
"""Maintainer: copy the verified portable skill into its repository plugin package."""

from pathlib import Path
import shutil

from verify_bundle import BUNDLE_ENTRIES, MANIFEST, verify


def main():
    root = Path(__file__).resolve().parent.parent
    errors = verify(root)
    if errors:
        raise SystemExit("Source bundle verification failed: " + "; ".join(errors))
    destination = root / "plugins/c4-mermaid/skills/c4-mermaid"
    destination.mkdir(parents=True, exist_ok=True)
    for name in (*BUNDLE_ENTRIES, MANIFEST):
        source = root / name
        if source.is_dir():
            shutil.copytree(
                source, destination / name, dirs_exist_ok=True,
                ignore=shutil.ignore_patterns("__pycache__", "*.pyc", "*.pyo"),
            )
        else:
            shutil.copy2(source, destination / name)
    errors = verify(destination)
    if errors:
        raise SystemExit("Packaged bundle verification failed: " + "; ".join(errors))
    print("Built and verified repository plugin: " + str(destination))


if __name__ == "__main__":
    main()
