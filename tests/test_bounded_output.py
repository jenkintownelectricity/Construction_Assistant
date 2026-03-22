"""Tests for BoundedOutputContract — type enforcement and provenance."""

import unittest

from assistant.bounded_output_contract import (
    BoundedOutput,
    BoundedOutputContract,
    OutputContractViolation,
)
from assistant.config import ALLOWED_OUTPUT_TYPES


class TestOutputContractEnforcesTypes(unittest.TestCase):
    """Only the four allowed types may be created."""

    def test_all_valid_types_succeed(self):
        for otype in ALLOWED_OUTPUT_TYPES:
            out = BoundedOutputContract.create(
                output_type=otype,
                content="test",
                confidence_basis="test_basis",
                snapshot_id="snap_001",
            )
            self.assertEqual(out.output_type, otype)

    def test_invalid_type_raises(self):
        with self.assertRaises(OutputContractViolation):
            BoundedOutputContract.create(
                output_type="hallucination",
                content="bad",
                confidence_basis="none",
                snapshot_id="snap_001",
            )

    def test_empty_type_raises(self):
        with self.assertRaises(OutputContractViolation):
            BoundedOutputContract.create(
                output_type="",
                content="bad",
                confidence_basis="none",
                snapshot_id="snap_001",
            )

    def test_allowed_types_returns_frozenset(self):
        types = BoundedOutputContract.allowed_types()
        self.assertIsInstance(types, frozenset)
        self.assertEqual(types, ALLOWED_OUTPUT_TYPES)


class TestProvenanceTracking(unittest.TestCase):
    """Every output must carry snapshot_id provenance."""

    def test_snapshot_id_present(self):
        out = BoundedOutputContract.create(
            output_type="verified_truth",
            content="test content",
            confidence_basis="lineage_ok",
            snapshot_id="snap_042",
        )
        self.assertEqual(out.snapshot_id, "snap_042")

    def test_snapshot_id_in_dict(self):
        out = BoundedOutputContract.create(
            output_type="uncertainty",
            content="maybe",
            confidence_basis="partial_lineage",
            snapshot_id="snap_099",
        )
        d = out.to_dict()
        self.assertIn("snapshot_id", d)
        self.assertEqual(d["snapshot_id"], "snap_099")

    def test_empty_snapshot_id_raises(self):
        with self.assertRaises(OutputContractViolation):
            BoundedOutputContract.create(
                output_type="insufficiency",
                content="missing",
                confidence_basis="none",
                snapshot_id="",
            )

    def test_to_dict_contains_all_fields(self):
        out = BoundedOutputContract.create(
            output_type="next_valid_action",
            content="schedule inspection",
            confidence_basis="action_derived",
            snapshot_id="snap_100",
        )
        d = out.to_dict()
        for key in ("output_type", "content", "confidence_basis", "snapshot_id"):
            self.assertIn(key, d)


if __name__ == "__main__":
    unittest.main()
