# STS2 Agent accelerated learning plan

## Goal

Build an inspectable Slay the Spire 2 Agent that can choose legal card rewards
and reachable map nodes from fresh game state, explain its decision, expose an
auditable trace, and eventually execute one action through a safe game
boundary.

The curriculum teaches how a complete Agent system is assembled. Python dict
plumbing, fixture mechanics, and repetitive test syntax are supporting work,
not the main learning target.

## Curriculum pivot — 2026-07-21

The original plan established useful boundaries but split them into too many
small lessons. Recent rounds spent more time correcting field names and single
assertions than reasoning about Agent architecture. The remaining curriculum
therefore changes from micro-slices to end-to-end modules.

The completed work is preserved. The new plan changes sequencing and ownership:

- one module delivers one runnable vertical capability;
- related offline and live evidence belong to the same module;
- the owner writes an architecture contract, state transition, context policy,
  or evaluation rule rather than routine data-access code;
- AI supplies fixtures, schemas, fake providers, repetitive validation,
  mechanical Python, and tests unless one of those is the learning concept;
- review reports all currently visible blocking issues together;
- assessment happens once per completed module.

Systematic Agent learning does not mean adding every fashionable capability.
Multi-agent orchestration, RAG, vector databases, GUI automation, OCR, and RL
remain deferred until the runtime has a concrete need for them.

## Target system

```text
manual fixture or GameGateway
  -> fresh StateSnapshot
  -> Observation + LegalActions
  -> task-specific TurnContract
       instructions
       provider tool schemas
       executable guarded tools
       final-output schema and validator
  -> AgentRuntime
       context selection
       provider call
       tool transition loop
       stop/limit/recovery policy
  -> Decision + Trace
  -> Evaluator
  -> optional safe execution
       re-observe -> revalidate -> execute -> re-observe
```

The important boundaries are:

- **GameGateway** owns external reads and actions.
- **Observation normalizer** converts raw state to current bounded facts.
- **Legal-action enumerator** is authoritative for immediate choices.
- **Turn contract** supplies only the instructions, schemas, tools, and
  validators relevant to one task.
- **Context policy** selects fresh observation, useful tool results, and
  optional session intent without accumulating stale state.
- **Provider adapter** translates vendor requests and responses.
- **Agent runtime** performs model/tool transitions and stops within a budget.
- **Guards** validate tool requests and final actions before side effects or
  return.
- **Trace evaluator** measures protocol behavior separately from strategy
  quality.

## Completed foundation

| Capability | Agent knowledge already practiced | Evidence |
| --- | --- | --- |
| Manual card choice | observation, policy, dynamic legal actions | deterministic legal decision |
| Provider-neutral loop | tool request, tool result, next model turn, stop | inspectable trace |
| OpenAI adapter | provider boundary and structured response normalization | fake and live API runs |
| Card vertical slice | end-to-end composition | legal card decision plus trace |
| Safety gates | capability allowlist, tool arguments, final action | invalid requests rejected before use |
| Turn isolation | provider context lifecycle | independent request sequence test |
| Route observation | full topology versus current action space | reachable-node test |

These are real Agent components. The missing learning value is their assembly
into a configurable runtime and their operation across more than one task.

## Accelerated modules

### Module 1 — End-to-end route decision (current)

Primary concept: **vertical Agent composition**.

Supporting concepts: task-specific tool contract and final-action safety.

User-visible behavior:

```text
manual map snapshot
  -> route observation
  -> model may inspect one reachable path
  -> guarded local route tool result
  -> model returns one reachable node and reason
  -> decision + trace
```

One entry point must accept either a fake Responses client or the real OpenAI
client. The deterministic test and one optional live smoke run verify the same
behavior; they are not separate lessons.

Acceptance:

- trace contains `observation -> tool_call -> tool_result -> final`;
- the requested `node_id` is currently reachable;
- the final `choice` is in `reachable_node_ids`;
- a route turn cannot see or execute `get_card_facts`;
- no game action is executed.

Human-owned core:

`build_route_turn_contract` — compose the route instructions, route tool
schema, guarded executable tool, final-output schema, and final validator into
one explicit concrete contract. The surrounding provider parameterization,
route tool implementation, fake client, entry point, and tests are AI-supported.

Expected change budget: at most five production files, three test files, 300
new non-test lines, and no new dependency.

### Module 2 — Unified card/route Agent runtime

Primary concept: **runtime task assembly**.

Card and route become the two concrete usages from which a small shared
`TurnSpec`/`TurnContract` shape can be extracted. The Agent loop remains
provider-neutral.

Acceptance:

- `run_decision("card", ...)` and `run_decision("route", ...)` share one
  runtime path;
- each task exposes only its own instructions, tools, schemas, and validators;
- adding a task changes task assembly, not the loop;
- existing card and route traces remain inspectable.

Human-owned core: the task-selection and runtime-assembly transition.

### Module 3 — Context and session state

Primary concept: **context engineering**.

Supporting concepts: state ownership and bounded memory.

Explicitly separate:

- fresh game observation, replaced every decision;
- current Agent-turn events, retained only through that tool loop;
- provider response correlation, owned by one adapter instance;
- optional route intent, retained across map steps but never authoritative over
  fresh legal actions.

Acceptance: a context manifest shows what was included or omitted; stale
observation and stale legal actions cannot survive into the next decision.

Human-owned core: `build_model_context`, including the selection and omission
rule.

### Module 4 — Evaluation and bounded recovery

Primary concept: **Agent evaluation**.

Supporting concepts: bounded autonomy and error recovery.

Build one scenario runner that produces a compact report for normal and failure
cases instead of treating every failure as a separate course round.

Required scenarios:

- legal tool-assisted final decision;
- unknown or out-of-scope tool request;
- malformed final event;
- repeated tool calls reaching the configured limit;
- one selected transient provider failure within a fixed retry budget.

Protocol correctness and strategy quality remain separate scores.

Human-owned core: the evaluation verdict policy that maps trace/outcome evidence
to pass, fail, or explicit terminal error.

### Module 5 — Game gateway and playable MVP

Primary concept: **environment interaction state machine**.

Inspect the available game boundary first, then choose direct HTTP or MCP; do
not implement both. Preserve manual fixtures and a fake gateway for tests.

Runtime transition:

```text
observe fresh state
  -> classify supported decision type
  -> run Agent decision
  -> re-observe
  -> revalidate against fresh legal actions
  -> execute one action
  -> observe resulting state
```

Card and route execution are added as sequential safety checkpoints inside the
module, never as one unreviewed bulk change.

Human-owned core: the application state transition that decides whether to
read, decide, revalidate, execute, or stop.

## Module workflow

```text
SYSTEM MAP
  -> show component ownership and one end-to-end acceptance trace
CONTRACT
  -> owner designs or predicts the architecture-level rule
BUILD
  -> AI scaffolds routine code/tests; owner implements the core
REVIEW
  -> inspect the full attempt and report all visible blocking issues together
VERIFY
  -> deterministic suite + trace; live smoke when the same module needs it
ASSESS
  -> AI supplies reflection, scores the module, updates the journal
```

A concept question is used only when it tests an architectural decision. It is
not a gate for obvious syntax or fixture access. Reflection is always supplied
by AI after verification.

## Evidence and assessment

Every module ends with:

1. one runnable end-to-end example;
2. deterministic tests for its contract and important failure boundary;
3. an inspectable trace or context manifest where relevant;
4. a statement of what the evidence proves and does not prove;
5. one five-dimension assessment recorded in the learning journal.

Live API evidence demonstrates provider integration but never replaces
deterministic tests. A legal action proves safety for covered inputs, not
strategic quality.

## Deferred capabilities

Combat, shops, events, relic decisions, broad card ingestion, persistent
self-editing memory, multi-agent delegation, background workers, cron, RAG,
vector databases, MCTS, RL, OCR, and unattended game automation remain outside
the accelerated MVP unless explicitly selected later.

## Immediate next command

Send `开始本轮` to begin Module 1. The first step is a system map and
the concrete `build_route_turn_contract` wiring contract, followed by one
owner architecture decision rather than a Python field-access exercise.
