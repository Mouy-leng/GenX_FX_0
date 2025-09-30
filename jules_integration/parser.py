import re
import frontmatter
import yaml

class MarkdownParser:
    """
    A parser for Markdown files to extract actionable triggers like
    checkboxes, YAML frontmatter, and inline tags.
    """
    def __init__(self, markdown_content):
        """
        Initializes the parser with the Markdown content.

        Args:
            markdown_content (str): The string content of the Markdown file.
        """
        self.content = markdown_content
        self.post = frontmatter.loads(self.content)

    def parse_checkboxes(self):
        """
        Parses the Markdown content to find all checkbox tasks.

        A checkbox is a line starting with '- [ ]' or '- [x]'.

        Returns:
            list: A list of dictionaries, where each dictionary represents a task
                  and has 'task', 'checked', and 'line' keys.
        """
        # Pattern to match '- [ ] task' or '- [x] task'
        pattern = r"^\s*-\s*\[(x| )\]\s*(.*)"
        tasks = []
        for line in self.post.content.splitlines():
            match = re.match(pattern, line)
            if match:
                checked_char, task_description = match.groups()
                tasks.append({
                    "task": task_description.strip(),
                    "checked": checked_char == 'x',
                    "line": line.strip()
                })
        return tasks

    def parse_tags(self):
        """
        Parses the Markdown content to find all inline tags.

        A tag is a word prefixed with '#', like #deploy or #urgent.
        Tags can include hyphens.

        Returns:
            list: A list of unique tags found in the content (without the '#').
        """
        # Pattern to find words starting with #, allowing for hyphens
        pattern = r"#([\w-]+)"
        tags = re.findall(pattern, self.post.content)
        return list(set(tags))

    def get_frontmatter(self):
        """
        Returns the YAML frontmatter from the Markdown file.

        Returns:
            dict: A dictionary containing the parsed YAML frontmatter.
        """
        return self.post.metadata

if __name__ == '__main__':
    # Example usage of the MarkdownParser
    example_md = """\
---
title: 'My Awesome Note'
author: 'Jules'
tags: ['automation', 'testing']
agent:
  name: 'build-agent'
  trigger: 'on-commit'
---

This is a note to demonstrate the parser.

## Tasks
- [x] Write the parser module.
- [ ] Write the dispatcher logic.
- [ ] Add #documentation.

## Notes
Here are some additional notes about the #project.
This is a #test tag.
"""

    print("--- Parsing Example Markdown ---")
    parser = MarkdownParser(example_md)

    # 1. Get YAML frontmatter
    metadata = parser.get_frontmatter()
    print("\n[1] YAML Frontmatter:")
    print(yaml.dump(metadata, indent=2))

    # 2. Get Checkboxes
    checkboxes = parser.parse_checkboxes()
    print("\n[2] Checkbox Tasks:")
    if checkboxes:
        for task in checkboxes:
            status = "DONE" if task['checked'] else "TODO"
            print(f"- [{status}] {task['task']}")
    else:
        print("No checkboxes found.")

    # 3. Get Inline Tags
    tags = parser.parse_tags()
    print("\n[3] Inline Tags:")
    if tags:
        print(f"Found tags: {', '.join(tags)}")
    else:
        print("No inline tags found.")

    print("\n--- Parsing Complete ---")