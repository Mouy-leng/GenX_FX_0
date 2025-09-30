#!/bin/bash

# This script starts the JULES WebDAV integration service.
# It runs the dispatcher, which monitors for changes in your notes
# and triggers the configured actions.

# Ensure the script is run from the root of the GenX_FX project directory
if [ ! -f "jules_integration/dispatcher.py" ]; then
    echo "Error: This script must be run from the root of the GenX_FX project."
    echo "Please navigate to the project root and run it again."
    exit 1
fi

echo "Starting JULES Integration Service..."
echo "Press Ctrl+C to stop the service."

# Set the PYTHONPATH to include the project root, so imports work correctly
export PYTHONPATH=$(pwd)

# Run the dispatcher
python3 jules_integration/dispatcher.py

echo "JULES Integration Service stopped."