from jules_integration.parser import MarkdownParser

# A sample Markdown document to be used across multiple tests
COMPREHENSIVE_MD_EXAMPLE = """\
---
title: 'Comprehensive Test Note'
author: 'Jules Tester'
tags: ['testing', 'parser-logic']
agent:
  name: 'parser-test-agent'
  active: true
---

## Main Content

This document is for testing the Markdown parser.

### Checkbox Tasks
- [x] A completed task.
- [ ] An incomplete task.
- [ ] Another incomplete task with an #urgent tag.
- [x] A final completed task with a #project-gamma tag.

### Tags Section
This section includes various tags like #planning, #review, and #final-release.
"""

def test_parse_checkboxes_with_varied_content():
    """
    Tests that checkboxes are correctly parsed, including their state and text.
    """
    parser = MarkdownParser(COMPREHENSIVE_MD_EXAMPLE)
    tasks = parser.parse_checkboxes()

    assert len(tasks) == 4, "Should find all four tasks"

    # Test first task
    assert tasks[0]['task'] == 'A completed task.'
    assert tasks[0]['checked'] is True
    assert tasks[0]['line'] == '- [x] A completed task.'

    # Test second task
    assert tasks[1]['task'] == 'An incomplete task.'
    assert tasks[1]['checked'] is False
    assert tasks[1]['line'] == '- [ ] An incomplete task.'

    # Test third task (with inline tag)
    assert tasks[2]['task'] == 'Another incomplete task with an #urgent tag.'
    assert tasks[2]['checked'] is False

    # Test fourth task (with inline tag)
    assert tasks[3]['task'] == 'A final completed task with a #project-gamma tag.'
    assert tasks[3]['checked'] is True

def test_parse_inline_tags():
    """
    Tests that all unique inline tags are extracted from the content.
    """
    parser = MarkdownParser(COMPREHENSIVE_MD_EXAMPLE)
    tags = parser.parse_tags()

    assert len(tags) == 5, "Should find all unique tags"
    expected_tags = ['urgent', 'project-gamma', 'planning', 'review', 'final-release']
    for tag in expected_tags:
        assert tag in tags, f"Expected tag '{tag}' not found"

def test_get_yaml_frontmatter():
    """
    Tests that the YAML frontmatter is correctly parsed into a dictionary.
    """
    parser = MarkdownParser(COMPREHENSIVE_MD_EXAMPLE)
    metadata = parser.get_frontmatter()

    assert metadata['title'] == 'Comprehensive Test Note'
    assert metadata['author'] == 'Jules Tester'
    assert metadata['tags'] == ['testing', 'parser-logic']
    assert isinstance(metadata['agent'], dict)
    assert metadata['agent']['name'] == 'parser-test-agent'
    assert metadata['agent']['active'] is True

def test_parser_with_empty_content():
    """
    Tests that the parser handles empty strings gracefully without errors.
    """
    parser = MarkdownParser("")
    assert parser.parse_checkboxes() == [], "Checkboxes should be empty for empty content"
    assert parser.parse_tags() == [], "Tags should be empty for empty content"
    assert parser.get_frontmatter() == {}, "Frontmatter should be an empty dict for empty content"

def test_parser_with_no_frontmatter():
    """
    Tests parsing of content that does not have a YAML frontmatter block.
    """
    md_content = """
# Just Content

- [ ] A single task here.
- A line that is not a task.
Some #random-tag.
"""
    parser = MarkdownParser(md_content)

    tasks = parser.parse_checkboxes()
    assert len(tasks) == 1
    assert tasks[0]['task'] == 'A single task here.'
    assert tasks[0]['checked'] is False

    tags = parser.parse_tags()
    assert tags == ['random-tag']

    metadata = parser.get_frontmatter()
    assert metadata == {}, "Frontmatter should be empty when none is provided"