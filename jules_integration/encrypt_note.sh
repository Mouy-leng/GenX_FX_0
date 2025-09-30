#!/bin/bash

# This script encrypts a note's content using GPG and saves it to a secure location.
# It is designed to be called by the JULES dispatcher.

# --- Configuration ---
# The directory where encrypted notes will be stored.
SECURE_DIR="jules_integration/secure_storage"
# The GPG passphrase should be set as an environment variable for security.
GPG_PASSPHRASE="$JULES_GPG_PASSPHRASE"
# The note content is passed via this environment variable from the dispatcher.
NOTE_CONTENT="$JULES_NOTE_CONTENT"

# --- Pre-flight Checks ---
if [ -z "$GPG_PASSPHRASE" ]; then
    echo "Error: JULES_GPG_PASSPHRASE environment variable is not set." >&2
    echo "Cannot encrypt the note without a passphrase." >&2
    exit 1
fi

if [ -z "$NOTE_CONTENT" ]; then
    echo "Error: JULES_NOTE_CONTENT environment variable is empty." >&2
    echo "No content to encrypt." >&2
    exit 1
fi

if [ ! -d "$SECURE_DIR" ]; then
    echo "Error: Secure storage directory '$SECURE_DIR' not found." >&2
    exit 1
fi

# --- Encryption ---
echo "Encrypting secure note..."

# Generate a unique filename for the encrypted note.
# Format: secure-note-YYYYMMDD-HHMMSS-random.gpg
FILENAME="secure-note-$(date +%Y%m%d-%H%M%S)-${RANDOM}.gpg"
OUTPUT_PATH="$SECURE_DIR/$FILENAME"

# Encrypt the content from the environment variable using GPG.
# --batch: Enables batch mode.
# --yes: Overwrites output file if it exists.
# --symmetric: Encrypts with a symmetric cipher.
# --cipher-algo AES256: Specifies the encryption algorithm.
# --passphrase: Provides the passphrase directly as an argument.
echo "$NOTE_CONTENT" | gpg --batch --yes --symmetric --cipher-algo AES256 \
    --passphrase "$GPG_PASSPHRASE" --output "$OUTPUT_PATH"

# --- Verification ---
if [ $? -eq 0 ]; then
    echo "Successfully encrypted and saved note to '$OUTPUT_PATH'."
else
    echo "Error: GPG encryption failed." >&2
    exit 1
fi