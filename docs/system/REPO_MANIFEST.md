# REPO MANIFEST: Construction_Assistant

## Identity

- **Repo Name:** Construction_Assistant
- **Organization:** jenkintownelectricity
- **Layer:** Cognitive Layer
- **Primary Role:** Live consciousness / safe operation

## Purpose

Construction_Assistant is the live consciousness and safe operation layer for Construction OS. It serves as the operator-facing surface that reads compiled awareness, enforces safety boundaries, and emits bounded outputs to support safe, auditable interaction with the system.

## Classification

- **Service Type:** Cognitive-layer service
- **Authority Status:** Non-authority
- **Operational Mode:** Reads truth-derived awareness but defers to kernels for all canonical truth determinations

## v0.1 Components — Cache Reader Integration

### assistant/config.py
Configuration constants: snapshot directory paths (configurable via environment), allowed output types, snapshot file extension, reader schema version, and read-only path declarations.

### assistant/awareness_reader.py
**AwarenessReader** — Read-only reader of frozen awareness snapshot JSON files. Provides: `list_snapshots()`, `get_latest_snapshot_id()`, `get_snapshot(id)`, `get_latest_snapshot()`. Fails closed on malformed JSON, non-object payloads, missing files. Contains no write methods.

### assistant/awareness_interpreter.py
**AwarenessInterpreter** — Takes a frozen snapshot and a query, produces a bounded output. Maps snapshot entries to one of four allowed output types based on entry presence, lineage completeness, and available next actions. Never modifies the snapshot. Never asserts canonical truth.

### assistant/bounded_output_contract.py
**BoundedOutputContract** and **BoundedOutput** — Enforces that every assistant output is one of: `verified_truth`, `uncertainty`, `insufficiency`, `next_valid_action`. Every output carries provenance (`snapshot_id`), content, and confidence basis. Raises `OutputContractViolation` on invalid type or missing provenance.

### tests/
- `test_awareness_reader.py` — Tests snapshot listing, loading, fail-closed on malformed data, read-only enforcement (no write methods exist)
- `test_awareness_interpreter.py` — Tests bounded output production, all four output types exercised, no unlisted types produced
- `test_bounded_output.py` — Tests contract enforcement, provenance tracking, type validation

## What It IS

- Live consciousness / safe operation layer for Construction OS
- Reader of frozen compiled awareness (point-in-time snapshots)
- Bounded emitter of safe outputs (verified_truth, uncertainty, insufficiency, next_valid_action)
- Operator interaction surface for queries, status, and bounded guidance

## What It IS NOT

- **NOT** truth authority -- does not establish, modify, or canonicalize truth
- **NOT** the primary proposal generator -- does not originate proposals for the system
- **NOT** a kernel -- does not compile, validate, or govern canonical state
- **NOT** a registry -- does not store or manage identities, schemas, or registrations
- **NOT** the cognitive bus -- does not route, broker, or transport messages between services

## Interactions with Other Repos

### Construction_Kernel
The assistant defers to Construction_Kernel as the canonical truth authority. All awareness consumed by the assistant originates from truth compiled or validated by the kernel. The assistant never overrides, contradicts, or bypasses kernel determinations.

### Construction_Awareness_Cache
The assistant is the primary reader of Construction_Awareness_Cache. It operates on frozen compiled awareness snapshots produced by the cache. The assistant reads only -- it does not write to, modify, or trigger compilation within the cache. If a snapshot is invalid or absent, the assistant fails closed.

### Construction_Workers
The assistant does not direct workers. Worker outputs reach the assistant indirectly through the cognitive bus and awareness compilation pipeline. The assistant has no command or scheduling authority over worker execution.

### Construction_CRI (Canonical Resource Index)
The assistant accesses CRI indirectly through compiled awareness. It does not query CRI directly or modify any canonical resource entries. CRI state is reflected in awareness snapshots that the assistant reads.

### Construction_Cognitive_Bus
The assistant receives awareness and context through the cognitive bus but does not act as the bus itself. It is a consumer endpoint, not a routing or brokerage service. Construction_Assistant is listed as a DENIED_EMITTER in the bus configuration.

### Construction_Proposals
The assistant is not the primary proposal generator. It may surface proposal-related information from compiled awareness but does not originate, approve, or modify proposals. Proposal lifecycle is governed by other system components.

## Non-Authority Guarantees

1. **No canonical truth:** The assistant never establishes or claims canonical truth. All truth statements are sourced from compiled awareness with preserved lineage.
2. **Reads frozen awareness only:** The assistant operates exclusively on point-in-time frozen snapshots. It does not interact with live compilation or mutable state.
3. **Fail-closed on insufficiency:** When awareness is insufficient, invalid, or absent, the assistant emits an insufficiency signal and halts further output rather than speculating or fabricating.
4. **Lineage preservation:** Every output emitted by the assistant carries lineage tracing back to its source in compiled awareness, ensuring full auditability.
