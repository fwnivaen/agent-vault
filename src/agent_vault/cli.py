"""JSON CLI for agents; no provider API or Obsidian process is required."""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import sys

from . import __version__
from .vault import FOLDERS, Vault, VaultError


def parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="agent-vault", description=__doc__)
    p.add_argument("--version", action="version", version=__version__)
    p.add_argument("--vault", default=os.environ.get("AGENT_VAULT"), help="Absolute or relative vault directory")
    sub = p.add_subparsers(dest="command", required=True)
    sub.add_parser("init", help="Create folders and agent guidance without overwriting notes")
    capture = sub.add_parser("capture", help="Create a typed, sourced Markdown note")
    capture.add_argument("--title", required=True)
    capture.add_argument("--type", choices=FOLDERS, default="note", dest="kind")
    capture.add_argument("--source", action="append", default=[])
    capture.add_argument("--tag", action="append", default=[])
    capture.add_argument("--link", action="append", default=[])
    for command in [capture, sub.add_parser("update", help="Update a body using its current revision")]:
        group = command.add_mutually_exclusive_group(required=True)
        group.add_argument("--body")
        group.add_argument("--body-file", type=Path, help="UTF-8 Markdown body file to import")
        if command is not capture:
            command.add_argument("path")
            command.add_argument("--revision", required=True)
    read = sub.add_parser("read")
    read.add_argument("path")
    classify = sub.add_parser("classify", help="Set an existing note's type without changing its path")
    classify.add_argument("path")
    classify.add_argument("--type", choices=FOLDERS, required=True, dest="kind")
    classify.add_argument("--revision", required=True)
    for command in [sub.add_parser("search"), sub.add_parser("context")]:
        command.add_argument("query")
        command.add_argument("--limit", type=int, default=5)
        if command.prog.endswith(" context"):
            command.add_argument("--depth", type=int, default=1)
            command.add_argument("--max-chars", type=int, default=16000)
    sub.add_parser("graph", help="Current link graph, unresolved links and parse issues")
    suggest = sub.add_parser("suggest", help="Preview title/alias link candidates")
    suggest.add_argument("--limit", type=int, default=20)
    link = sub.add_parser("link", help="Add a checked relationship between existing notes")
    link.add_argument("source")
    link.add_argument("target")
    link.add_argument("--revision", required=True)
    organize = sub.add_parser("organize", help="Preview a type-based move; --apply commits a safe move")
    organize.add_argument("path")
    organize.add_argument("--revision", required=True)
    organize.add_argument("--apply", action="store_true")
    sub.add_parser("index", help="Generate an Obsidian Home.md map")
    sub.add_parser("doctor", help="Check broken/ambiguous links, duplicates and malformed notes")
    serve = sub.add_parser("serve", help="Expose the vault to an MCP-compatible agent over stdio")
    serve.add_argument("--allow-write", action="store_true", help="Explicitly expose mutation tools")
    return p


def main(argv: list[str] | None = None) -> int:
    p = parser()
    args = p.parse_args(argv)
    if not args.vault:
        p.error("--vault or AGENT_VAULT is required; a vault is never selected implicitly")
    try:
        if args.command == "init":
            result = Vault.init(args.vault)
        else:
            vault = Vault(args.vault)
            if args.command == "serve":
                from .server import serve
                serve(vault, allow_write=args.allow_write)
                return 0
            if args.command in {"capture", "update"}:
                body = args.body_file.read_text(encoding="utf-8") if args.body_file else args.body
            if args.command == "capture":
                result = vault.create(args.title, body, args.kind, args.source, args.tag, args.link)
            elif args.command == "update":
                result = vault.update(args.path, body, args.revision)
            elif args.command == "read":
                note = vault.read(args.path)
                result = {**note.summary(), "metadata": note.metadata, "body": note.body}
            elif args.command == "classify":
                result = vault.classify(args.path, args.kind, args.revision)
            elif args.command == "search":
                result = vault.search(args.query, args.limit)
            elif args.command == "context":
                result = vault.context(args.query, args.depth, args.max_chars, args.limit)
            elif args.command == "graph":
                result = vault.graph()
            elif args.command == "suggest":
                result = vault.suggest(args.limit)
            elif args.command == "link":
                result = vault.link(args.source, args.target, args.revision)
            elif args.command == "organize":
                result = vault.organize(args.path, args.revision, args.apply)
            elif args.command == "index":
                result = vault.index()
            elif args.command == "doctor":
                result = vault.doctor()
        print(json.dumps(result, ensure_ascii=False, indent=2, default=str))
        return 1 if args.command == "doctor" and not result["ok"] else 0
    except (VaultError, OSError, UnicodeError) as exc:
        print(json.dumps({"error": str(exc), "type": type(exc).__name__}), file=sys.stderr)
        return 2
