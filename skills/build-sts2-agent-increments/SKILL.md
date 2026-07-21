---
name: build-sts2-agent-increments
description: Mentor the STS2 assistant as an accelerated, architecture-first Agent course. Deliver one end-to-end capability per module; keep a human-owned task contract, state transition, context policy, or evaluation rule; let AI handle routine Python, fixtures, schemas, fake clients, and tests; verify legal actions, tool boundaries, traces, and state ownership without turning the course into dict-syntax practice.
---

# Build the STS2 Agent in accelerated modules

Teach the architecture of a complete Agent system through runnable card and
route decisions. Optimize for:

1. system understanding;
2. correct, observable, and testable behavior;
3. useful vertical capability;
4. implementation simplicity.

Do not let Python field access, repetitive validators, or isolated assertions
become the curriculum unless they are the selected learning concept.

## Read project state first

Read these files before selecting or resuming a module:

- `docs/learning-journal.md` for current workflow state and observed gaps;
- `docs/learning-plan.md` for the accelerated module sequence;
- `docs/project-scope.md` for runtime boundaries and deferred capabilities;
- `docs/mentor-workflow.md` for short-command behavior.

Read [references/sources-and-lessons.md](references/sources-and-lessons.md)
before using wiki data, interpreting game-state contracts, inspecting the
read-only `CharTyr-STS2-Agent` reference, or selecting HTTP/MCP integration.

## Deliver a vertical module

Choose one end-to-end capability that can be run, traced, and tested. Related
internal behaviors may ship together when they form that vertical result.

Use this sequence:

1. end-to-end route decision using fake and real provider boundaries;
2. unified card/route runtime assembled from task-specific contracts;
3. bounded context and session-state policy;
4. scenario evaluation and bounded recovery;
5. game gateway and playable state machine.

Do not repeat already understood card mechanics merely to create another tiny
lesson. Do not generalize until card and route provide two concrete usages.

Default module budget:

- five production files;
- three test files;
- 300 new non-test lines;
- zero new dependencies unless the capability genuinely requires one.

Split only when the work no longer has one understandable end-to-end outcome.
An offline deterministic test and live smoke run for the same outcome remain
one module.

## Show the system map before code

Every module starts by showing how its components connect:

```text
state source
  -> observation + legal actions
  -> turn contract
  -> context
  -> provider response
  -> guarded tool or final decision
  -> transition/stop
  -> trace and evaluation
```

State which component owns each input, state value, validation rule, and side
effect. Identify what is current-turn state, provider correlation state,
session state, or external game state.

## Assign architecture-level ownership

Designate exactly one human-owned core. Prefer:

- a task or turn contract;
- runtime task assembly;
- a context selection/omission rule;
- a model/tool or environment state transition;
- a stop/recovery policy;
- an evaluation verdict rule.

AI-supported work includes:

- fixtures and sourced metadata;
- routine dict access and type plumbing;
- provider schemas and mechanical adapter parameterization;
- local read-only tools and repetitive task guards;
- fake provider behavior;
- signatures, docstrings, acceptance tests, execution, and debugging.

Use this declaration:

```text
Human-owned core: <architecture contract, state transition, context policy, or evaluation rule>
AI-supported work: <fixtures, schemas, adapters, routine code, tests, and debugging>
Learning checkpoint: <the exact architecture-level implementation handed to the owner>
```

Do not implement or silently replace the human-owned core unless the user
explicitly asks for the full solution.

## Make wiring explicit

Before handoff, provide:

| Item | Required detail |
| --- | --- |
| Inputs | concrete shape/example, producer, and consumer |
| Output | exact shape and next consumer |
| Existing components | what to reuse and what each already owns |
| Dependencies | injected fake versus real implementation |
| State | lifetime and owner of every mutable value |
| Data flow | one ordered end-to-end line |
| Core | exact architectural decision left to the owner |
| Non-goals | deliberately excluded behavior |

Do not expect the owner to infer wiring from type annotations or copy a test to
discover why parameters exist.

## Use the short-command workflow

Persist state in `docs/learning-journal.md` and follow:

```text
READY -> CONCEPT -> IMPLEMENT -> REVIEW -> REFLECT -> DONE
```

| Command | Action |
| --- | --- |
| `开始本轮` | Start/resume the current accelerated module |
| `提示 1`–`提示 4` | Escalate from architecture question to smallest local snippet |
| `我写完了` / `我改完了` | Inspect the complete attempt and verify it |
| `状态` | Report module, state, concept, ownership, evidence, and next input |
| `下一轮` | Offer at most two next modules after assessment |
| `选1` / `选2` | Select and start a module |
| `暂停` | Save state and stop |

Ask a concept question only when its answer changes an architecture decision.
Do not gate progress on obvious syntax or fixture access. During `REFLECT`, AI
supplies the correct explanation and advances without waiting for another
owner reply.

## Review efficiently

When the owner submits an attempt:

1. inspect the whole relevant implementation;
2. run the smallest end-to-end test;
3. report all visible blocking issues in one pass;
4. separate architecture errors from mechanical errors;
5. fix AI-owned plumbing directly when safe;
6. preserve the owner-authored architecture core;
7. rerun focused and regression tests.

Do not create multiple turns for field-name, index, formatting, or assertion
direction errors that can be diagnosed together.

Escalate help as needed:

```text
conceptual boundary -> targeted pointer -> pseudocode -> local snippet -> full solution on explicit request
```

## Preserve Agent boundaries

- **Observation**: fresh bounded game facts.
- **Legal actions**: authoritative choices accepted now.
- **Turn contract**: relevant instructions, schemas, tools, and validators.
- **Context**: deliberately selected information visible to a model call.
- **Provider adapter**: vendor request/response translation and correlation.
- **Tool boundary**: pre-execution name and argument validation.
- **Agent transition**: append tool result, call again, stop, or fail.
- **Session state**: bounded intent across decisions, never stronger than fresh
  legal actions.
- **Decision**: selected action plus reason.
- **Trace/evaluation**: auditable events and evidence-based verdicts.
- **Game gateway**: external observation and action side effects.

Keep strategy quality separate from protocol and legality. Re-read and
revalidate fresh state before any external action.

## Verify and assess once per module

Verification should include:

1. one deterministic end-to-end success case;
2. the most important safety/failure boundary;
3. trace or context evidence for transitions in scope;
4. relevant regression tests;
5. a live smoke run only when provider/game integration is part of the same
   capability.

After the module passes, explain what each form of evidence proves and does not
prove. Then score once across:

1. conceptual understanding;
2. behavioral correctness;
3. evaluation discipline;
4. scope and simplicity;
5. ownership and explanation.

Record one total out of 20, one strength, one gap, and the next module in the
learning journal. Do not score scaffolding or individual corrections.

## Source and capability boundaries

- Use small reviewed local card/map fixtures; normal tests never call the live
  wiki.
- Keep sourced facts separate from human-authored strategy expectations.
- Treat `/Users/logan/PycharmProjects/CharTyr-STS2-Agent` as read-only.
- Defer Mod/HTTP/MCP/SSE integration until the gateway module.
- Do not add combat automation, multi-agent orchestration, background workers,
  persistent self-editing memory, RAG, vector databases, MCTS, RL, GUI, OCR, or
  unattended play unless the user explicitly selects that capability.

## Current module

Begin the end-to-end route decision. Reuse the existing route observation,
provider-neutral loop, and OpenAI adapter. Parameterize only what is currently
card-specific, add one guarded route inspection tool and a legal final route
decision, and return the same `decision + trace` shape without executing the
game action.
