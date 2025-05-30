#!/bin/bash

# Make all Python and shell scripts executable
chmod +x $(find $(dirname $0) -name "*.py" -o -name "*.sh")

echo "All scripts are now executable."
