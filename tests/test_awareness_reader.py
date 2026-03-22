"""Tests for AwarenessReader — read-only snapshot consumer."""

import inspect
import json
import os
import tempfile
import unittest

from assistant.awareness_reader import AwarenessReader, AwarenessReaderError


class TestAwarenessReaderReadSnapshots(unittest.TestCase):
    """Verify the reader can list and load frozen snapshots."""

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()
        self.reader = AwarenessReader(snapshots_dir=self.tmpdir)

        # Write two valid snapshots
        for name, data in [
            ("snap_001.json", {"version": "001", "entries": {"a": {"value": 1}}}),
            ("snap_002.json", {"version": "002", "entries": {"b": {"value": 2}}}),
        ]:
            with open(os.path.join(self.tmpdir, name), "w") as fh:
                json.dump(data, fh)

    def test_list_snapshots(self):
        result = self.reader.list_snapshots()
        self.assertEqual(result, ["snap_001.json", "snap_002.json"])

    def test_get_snapshot_by_id(self):
        data = self.reader.get_snapshot("snap_001")
        self.assertEqual(data["version"], "001")

    def test_get_latest_snapshot_id(self):
        self.assertEqual(self.reader.get_latest_snapshot_id(), "snap_002")

    def test_get_latest_snapshot(self):
        data = self.reader.get_latest_snapshot()
        self.assertEqual(data["version"], "002")

    def test_empty_directory(self):
        empty = tempfile.mkdtemp()
        reader = AwarenessReader(snapshots_dir=empty)
        self.assertEqual(reader.list_snapshots(), [])
        self.assertIsNone(reader.get_latest_snapshot_id())

    def test_nonexistent_directory(self):
        reader = AwarenessReader(snapshots_dir="/tmp/does_not_exist_xyz")
        self.assertEqual(reader.list_snapshots(), [])


class TestAwarenessReaderFailsClosed(unittest.TestCase):
    """Verify fail-closed behaviour on malformed data."""

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()
        self.reader = AwarenessReader(snapshots_dir=self.tmpdir)

    def test_malformed_json_raises(self):
        path = os.path.join(self.tmpdir, "bad.json")
        with open(path, "w") as fh:
            fh.write("{not valid json")
        with self.assertRaises(AwarenessReaderError):
            self.reader.get_snapshot("bad")

    def test_non_object_json_raises(self):
        path = os.path.join(self.tmpdir, "array.json")
        with open(path, "w") as fh:
            json.dump([1, 2, 3], fh)
        with self.assertRaises(AwarenessReaderError):
            self.reader.get_snapshot("array")

    def test_missing_snapshot_raises(self):
        with self.assertRaises(AwarenessReaderError):
            self.reader.get_snapshot("nonexistent")

    def test_no_snapshots_raises_on_get_latest(self):
        empty = tempfile.mkdtemp()
        reader = AwarenessReader(snapshots_dir=empty)
        with self.assertRaises(AwarenessReaderError):
            reader.get_latest_snapshot()


class TestAwarenessReaderIsReadOnly(unittest.TestCase):
    """Verify that no write methods exist on AwarenessReader."""

    def test_no_write_methods(self):
        write_prefixes = ("write", "save", "put", "delete", "remove",
                          "update", "create", "emit", "publish", "send")
        methods = inspect.getmembers(AwarenessReader, predicate=inspect.isfunction)
        for name, _ in methods:
            if name.startswith("_"):
                continue
            self.assertFalse(
                any(name.startswith(p) for p in write_prefixes),
                f"AwarenessReader has write-like method: {name}",
            )


if __name__ == "__main__":
    unittest.main()
