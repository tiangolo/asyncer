#!/usr/bin/env bash

set -e

export DYLD_FALLBACK_LIBRARY_PATH="/opt/homebrew/lib"

mkdocs serve --config-file mkdocs.insiders.yml
