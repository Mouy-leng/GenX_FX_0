import os
import json
import subprocess
import time
import yaml
import hashlib
from jules_integration.webdav_client import WebDAVClient
from jules_integration.parser import MarkdownParser

class Dispatcher:
    """
    Monitors a WebDAV directory for changes in Markdown files and dispatches
    actions based on their content (checkboxes, tags).
    """
    def __init__(self, remote_dir="/", poll_interval=15):
        """
        Initializes the Dispatcher.

        Args:
            remote_dir (str): The directory on the WebDAV server to monitor.
            poll_interval (int): The time in seconds between each check for changes.
        """
        self.remote_dir = remote_dir
        self.poll_interval = poll_interval
        self.state_file = "jules_integration/state.json"
        self.action_mapping_file = "jules_integration/action_mapping.yaml"

        print("Initializing Dispatcher...")
        self.webdav_client = WebDAVClient()
        self.actions = self._load_action_mapping()
        self.state = self._load_state()
        print("Dispatcher initialized successfully.")

    def _load_action_mapping(self):
        """Loads the action mapping from the YAML configuration file."""
        try:
            with open(self.action_mapping_file, 'r') as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            print(f"Warning: Action mapping file not found at '{self.action_mapping_file}'.")
            print("Please create it. No actions will be dispatched.")
            return {}
        except yaml.YAMLError as e:
            print(f"Error parsing action mapping file: {e}")
            return {}

    def _load_state(self):
        """Loads the last known state from the state file."""
        try:
            with open(self.state_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            # Initialize state for all trigger types
            return {"processed_tasks": [], "processed_tags": {}, "processed_secure_files": []}

    def _save_state(self):
        """Saves the current state to the state file."""
        with open(self.state_file, 'w') as f:
            json.dump(self.state, f, indent=2)

    def _get_task_hash(self, task_line):
        """Creates a unique hash for a task line to track its state."""
        return hashlib.sha1(task_line.encode()).hexdigest()

    def _dispatch_action(self, action_type, keyword, file_path, context=None):
        """Finds and executes the command associated with a keyword and action type."""
        action_group = self.actions.get(action_type, {})
        command_template = action_group.get(keyword)

        if command_template:
            print(f"Action triggered for {action_type} '{keyword}' in file '{file_path}'.")

            # For secure routing, we pass the file content via an environment variable
            command = command_template
            env = os.environ.copy()
            if action_type == 'secure_actions' and context and 'content' in context:
                env['JULES_NOTE_CONTENT'] = context['content']
                print("Note content passed to secure action environment.")

            print(f"Executing command: {command}")
            try:
                subprocess.run(command, shell=True, check=True, cwd=os.getcwd(), env=env)
                print(f"Successfully executed command for '{keyword}'.")
            except subprocess.CalledProcessError as e:
                print(f"Error executing command for '{keyword}': {e}")
            except Exception as e:
                print(f"An unexpected error occurred during command execution: {e}")
        else:
            print(f"No action defined for {action_type}: '{keyword}'")

    def _process_checkboxes(self, parser, file_path):
        """Processes checkbox-based actions."""
        checkboxes = parser.parse_checkboxes()
        for task in checkboxes:
            task_hash = self._get_task_hash(task['line'])
            if task['checked'] and task_hash not in self.state['processed_tasks']:
                print(f"New completed task found: \"{task['task']}\"")
                self._dispatch_action('checkbox_actions', task['task'], file_path)
                self.state['processed_tasks'].append(task_hash)
                self._save_state()

    def _process_tags(self, parser, file_path):
        """Processes tag-based actions."""
        tags = parser.parse_tags()
        if file_path not in self.state['processed_tags']:
            self.state['processed_tags'][file_path] = []

        for tag in tags:
            if tag not in self.state['processed_tags'][file_path]:
                print(f"New tag found: '#{tag}' in '{file_path}'")
                self._dispatch_action('tag_actions', tag, file_path)
                self.state['processed_tags'][file_path].append(tag)
                self._save_state()

    def _process_secure_journal(self, parser, file_path, content):
        """Processes secure journal routing."""
        frontmatter = parser.get_frontmatter()
        tags = parser.parse_tags()

        is_secure = frontmatter.get('secure') is True or 'secure-journal' in tags

        if is_secure and file_path not in self.state['processed_secure_files']:
            print(f"Secure journal entry detected: '{file_path}'")
            context = {'content': content}
            self._dispatch_action('secure_actions', 'encrypt_and_store', file_path, context=context)
            self.state['processed_secure_files'].append(file_path)
            self._save_state()

    def run_monitor(self):
        """Starts the main monitoring loop."""
        print(f"Starting WebDAV monitor for directory: '{self.remote_dir}'")
        while True:
            try:
                print("\nChecking for updated notes...")
                files = self.webdav_client.list_files(self.remote_dir)

                md_files = [f for f in files if f.endswith('.md')]

                for file_path in md_files:
                    content = self.webdav_client.get_file_content(file_path)
                    if content is None:
                        continue

                    parser = MarkdownParser(content)

                    # Process all trigger types
                    self._process_checkboxes(parser, file_path)
                    self._process_tags(parser, file_path)
                    self._process_secure_journal(parser, file_path, content)

                print(f"Check complete. Waiting for {self.poll_interval} seconds...")
                time.sleep(self.poll_interval)

            except KeyboardInterrupt:
                print("\nShutting down dispatcher.")
                break
            except Exception as e:
                print(f"An error occurred in the monitoring loop: {e}")
                time.sleep(self.poll_interval)


if __name__ == '__main__':
    # Make sure to set your WebDAV environment variables before running this.
    # export WEBDAV_HOSTNAME="your_webdav_url"
    # export WEBDAV_LOGIN="your_username"
    # export WEBDAV_PASSWORD="your_password"
    try:
        dispatcher = Dispatcher()
        dispatcher.run_monitor()
    except ValueError as e:
        print(f"Failed to initialize dispatcher: {e}")
    except Exception as e:
        print(f"A critical error occurred: {e}")