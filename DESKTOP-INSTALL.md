# Install in ChatGPT Desktop / Codex

This page covers connected repository distribution. The standalone skill remains self-contained for air-gapped use; these instructions are not part of its offline runtime bundle.

## Add the repository marketplace

In the desktop app's plugin marketplace dialog, use the explicit HTTPS clone URL:

```text
https://github.com/eccodolf/c4-mermaid.git
```

Choose **C4 Mermaid** from the added marketplace, then install its `c4-mermaid` plugin. The repository contains a supported `.agents/plugins/marketplace.json`, a portable plugin manifest, a Codex compatibility manifest, and the complete skill under the plugin's `skills/c4-mermaid` directory.

For CLI installation:

```sh
codex plugin marketplace add https://github.com/eccodolf/c4-mermaid.git
codex plugin add c4-mermaid@eccodolf-c4-mermaid
```

Installing the plugin does not require MCP servers, provider credentials, SSH keys, package managers, or build commands. The marketplace entry points to a local directory in the same checkout and never starts another repository clone for the plugin.

## SSH host key verification error

An error mentioning `git@github.com:eccodolf/c4-mermaid.git` and `Host key verification failed` occurs before Git has read this repository's files. Repository contents cannot change the transport selected for that initial clone or configure a client's SSH trust store.

Retry with the complete HTTPS URL above. If the application reuses a previously saved SSH source, remove that failed marketplace entry and add the HTTPS URL again. If Git still rewrites HTTPS into SSH, inspect the client's Git URL rewrite configuration; that is a local setting, not a repository setting. Do not disable host-key verification or accept an unverified SSH host key to install a public repository over HTTPS.

## Local / air-gapped distribution

Transfer a complete reviewed repository checkout, then add it as a local marketplace:

```sh
codex plugin marketplace add /path/to/c4-mermaid
codex plugin add c4-mermaid@eccodolf-c4-mermaid
```

Alternatively transfer only the standalone skill bundle and use its offline installer. Adding a repository marketplace is not a prerequisite for using the skill in another supported harness.

## Maintainers

The root skill is canonical. After an intentional skill update:

```sh
python scripts/verify_bundle.py --write-manifest
python scripts/build_plugin.py
python -m unittest discover -s tests
```

Commit the generated `plugins/c4-mermaid/skills/c4-mermaid` directory. Clients install checked-in files and never need to run the maintainer build. Update both plugin manifest versions together when publishing a new plugin revision.
