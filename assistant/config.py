"""
Construction_Assistant v0.1 — Configuration constants.

Paths, output type constants, and operational boundaries.
Standard library only.  No external dependencies.
"""

import os

# --- Storage paths ---
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Default snapshots directory (inside the Awareness Cache repo).
# Override via AWARENESS_SNAPSHOTS_DIR environment variable.
DEFAULT_SNAPSHOTS_DIR = os.path.join(
    os.path.dirname(BASE_DIR),
    "Construction_Awareness_Cache",
    "state",
    "snapshots",
)
SNAPSHOTS_DIR = os.environ.get("AWARENESS_SNAPSHOTS_DIR", DEFAULT_SNAPSHOTS_DIR)

# --- Bounded output types (exhaustive) ---
ALLOWED_OUTPUT_TYPES = frozenset({
    "verified_truth",
    "uncertainty",
    "insufficiency",
    "next_valid_action",
})

# --- Snapshot file extension ---
SNAPSHOT_EXTENSION = ".json"

# --- Schema version this reader understands ---
READER_SCHEMA_VERSION = "0.1"

# --- Hard read-only guarantee ---
# The assistant NEVER writes to these directories.
READONLY_PATHS = frozenset({
    SNAPSHOTS_DIR,
    os.path.join(os.path.dirname(BASE_DIR), "Construction_Cognitive_Bus"),
})
