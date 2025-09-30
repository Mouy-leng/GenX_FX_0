import os
import unittest
import tempfile
import shutil
from pathlib import Path
from unittest.mock import patch, MagicMock

from jules_integration.parser import MarkdownParser
from jules_integration.dispatcher import Dispatcher

class TestDispatcherIntegration(unittest.TestCase):

    def setUp(self):
        """Set up a temporary directory to simulate the environment."""
        self.test_dir = Path(tempfile.mkdtemp())

        self.jules_integration_dir = self.test_dir / "jules_integration"
        self.jules_integration_dir.mkdir()

        self.notes_dir = self.test_dir / "notes"
        self.notes_dir.mkdir()

        self.secure_storage_dir = self.jules_integration_dir / "secure_storage"
        self.secure_storage_dir.mkdir()

        self.action_mapping_file = self.jules_integration_dir / "action_mapping.yaml"
        self.state_file = self.jules_integration_dir / "state.json"

        with open(self.action_mapping_file, 'w') as f:
            f.write("""
checkbox_actions:
  "Build the project": "npm run build"
  "Run backend tests": "python run_tests.py"
tag_actions:
  "deploy-staging": "echo 'deploying to staging'"
secure_actions:
  "encrypt_and_store": "bash jules_integration/encrypt_note.sh"
""")
        # Create a dummy encryption script for testing
        encrypt_script_path = self.jules_integration_dir / "encrypt_note.sh"
        encrypt_script_path.write_text("#!/bin/bash\necho 'encrypting' > /dev/null")
        encrypt_script_path.chmod(0o755)


        # --- Mock the WebDAV Client ---
        self.mock_webdav_patch = patch('jules_integration.dispatcher.WebDAVClient')
        self.MockWebDAVClient = self.mock_webdav_patch.start()
        self.mock_webdav_instance = self.MockWebDAVClient.return_value

        def mock_list_files(remote_path):
            files = [str(p.relative_to(self.test_dir)) for p in self.notes_dir.glob('*.md')]
            return files

        def mock_get_file_content(remote_path):
            local_path = self.test_dir / remote_path
            return local_path.read_text()

        self.mock_webdav_instance.list_files.side_effect = mock_list_files
        self.mock_webdav_instance.get_file_content.side_effect = mock_get_file_content

        # --- Change to test directory context ---
        self.original_cwd = os.getcwd()
        os.chdir(self.test_dir)
        self.dispatcher = Dispatcher(remote_dir="notes")

    def tearDown(self):
        """Clean up the temporary directory and patches after tests."""
        os.chdir(self.original_cwd)
        self.mock_webdav_patch.stop()
        shutil.rmtree(self.test_dir)

    def _perform_check(self):
        """Simulates one cycle of the dispatcher's monitoring loop."""
        files = self.dispatcher.webdav_client.list_files(self.dispatcher.remote_dir)
        md_files = [f for f in files if f.endswith('.md')]
        for file_path in md_files:
            content = self.dispatcher.webdav_client.get_file_content(file_path)
            if not content: continue

            parser = MarkdownParser(content)
            self.dispatcher._process_checkboxes(parser, file_path)
            self.dispatcher._process_tags(parser, file_path)
            self.dispatcher._process_secure_journal(parser, file_path, content)

    @patch('subprocess.run')
    def test_checkbox_and_tag_dispatching(self, mock_subprocess_run):
        """Tests that both checkbox and tag-based actions are dispatched correctly."""
        note_file = self.notes_dir / "tasks.md"
        note_file.write_text("- [ ] Build the project\n\nSome content with #deploy-staging tag.")

        # Run 1: Nothing is checked, but tag should be processed
        self._perform_check()
        mock_subprocess_run.assert_called_once_with("echo 'deploying to staging'", shell=True, check=True, cwd=str(self.test_dir), env=os.environ)

        # Run 2: Check the task
        mock_subprocess_run.reset_mock()
        note_file.write_text("- [x] Build the project\n\nSome content with #deploy-staging tag.")
        self._perform_check()

        # The checkbox action should be called, but the tag action should not be called again.
        mock_subprocess_run.assert_called_once_with("npm run build", shell=True, check=True, cwd=str(self.test_dir), env=os.environ)

        # Run 3: No new changes, nothing should be called.
        mock_subprocess_run.reset_mock()
        self._perform_check()
        mock_subprocess_run.assert_not_called()

    @patch('subprocess.run')
    def test_secure_journal_dispatch_via_frontmatter(self, mock_subprocess_run):
        """Tests that a note with `secure: true` in frontmatter triggers encryption."""
        note_content = "---\nsecure: true\n---\nThis is a secret note."
        note_file = self.notes_dir / "secret_note.md"
        note_file.write_text(note_content)

        # Run 1: The secure note should be processed.
        self._perform_check()

        # Check that the encryption script was called with the content in the environment
        expected_env = os.environ.copy()
        expected_env['JULES_NOTE_CONTENT'] = note_content
        mock_subprocess_run.assert_called_once_with("bash jules_integration/encrypt_note.sh", shell=True, check=True, cwd=str(self.test_dir), env=expected_env)

        # Run 2: The same secure note should not be processed again.
        mock_subprocess_run.reset_mock()
        self._perform_check()
        mock_subprocess_run.assert_not_called()

    @patch('subprocess.run')
    def test_secure_journal_dispatch_via_tag(self, mock_subprocess_run):
        """Tests that a note with `#secure-journal` tag triggers encryption."""
        note_content = "This is a secret note with a #secure-journal tag."
        note_file = self.notes_dir / "secret_note_by_tag.md"
        note_file.write_text(note_content)

        self._perform_check()

        expected_env = os.environ.copy()
        expected_env['JULES_NOTE_CONTENT'] = note_content
        mock_subprocess_run.assert_called_once_with("bash jules_integration/encrypt_note.sh", shell=True, check=True, cwd=str(self.test_dir), env=expected_env)

if __name__ == '__main__':
    unittest.main()