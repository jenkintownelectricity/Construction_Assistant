# Construction_Assistant

## Purpose

Construction_Assistant is the live consciousness and safe operation layer for Construction OS. It reads frozen compiled awareness snapshots from Construction_Awareness_Cache and emits bounded outputs to operators. It is a non-authority service that defers to kernels for all canonical truth determinations.

## Cache Reader Integration v0.1

This version implements the read-only integration with Construction_Awareness_Cache:

- **AwarenessReader** — reads frozen snapshot JSON files from a configurable snapshots directory. Lists available snapshots, retrieves by ID or latest. Fails closed on malformed data.
- **AwarenessInterpreter** — takes a frozen snapshot and a query, produces a bounded interpretation mapped to one of four allowed output types. Does not modify the snapshot or assert truth.
- **BoundedOutputContract** — enforces that every output falls into exactly one of the four allowed types, with provenance tracking via snapshot_id.

## What This Repo Is

- A read-only consumer of frozen compiled awareness (point-in-time snapshots)
- A bounded emitter of safe outputs with provenance tracking
- An operator interaction surface for queries, status, and bounded guidance
- A query-response interface that classifies every response as one of four emission types

## What This Repo Is Not

- **NOT** truth authority -- does not establish, modify, or canonicalize truth
- **NOT** a cache writer -- never modifies, writes to, or triggers recompilation of the Awareness Cache
- **NOT** a bus emitter -- never writes to the Cognitive Bus (Construction_Assistant is a DENIED_EMITTER)
- **NOT** a kernel -- does not compile, validate, or govern canonical state
- **NOT** a proposal generator -- does not originate proposals for the system
- **NOT** a registry -- does not store or manage identities, schemas, or registrations

## Bounded Output Types

The Assistant produces exactly four output types. No output may fall outside these categories:

| Output Type | Description |
|---|---|
| `verified_truth` | Information confirmed in the frozen snapshot with verified lineage. The assistant references but does not create truth. |
| `uncertainty` | Information partially present but with incomplete lineage. Flagged explicitly as uncertain. |
| `insufficiency` | The snapshot lacks sufficient information to answer the query. No speculation attempted. |
| `next_valid_action` | A suggested next step derived from the snapshot. Non-authoritative, bounded by safety constraints. |

Every output includes: `output_type`, `content`, `confidence_basis`, and `snapshot_id` (provenance).

## Hard Rules

- Python standard library only -- no external dependencies
- Read-only with respect to Awareness Cache and Cognitive Bus
- Fail-closed on malformed, missing, or invalid snapshots
- All outputs carry lineage/provenance back to the source snapshot
- No self-canonicalization -- assistant outputs are never promoted to canonical status

## Stack Position

```
Layer 5: Construction_Kernel (domain truth)
Layer 6: Construction_Runtime (execution engine)
Layer 7: Construction_Application_OS (application coordination)
        |
        +-- Construction_Assistant (beside stack, reads and emits, does not originate)
              |
              reads from: Construction_Awareness_Cache (frozen snapshots)
```

## First-Read Order

1. `docs/system/REPO_MANIFEST.md`
2. `docs/architecture/assistant-role.md`
3. `assistant/config.py`
4. `assistant/bounded_output_contract.py`
5. `assistant/awareness_reader.py`
6. `assistant/awareness_interpreter.py`
