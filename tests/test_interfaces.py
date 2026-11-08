import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from agent_vault.vault import Vault


class CliTests(unittest.TestCase):
    def test_documented_workflow_and_error_codes(self):
        with tempfile.TemporaryDirectory(prefix="agent vault ") as folder:
            def run(*args):
                return subprocess.run([sys.executable, "-m", "agent_vault", "--vault", folder, *args],
                                      capture_output=True, text=True, timeout=15)
            self.assertEqual(run("init").returncode, 0)
            result = run("capture", "--type", "project", "--title", "Atlas", "--body", "A demo")
            self.assertEqual(result.returncode, 0, result.stderr)
            note = json.loads(result.stdout)
            self.assertEqual(run("read", note["path"]).returncode, 0)
            result = run("update", note["path"], "--revision", "stale", "--body", "Overwrite")
            self.assertEqual(result.returncode, 2)
            self.assertEqual(json.loads(result.stderr)["type"], "Conflict")
            self.assertEqual(run("context", "Atlas").returncode, 0)
            self.assertEqual(run("doctor").returncode, 0)
            Path(folder, "broken.md").write_text("# Broken\n[[missing]]", encoding="utf-8")
            self.assertEqual(run("doctor").returncode, 1)


@unittest.skipUnless(importlib.util.find_spec("mcp"), "Install the optional mcp extra")
class McpTests(unittest.IsolatedAsyncioTestCase):
    async def test_real_stdio_read_only_tools_and_context(self):
        from mcp import Client, StdioServerParameters
        with tempfile.TemporaryDirectory(prefix="agent vault ") as folder:
            Vault.init(folder)
            vault = Vault(folder)
            project = vault.create("Atlas", "A fictional project", "project")
            vault.create("Use Markdown", "Decision for Atlas", "decision", links=[project["path"]])
            params = StdioServerParameters(command=sys.executable,
                args=["-m", "agent_vault", "--vault", folder, "serve"])
            async with Client(params, read_timeout_seconds=15, mode="legacy") as client:
                listing = await client.list_tools()
                names = {t.name for t in listing.tools}
                self.assertEqual(len(names), 6)
                self.assertNotIn("capture_note", names)
                self.assertTrue(all(t.annotations.read_only_hint for t in listing.tools))
                result = await client.call_tool("get_context", {"query": "Atlas"})
                self.assertFalse(result.is_error)
                self.assertEqual(len(result.structured_content["documents"]), 2)
                result = await client.call_tool("read_note", {"path": "../outside.md"})
                self.assertTrue(result.is_error)
                self.assertIn("visible .md", result.content[0].text)

    async def test_second_agent_reads_first_agents_saved_note(self):
        from mcp import Client, StdioServerParameters
        with tempfile.TemporaryDirectory(prefix="agent vault ") as folder:
            Vault.init(folder)
            params = StdioServerParameters(command=sys.executable,
                args=["-m", "agent_vault", "--vault", folder, "serve", "--allow-write"])
            async with Client(params, read_timeout_seconds=15) as first_agent:
                listing = await first_agent.list_tools()
                self.assertEqual(len(listing.tools), 12)
                created = await first_agent.call_tool("capture_note", {
                    "title": "Portable decision", "body": "An agreed fictional choice", "kind": "decision",
                    "sources": ["https://example.com/decision"]})
                self.assertFalse(created.is_error)
                saved = created.structured_content
            async with Client(params, read_timeout_seconds=15) as next_agent:
                read = await next_agent.call_tool("read_note", {"path": saved["path"]})
                self.assertEqual(read.structured_content["revision"], saved["revision"])
                self.assertEqual(read.structured_content["sources"], ["https://example.com/decision"])
                changed = await next_agent.call_tool("update_note", {
                    "path": saved["path"], "body": "# Updated decision\nMore evidence", "revision": saved["revision"]})
                self.assertFalse(changed.is_error)
                stale = await next_agent.call_tool("update_note", {
                    "path": saved["path"], "body": "stale overwrite", "revision": saved["revision"]})
                self.assertTrue(stale.is_error)
                self.assertIn("Revision conflict", stale.content[0].text)
            self.assertIn("More evidence", Vault(folder).read(saved["path"]).body)


if __name__ == "__main__":
    unittest.main()
