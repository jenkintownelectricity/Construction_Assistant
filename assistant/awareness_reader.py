"""
Construction_Assistant v0.1 — AwarenessReader.

Reads frozen awareness snapshot JSON files from a configurable
snapshots directory.  Strictly read-only.  Fails closed on
malformed data.
"""

import json
import os
from typing import Any, Dict, List, Optional

from . import config


class AwarenessReaderError(Exception):
    """Raised when a snapshot cannot be safely read."""


class AwarenessReader:
    """Read-only reader of frozen awareness snapshots.

    This class provides NO methods that write to the cache directory,
    the cognitive bus, or any external system.
    """

    def __init__(self, snapshots_dir: Optional[str] = None) -> None:
        self._snapshots_dir = snapshots_dir or config.SNAPSHOTS_DIR

    # ------------------------------------------------------------------
    # Public read interface
    # ------------------------------------------------------------------

    def list_snapshots(self) -> List[str]:
        """Return sorted list of available snapshot filenames.

        Returns an empty list if the directory does not exist.
        """
        if not os.path.isdir(self._snapshots_dir):
            return []
        entries = [
            f for f in os.listdir(self._snapshots_dir)
            if f.endswith(config.SNAPSHOT_EXTENSION)
        ]
        entries.sort()
        return entries

    def get_latest_snapshot_id(self) -> Optional[str]:
        """Return the ID (filename stem) of the most recent snapshot, or None."""
        snapshots = self.list_snapshots()
        if not snapshots:
            return None
        # Latest = last in sorted order (lexicographic / timestamp-based names)
        return os.path.splitext(snapshots[-1])[0]

    def get_snapshot(self, snapshot_id: str) -> Dict[str, Any]:
        """Load and return a single frozen snapshot by ID.

        Fails closed: returns a clear error rather than partial data.

        Raises:
            AwarenessReaderError: if the snapshot is missing, unreadable,
                                  or contains malformed JSON.
        """
        filename = snapshot_id + config.SNAPSHOT_EXTENSION
        filepath = os.path.join(self._snapshots_dir, filename)

        if not os.path.isfile(filepath):
            raise AwarenessReaderError(
                f"Snapshot not found: {snapshot_id}"
            )

        try:
            with open(filepath, "r", encoding="utf-8") as fh:
                data = json.load(fh)
        except json.JSONDecodeError as exc:
            raise AwarenessReaderError(
                f"Malformed snapshot (invalid JSON): {snapshot_id}"
            ) from exc
        except OSError as exc:
            raise AwarenessReaderError(
                f"Unreadable snapshot: {snapshot_id}"
            ) from exc

        if not isinstance(data, dict):
            raise AwarenessReaderError(
                f"Malformed snapshot (not a JSON object): {snapshot_id}"
            )

        return data

    def get_latest_snapshot(self) -> Dict[str, Any]:
        """Convenience: load the most recent snapshot.

        Raises AwarenessReaderError if no snapshots exist.
        """
        latest_id = self.get_latest_snapshot_id()
        if latest_id is None:
            raise AwarenessReaderError("No snapshots available")
        return self.get_snapshot(latest_id)
