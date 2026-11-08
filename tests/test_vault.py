from concurrent.futures import ThreadPoolExecutor
import json
from pathlib import Path
import tempfile
import unittest

from agent_vault.vault import Conflict, INDEX_MARKER, Vault, VaultError


class VaultTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name) / "vault"
        Vault.init(self.root)
        self.vault = Vault(self.root)

    def put(self, path, content):
        file = self.root / path
        file.parent.mkdir(parents=True, exist_ok=True)
        file.write_text(content, encoding="utf-8")

    def test_init_preserves_existing_user_files(self):
        self.put("AGENTS.md", "my own guidance")
        self.put("Home.md", "my own home")
        Vault.init(self.root)
        self.assertEqual((self.root / "AGENTS.md").read_text(), "my own guidance")
        with self.assertRaises(Conflict):
            self.vault.index()
        self.assertEqual((self.root / "Home.md").read_text(), "my own home")

    def test_typed_capture_sources_and_collision(self):
        result = self.vault.create("Atlas project", "A documented fact.", "project", ["https://example.com/brief"], ["demo"])
        note = self.vault.read(result["path"])
        self.assertEqual(note.path, "projects/atlas-project.md")
        self.assertEqual(note.metadata["sources"], ["https://example.com/brief"])
        self.assertEqual(note.metadata["tags"], ["demo"])
        self.assertIn("id", note.metadata)
        with self.assertRaises(Conflict):
            self.vault.create("Atlas project", "Do not overwrite", "project")
        self.assertIn("documented fact", self.vault.read(note.path).body)

    def test_update_preserves_metadata_and_backup_and_checks_revision(self):
        self.put("inbox/manual.md", "---\ntitle: Manual\ntype: note\ncustom: preserved\ndate: 2026-11-08\n---\n\n# Before\n")
        note = self.vault.read("inbox/manual.md")
        updated = self.vault.update(note.path, "# After", note.revision)
        self.assertNotEqual(updated["revision"], note.revision)
        self.assertEqual(self.vault.read(note.path).metadata["custom"], "preserved")
        self.assertEqual((self.root / ".agent-vault/history" / (note.revision + ".md")).read_bytes(), note.raw)
        with self.assertRaises(Conflict):
            self.vault.update(note.path, "stale write", note.revision)
        self.assertEqual(self.vault.read(note.path).body, "# After\n")

    def test_parallel_agents_do_not_silently_overwrite(self):
        note = self.vault.create("Shared", "Original")
        def attempt(body):
            try:
                self.vault.update(note["path"], body, note["revision"])
                return "saved"
            except Conflict:
                return "conflict"
        with ThreadPoolExecutor(max_workers=2) as pool:
            outcomes = list(pool.map(attempt, ["Agent one", "Agent two"]))
        self.assertCountEqual(outcomes, ["saved", "conflict"])

    def test_path_traversal_hidden_files_and_reserved_names(self):
        for path in ["../secret.md", "/tmp/secret.md", "a/../secret.md", ".private/x.md",
                     "a\\b.md", "C:/secret.md", "image.png", "Home.md", "AGENTS.md", "home.md", "agents.md",
                     "inbox//x.md", "inbox/x.md/"]:
            with self.subTest(path=path), self.assertRaises(VaultError):
                self.vault.read(path)

    def test_symlink_escape_and_private_state(self):
        outside = Path(self.temporary.name) / "outside"
        outside.mkdir()
        (outside / "secret.md").write_text("private")
        try:
            (self.root / "shortcut").symlink_to(outside, target_is_directory=True)
        except (OSError, NotImplementedError):
            self.skipTest("Symlink creation unavailable")
        with self.assertRaises(VaultError):
            self.vault.read("shortcut/secret.md")
        self.assertEqual(self.vault.scan()[0], {})
        # Use a separate new vault with an explicitly hostile private-state path.
        other = Path(self.temporary.name) / "other"
        other.mkdir()
        (other / ".agent-vault").symlink_to(outside, target_is_directory=True)
        with self.assertRaises(VaultError):
            Vault.init(other)
        self.assertFalse((outside / "config.json").exists())

    def test_link_graph_aliases_markdown_and_code_examples(self):
        self.put("people/alice.md", "---\ntitle: Alice Example\naliases: [Alice]\n---\n# Alice Example\n")
        self.put("projects/atlas.md", "# Atlas\n\n[[Alice]]\n[Person](../people/alice.md)\n\n```md\n[[Imaginary]]\n```\n`[[Not a link]]`\n")
        graph = self.vault.graph()
        self.assertEqual(graph["edges"], [{"source": "projects/atlas.md", "target": "people/alice.md"}])
        self.assertEqual(graph["unresolved"], [])
        self.assertEqual(len(self.vault.context("Alice", depth=1, limit=1)["documents"]), 2)

    def test_ambiguous_and_missing_links_are_not_guessed(self):
        self.put("people/a.md", "# Alex\n")
        self.put("people/b.md", "# Alex\n")
        self.put("inbox/example.md", "# Example\n[[Alex]] [[Missing]]")
        result = self.vault.doctor()
        self.assertFalse(result["ok"])
        self.assertCountEqual([x["reason"] for x in result["unresolved"]], ["ambiguous", "unresolved"])
        self.assertEqual(result["links"], 0)

    def test_existing_plain_markdown_and_external_edits_are_immediate(self):
        self.put("manual.md", "# Existing note\nOriginal text")
        self.assertEqual(self.vault.search("Original")["matches"][0]["path"], "manual.md")
        self.put("manual.md", "# Existing note\nNew result")
        self.assertEqual(self.vault.search("Original")["matches"], [])
        self.assertEqual(self.vault.search("New result")["total_matches"], 1)

    def test_malformed_yaml_and_oversized_notes_surface_in_diagnostics(self):
        self.put("bad.md", "---\ntags: wrong\n---\n# Malformed")
        self.put("huge.md", "x" * 1_000_001)
        self.assertEqual(len(self.vault.search("anything")["issues"]), 2)
        self.assertFalse(self.vault.doctor()["ok"])

    def test_invalid_yaml_cannot_construct_objects(self):
        self.put("bad.md", "---\nx: !!python/object/apply:os.system ['echo unsafe']\n---\n")
        with self.assertRaises(VaultError):
            self.vault.read("bad.md")

    def test_malformed_metadata_and_url_do_not_crash_graph(self):
        self.put("invalid.md", "---\nid: [not, a, string]\n---\n# Invalid")
        self.put("valid.md", "# Valid\n[External](//[invalid)\n")
        result = self.vault.graph()
        self.assertEqual(len(result["issues"]), 1)
        self.assertEqual(result["unresolved"], [])

    def test_context_budget_is_bounded_and_reports_truncation(self):
        self.vault.create("Long topic", "x" * 1000)
        result = self.vault.context("Long", max_chars=500)
        self.assertEqual(result["body_chars"], 500)
        self.assertTrue(result["documents"][0]["truncated"])
        self.assertTrue(result["budget_exhausted"])
        self.assertTrue(result["content_is_untrusted"])

    def test_link_checks_target_and_is_idempotent_after_reread(self):
        first = self.vault.create("First", "One")
        second = self.vault.create("Second", "Two")
        linked = self.vault.link(first["path"], second["path"], first["revision"])
        again = self.vault.link(first["path"], second["path"], linked["revision"])
        self.assertTrue(again["already_linked"])
        self.assertEqual(len(self.vault.graph()["edges"]), 1)
        with self.assertRaises(VaultError):
            self.vault.create("Broken", "Body", links=["missing.md"])
        self.assertFalse((self.root / "inbox/broken.md").exists())

    def test_suggestions_are_preview_only(self):
        first = self.vault.create("Meeting", "We discussed Atlas project.")
        self.vault.create("Atlas project", "A project", "project")
        before = self.vault.read(first["path"]).raw
        result = self.vault.suggest()
        self.assertEqual(result["total"], 1)
        self.assertFalse(result["applied"])
        self.assertEqual(before, self.vault.read(first["path"]).raw)

    def test_organize_previews_then_moves_unlinked_typed_note(self):
        self.put("loose.md", "---\ntitle: A topic\ntype: topic\n---\n# A topic\n")
        note = self.vault.read("loose.md")
        result = self.vault.organize(note.path, note.revision)
        self.assertEqual(result["destination"], "topics/loose.md")
        self.assertFalse(result["applied"])
        self.assertTrue((self.root / "loose.md").exists())
        result = self.vault.organize(note.path, note.revision, apply=True)
        self.assertTrue(result["applied"])
        self.assertEqual(self.vault.read("topics/loose.md").raw, note.raw)

    def test_organize_refuses_to_break_links_or_clobber_destination(self):
        self.put("loose.md", "---\ntype: topic\n---\n# Loose\n")
        self.put("ref.md", "# Reference\n[[loose]]")
        note = self.vault.read("loose.md")
        self.assertTrue(self.vault.organize(note.path, note.revision)["blocked"])
        with self.assertRaises(Conflict):
            self.vault.organize(note.path, note.revision, apply=True)
        self.put("another.md", "---\ntype: topic\n---\n# Another\n")
        self.put("topics/another.md", "# Existing")
        other = self.vault.read("another.md")
        with self.assertRaises(Conflict):
            self.vault.organize(other.path, other.revision, apply=True)
        self.assertEqual((self.root / "topics/another.md").read_text(), "# Existing")

    def test_classify_existing_markdown_preserves_body_and_other_metadata(self):
        self.put("loose.md", "---\ncustom: keep\n---\n# Existing project\nEvidence stays here.\n")
        note = self.vault.read("loose.md")
        result = self.vault.classify(note.path, "project", note.revision)
        updated = self.vault.read(note.path)
        self.assertEqual(updated.body, note.body)
        self.assertEqual(updated.metadata["custom"], "keep")
        self.assertEqual(result["type"], "project")
        self.assertTrue(self.vault.organize(note.path, result["revision"])["change_needed"])
        with self.assertRaises(Conflict):
            self.vault.classify(note.path, "topic", note.revision)

    def test_home_index_and_duplicate_ids(self):
        created = self.vault.create("Indexed", "One note", "topic")
        self.vault.index()
        self.assertIn(INDEX_MARKER, (self.root / "Home.md").read_text())
        self.assertIn("[[topics/indexed|Indexed]]", (self.root / "Home.md").read_text())
        self.put("duplicate.md", self.vault.read(created["path"]).raw.decode())
        self.assertEqual(len(self.vault.doctor()["duplicate_ids"]), 1)


if __name__ == "__main__":
    unittest.main()
