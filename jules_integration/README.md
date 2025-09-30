# JULES - LiteWriter Integration for GenX FX

This directory contains a command-line integration that connects a WebDAV-enabled note-taking application (like LiteWriter) to the GenX FX trading platform. It allows you to trigger automated workflows, such as builds, tests, and deployments, directly from your Markdown notes.

## How It Works

The system works by monitoring a directory on a WebDAV server for changes to Markdown files. It can be triggered in three ways:

1.  **Checkboxes**: When a task is checked off (e.g., `- [x] Build the project`), a corresponding command is executed.
2.  **Tags**: When a specific tag (e.g., `#deploy-staging`) is found in a note, a command is run. This action is triggered only once per file for a given tag.
3.  **Secure Journals**: When a note is marked as secure, either in its YAML frontmatter (`secure: true`) or with a specific tag (`#secure-journal`), its content is encrypted with GPG and saved to a secure location.

This creates a powerful "GitOps-style" workflow where your notes become a control panel for your development and operations tasks.

## 1. Setup and Configuration

Follow these steps to set up and configure the integration service.

### Step 1: Install Dependencies

The required Python libraries are listed in `requirements.txt`.

```bash
pip install -r jules_integration/requirements.txt
```

### Step 2: Configure WebDAV Credentials

The service needs to connect to your WebDAV server. Set the following environment variables:

```bash
export WEBDAV_HOSTNAME="https://your-webdav-server.com/remote.php/webdav/"
export WEBDAV_LOGIN="your_username"
export WEBDAV_PASSWORD="your_password"
```

### Step 3: Configure GPG for Secure Journaling (Optional)

To use the secure journaling feature, you need `gpg` installed on your system. You also need to set a passphrase as an environment variable. The encryption script uses this to secure your notes.

```bash
# Make sure GPG is installed (e.g., `sudo apt-get install gnupg`)
export JULES_GPG_PASSPHRASE="your-strong-encryption-password"
```
**Security Note:** For better security, consider using a tool like `direnv` or placing secrets in your shell's profile (e.g., `~/.bashrc` or `~/.zshrc`) rather than saving them in plaintext scripts.

### Step 4: Configure Action Mappings

You need to tell the dispatcher what to do for each trigger.

1.  **Rename the example file:**
    ```bash
    mv jules_integration/action_mapping.yaml.example jules_integration/action_mapping.yaml
    ```
2.  **Edit `action_mapping.yaml`:**
    Open the file and customize the mappings under the appropriate sections: `checkbox_actions`, `tag_actions`, or `secure_actions`.

## 2. Running the Service

Once configured, start the monitoring service using the provided shell script.

**Important:** Run this script from the **root directory** of the GenX_FX project.

```bash
bash run_integration_service.sh
```

The script will start the dispatcher, which will begin polling your WebDAV server for changes. To stop the service, press `Ctrl+C`.

## 3. Example Usage

### Example 1: Triggering a Build with a Checkbox

1.  In your note-taking app, add the following task to a file:
    ```markdown
    - [ ] Build the project
    ```
2.  Check the box: `- [x] Build the project`.
3.  When the note syncs, the dispatcher will see the completed task and run the command mapped to `"Build the project"` in your `action_mapping.yaml`.

### Example 2: Triggering a Deployment with a Tag

1.  Create a new note or edit an existing one and add a tag:
    ```markdown
    # Deployment Plan

    Today, we are deploying to staging. #deploy-staging
    ```
2.  When the note syncs, the dispatcher will find the `#deploy-staging` tag and execute the corresponding command from `tag_actions`. This will only happen once for this file, even if you edit it again.

### Example 3: Creating a Secure Journal Entry

You can mark a note as secure in two ways.

**Option A: Using YAML Frontmatter**
```markdown
---
secure: true
title: 'My Secret Thoughts'
---

This content will be encrypted.
```

**Option B: Using a Tag**
```markdown
# Private Journal Entry

This note contains sensitive information and should be encrypted. #secure-journal
```

When either of these notes is synced, the dispatcher will trigger the `encrypt_and_store` action. The entire content of the note will be encrypted with GPG and saved in the `jules_integration/secure_storage/` directory.