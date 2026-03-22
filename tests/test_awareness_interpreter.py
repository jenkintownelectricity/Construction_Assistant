"""Tests for AwarenessInterpreter — bounded output producer."""

import unittest

from assistant.awareness_interpreter import AwarenessInterpreter
from assistant.config import ALLOWED_OUTPUT_TYPES


class TestInterpreterProducesBoundedOutputs(unittest.TestCase):
    """Every output must be one of the four allowed types."""

    def setUp(self):
        self.interp = AwarenessInterpreter()
        self.snapshot = {
            "entries": {
                "project_alpha": {
                    "value": "active",
                    "lineage": "CRI/structural/2025-001",
                },
                "project_beta": {
                    "value": "pending",
                    # no lineage
                },
            },
            "next_actions": [
                {"action": "run_inspection", "context": "project_alpha"},
            ],
        }
        self.snapshot_id = "snap_test_001"

    def test_verified_truth_on_lineage_present(self):
        out = self.interp.interpret(self.snapshot, self.snapshot_id, "project_alpha")
        self.assertEqual(out.output_type, "verified_truth")
        self.assertIn(out.output_type, ALLOWED_OUTPUT_TYPES)

    def test_uncertainty_on_missing_lineage(self):
        out = self.interp.interpret(self.snapshot, self.snapshot_id, "project_beta")
        self.assertEqual(out.output_type, "uncertainty")
        self.assertIn(out.output_type, ALLOWED_OUTPUT_TYPES)

    def test_insufficiency_on_missing_key(self):
        out = self.interp.interpret(self.snapshot, self.snapshot_id, "unknown_key")
        self.assertEqual(out.output_type, "insufficiency")
        self.assertIn(out.output_type, ALLOWED_OUTPUT_TYPES)

    def test_insufficiency_on_empty_snapshot(self):
        out = self.interp.interpret({}, self.snapshot_id, "anything")
        self.assertEqual(out.output_type, "insufficiency")

    def test_next_valid_action(self):
        out = self.interp.interpret(self.snapshot, self.snapshot_id, "project_alpha")
        # Direct key match returns verified_truth first; query for action context
        # via a key that does not exist as an entry but matches action context
        snapshot_no_entry = {
            "entries": {},
            "next_actions": [
                {"action": "run_inspection", "context": "site_review"},
            ],
        }
        out = self.interp.interpret(snapshot_no_entry, self.snapshot_id, "site_review")
        self.assertEqual(out.output_type, "next_valid_action")
        self.assertIn(out.output_type, ALLOWED_OUTPUT_TYPES)


class TestOutputTypesExhaustive(unittest.TestCase):
    """Only four output types are ever produced."""

    def test_allowed_types_are_exactly_four(self):
        self.assertEqual(len(ALLOWED_OUTPUT_TYPES), 4)
        self.assertEqual(
            ALLOWED_OUTPUT_TYPES,
            {"verified_truth", "uncertainty", "insufficiency", "next_valid_action"},
        )

    def test_interpreter_never_returns_unlisted_type(self):
        interp = AwarenessInterpreter()
        scenarios = [
            ({"entries": {"k": {"value": "v", "lineage": "L"}}}, "k"),
            ({"entries": {"k": {"value": "v"}}}, "k"),
            ({}, "anything"),
            ({"entries": {}}, "anything"),
        ]
        for snapshot, query in scenarios:
            out = interp.interpret(snapshot, "snap", query)
            self.assertIn(
                out.output_type,
                ALLOWED_OUTPUT_TYPES,
                f"Unexpected type: {out.output_type}",
            )


if __name__ == "__main__":
    unittest.main()
