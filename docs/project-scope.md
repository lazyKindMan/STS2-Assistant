# STS2 Agent learning scope

## Project purpose

Build a Slay the Spire 2 assistant as a concrete environment for learning the
architecture of a complete Agent system:

- fresh state and bounded observations;
- dynamic legal actions;
- task-specific instructions, tools, and output contracts;
- provider calls and model/tool state transitions;
- context selection and session state;
- validation, traces, evaluation, and bounded recovery;
- safe interaction with an external game boundary.

Card and route strategy provide realistic inputs, but Python syntax practice
and maximum win rate are not the curriculum.

## Runtime target

```text
GameGateway or manual fixture
  -> StateSnapshot
  -> Observation + LegalActions
  -> TurnContract
  -> AgentRuntime(model <-> guarded tools)
  -> Decision + Trace
  -> Evaluator
  -> optional revalidate-and-execute boundary
```

The owner should eventually be able to explain:

1. which component owns each piece of state;
2. how a task selects instructions, tools, schemas, and validators;
3. why an Agent turn may contain several provider calls;
4. how context changes after a tool result;
5. what limits autonomy and rejects stale or invented actions;
6. what deterministic tests, live calls, and traces each prove;
7. how the Agent re-observes before an external action.

## Accelerated curriculum

The detailed contract is in `docs/learning-plan.md`.

```text
completed card runtime and route observation
  -> Module 1: end-to-end route decision
  -> Module 2: unified card/route runtime
  -> Module 3: context and session state
  -> Module 4: evaluation and bounded recovery
  -> Module 5: game gateway and playable MVP
```

Each module delivers one vertical capability. Related fake-provider tests and
real-provider smoke evidence stay together. Assessment occurs once after the
module works.

## Human and AI ownership

Every module reserves one architecture-level human-owned core. Preferred cores
are:

- a concrete task/turn contract;
- runtime task assembly;
- context-selection or omission policy;
- an Agent/environment state transition;
- bounded recovery or evaluation verdict logic.

AI owns routine fixture access, schemas, mechanical adapter changes, fake
providers, repetitive validators, tests, test execution, and Python syntax
debugging unless one of those is the current learning concept.

The learning checkpoint must not be a field-name transcription exercise.

## Current boundary

The completed repository already contains:

- one provider-neutral model/tool loop;
- an OpenAI Responses adapter;
- a tested and live card decision entry point;
- card tool and final-action safety gates;
- independent-turn provider context isolation;
- a route observation with complete topology and current reachable nodes.

The current module is an end-to-end route decision. It may parameterize the
currently card-specific provider request, add one local route tool, compose a
fake/real route entry point, and validate the final reachable node. It does not
execute a game action.

## External references and test data

- Use the STS2 wiki only to create small reviewed local fact snapshots; normal
  tests never depend on the live wiki.
- Keep source facts separate from human-authored strategy expectations.
- Treat `/Users/logan/PycharmProjects/CharTyr-STS2-Agent` as a read-only
  contract reference.
- Borrow its state/action separation and fresh-state discipline, not its full
  Mod, HTTP, MCP, SSE, planner handoff, or persistent knowledge architecture.

## Deferred capabilities

Combat, shops, events, relic choices, broad knowledge ingestion, persistent
self-editing memory, multi-agent orchestration, background workers, cron, RAG,
vector databases, MCTS, RL, GUI/OCR automation, and unattended play remain out
of scope until the five accelerated modules create a concrete need.

## Definition of done for a module

A module is complete only when:

1. its vertical behavior runs end to end;
2. deterministic tests cover the main contract and safety boundary;
3. the relevant trace or context manifest is inspectable;
4. every returned action is legal for the supplied fresh observation;
5. component and state ownership can be explained plainly;
6. evidence limits and deferred capabilities are explicit;
7. the learning journal contains one module-level assessment.
