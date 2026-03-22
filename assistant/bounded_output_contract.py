"""
Construction_Assistant v0.1 — BoundedOutputContract.

Defines and enforces the ONLY output types the Assistant may produce.
Every output carries provenance (snapshot_id) and a confidence basis.
"""

from typing import Any, Dict

from . import config


class OutputContractViolation(Exception):
    """Raised when an output violates the bounded output contract."""


class BoundedOutput:
    """A single bounded output produced by the Assistant.

    Attributes:
        output_type:      One of the four allowed types.
        content:          The payload of the output.
        confidence_basis: Why the assistant has this confidence level.
        snapshot_id:      Provenance — which snapshot this derives from.
    """

    __slots__ = ("output_type", "content", "confidence_basis", "snapshot_id")

    def __init__(
        self,
        output_type: str,
        content: str,
        confidence_basis: str,
        snapshot_id: str,
    ) -> None:
        if output_type not in config.ALLOWED_OUTPUT_TYPES:
            raise OutputContractViolation(
                f"Invalid output type '{output_type}'. "
                f"Allowed: {sorted(config.ALLOWED_OUTPUT_TYPES)}"
            )
        if not snapshot_id:
            raise OutputContractViolation(
                "snapshot_id (provenance) is required on every output"
            )
        self.output_type = output_type
        self.content = content
        self.confidence_basis = confidence_basis
        self.snapshot_id = snapshot_id

    def to_dict(self) -> Dict[str, Any]:
        return {
            "output_type": self.output_type,
            "content": self.content,
            "confidence_basis": self.confidence_basis,
            "snapshot_id": self.snapshot_id,
        }

    def __repr__(self) -> str:
        return (
            f"BoundedOutput(type={self.output_type!r}, "
            f"snapshot={self.snapshot_id!r})"
        )


class BoundedOutputContract:
    """Factory that enforces bounded output creation rules."""

    @staticmethod
    def create(
        output_type: str,
        content: str,
        confidence_basis: str,
        snapshot_id: str,
    ) -> BoundedOutput:
        """Create a validated BoundedOutput.  Raises on violation."""
        return BoundedOutput(output_type, content, confidence_basis, snapshot_id)

    @staticmethod
    def allowed_types() -> frozenset:
        return config.ALLOWED_OUTPUT_TYPES
