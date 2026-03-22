"""
Construction_Assistant v0.1 — AwarenessInterpreter.

Takes a frozen snapshot and a query/context, produces a bounded
interpretation.  Does NOT modify the snapshot.  Does NOT assert truth.
Maps snapshot entries to one of the allowed output types.
"""

from typing import Any, Dict

from .bounded_output_contract import BoundedOutput, BoundedOutputContract


class AwarenessInterpreter:
    """Interprets frozen awareness snapshots into bounded outputs.

    The interpreter never modifies the snapshot it receives.
    It never asserts canonical truth — it references or reports
    insufficiency.
    """

    def __init__(self) -> None:
        self._contract = BoundedOutputContract()

    def interpret(
        self,
        snapshot: Dict[str, Any],
        snapshot_id: str,
        query: str,
    ) -> BoundedOutput:
        """Produce a bounded output for *query* against *snapshot*.

        Decision logic:
        1. If snapshot is empty or missing entries  -> insufficiency
        2. If the query key exists with verified lineage -> verified_truth
        3. If the query key exists without lineage   -> uncertainty
        4. If a valid next action can be derived     -> next_valid_action
        5. Otherwise                                 -> insufficiency
        """
        if not snapshot or not isinstance(snapshot, dict):
            return self._contract.create(
                output_type="insufficiency",
                content="Snapshot is empty or invalid; cannot answer query.",
                confidence_basis="empty_snapshot",
                snapshot_id=snapshot_id,
            )

        entries = snapshot.get("entries", {})

        # Direct key lookup
        entry = entries.get(query) if entries else None
        if entry is not None and isinstance(entry, dict):
            lineage = entry.get("lineage")
            if lineage:
                return self._contract.create(
                    output_type="verified_truth",
                    content=str(entry.get("value", "")),
                    confidence_basis=f"lineage_present: {lineage}",
                    snapshot_id=snapshot_id,
                )
            return self._contract.create(
                output_type="uncertainty",
                content=str(entry.get("value", "")),
                confidence_basis="entry_exists_but_lineage_missing",
                snapshot_id=snapshot_id,
            )

        # Check for suggested next actions in the snapshot
        actions = snapshot.get("next_actions", [])
        for action in actions:
            if isinstance(action, dict) and query in action.get("context", ""):
                return self._contract.create(
                    output_type="next_valid_action",
                    content=str(action.get("action", "")),
                    confidence_basis="derived_from_snapshot_actions",
                    snapshot_id=snapshot_id,
                )

        # Default: insufficiency
        return self._contract.create(
            output_type="insufficiency",
            content=f"Awareness snapshot lacks information for query: {query}",
            confidence_basis="key_not_found",
            snapshot_id=snapshot_id,
        )
