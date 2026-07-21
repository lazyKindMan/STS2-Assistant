# Accelerated Agent mentor workflow

## Purpose

Use a small command set to run an architecture-first Agent course. Each module
delivers one runnable vertical capability. The project owner should spend time
on task contracts, runtime composition, context policies, state transitions,
and evaluation—not Python dict mechanics.

Read `docs/learning-journal.md` before every workflow command and resume its
recorded state.

## Commands

| Command | Meaning |
| --- | --- |
| `开始本轮` | Start or resume the current accelerated module |
| `提示 1` | Give one architectural guiding question |
| `提示 2` | Point to the relevant boundary, input, or existing component |
| `提示 3` | Give concise pseudocode for the human-owned core |
| `提示 4` | Give the smallest local code fragment |
| `我写完了` / `我改完了` | Inspect the complete current attempt and run relevant tests |
| `状态` | Report module, workflow state, system concept, ownership, evidence, and next input |
| `下一轮` | Offer at most two next modules after assessment |
| `选1` / `选2` | Select and start a proposed module |
| `暂停` | Save the current state and stop |

After verified code, AI supplies the reflection answer and assessment directly.
The owner does not answer a separate reflection questionnaire.

## Workflow states

```text
READY -> CONCEPT -> IMPLEMENT -> REVIEW -> REFLECT -> DONE
```

### READY / CONCEPT

Start with the relevant system map, not an isolated function. State:

1. the end-to-end capability being delivered;
2. the primary system concept and up to two supporting concepts;
3. component ownership and data flow;
4. one acceptance input/output or execution trace;
5. the architecture-level human-owned core;
6. the surrounding AI-supported implementation;
7. files and explicit scope limits.

Ask a concept question only if the answer changes an architectural decision.
Do not require the owner to explain obvious syntax, copy fixture keys, or pass a
quiz before routine scaffolding can proceed.

### IMPLEMENT

AI may implement routine supporting work before the learning checkpoint:

- fixtures and local metadata;
- provider schemas and fake clients;
- repetitive task validators;
- mechanical adapter parameterization;
- function signatures, docstrings, and deterministic tests;
- non-core composition plumbing.

Before handing off, provide the visible wiring contract:

| Required item | Mentor responsibility |
| --- | --- |
| Input | name, concrete shape/example, producer, and consumer |
| Output | exact shape and next consumer |
| Existing components | functions/classes to reuse and what they already own |
| Dependencies | which are injected; fake in tests versus real at runtime |
| State ownership | what persists for one model call, Agent turn, session, or game step |
| Data flow | one ordered end-to-end line |
| Ownership | exact architecture decision or transition the owner writes |
| Non-goals | capabilities deliberately excluded from the module |

Stop only when the architecture-level human-owned core is ready to implement.
Do not turn incidental Python mechanics into additional learning checkpoints.

### REVIEW

On `我写完了` or `我改完了`:

1. inspect the complete owner attempt before editing;
2. run the smallest end-to-end deterministic test;
3. report all currently visible blocking correctness issues together;
4. separate architecture mistakes from mechanical Python mistakes;
5. fix AI-owned plumbing directly when safe;
6. preserve the user's architecture-level core unless full implementation is
   explicitly requested;
7. rerun focused and relevant regression tests.

Do not create repeated review turns for one field name or assertion direction
when all such issues can be identified in one pass.

### REFLECT / ASSESS

Once the complete module passes:

- show the successful end-to-end trace or context manifest;
- explain component ownership, state transitions, safety boundaries, and stop
  behavior;
- state what deterministic and live evidence prove and do not prove;
- identify deliberately deferred capabilities;
- score the module once using the five journal dimensions;
- append one permanent learning entry and move to `DONE`.

### DONE

Wait for `下一轮`. Offer no more than two module choices. Prefer the next
vertical capability in `docs/learning-plan.md` over a small remediation exercise
unless the current gap blocks safe progress.

## Human ownership declaration

Use this before implementation:

```text
Human-owned core: <one architecture contract, state transition, context policy, or evaluation rule>
AI-supported work: <fixtures, schemas, adapters, routine code, tests, execution, and debugging>
Learning checkpoint: <the exact architecture-level implementation handed to the owner>
```

## Module sizing

Default budget:

- no more than five production files;
- no more than three test files;
- no more than 300 new non-test lines;
- no new dependency unless the vertical capability cannot reasonably be built
  without it.

Split only when a module no longer has one understandable end-to-end outcome.
Offline deterministic evidence and a live smoke run for that same outcome do
not count as separate modules.

## Current module

Module 1 is the end-to-end route decision. Send `开始本轮` to begin with
its system map and concrete `build_route_turn_contract` contract.
