# Agent development learning journal

## Purpose

Keep a durable record of what the project owner learned while building the STS2 Agent assistant. Read this file before each learning iteration and update it only after reviewing a meaningful owner-authored attempt.

Scores measure progress against the current milestone. They do not measure personal ability or production readiness.

## Current status

- Current milestone: Accelerated Module 1 — end-to-end route decision
- Status: ready
- Workflow state: `READY`
- Active iteration: compose one complete route vertical slice with fake and real provider boundaries
- Next expected input: `开始本轮`
- Primary concept focus: vertical Agent composition (supported by task-specific tool contract and final-action safety)
- Human-owned core: `build_route_turn_contract`
- Latest score: 18/20 (Phase 2A)

## Accelerated curriculum pivot — 2026-07-21

- Owner feedback: progress felt slow and the micro-slice sequence did not make
  the architecture of a complete Agent system visible enough.
- Evidence: recent rounds spent multiple review turns on fixture field names,
  list indices, and assertion direction after the underlying Agent boundary was
  already understood.
- Decision: replace the remaining Phase 2B–6 micro-slices with five vertical
  modules: route decision, unified runtime, context/session state,
  evaluation/recovery, and game gateway/MVP.
- Ownership change: reserve owner work for task contracts, runtime assembly,
  context policies, state transitions, and evaluation verdicts. AI owns routine
  Python, schemas, fixtures, fake clients, repetitive validators, and tests.
- Review change: report all visible blocking issues in one pass and assess only
  after a complete module, not after mechanical corrections.
- Evidence change: deterministic tests and a live smoke run for the same
  behavior stay in one module.
- Current module acceptance: a manual route snapshot produces a reachable
  route decision and trace through one guarded route tool, using the same entry
  point with a fake or real OpenAI client and executing no game action.

## Curriculum alignment — 2026-07-17

- Owner goal: learn Agent harness programming while building an STS2 assistant
  that eventually chooses cards and map routes from current game state.
- Reference: `/Users/logan/PycharmProjects/learn-claude-code` supplies the
  teaching pattern “keep one Agent loop; add one harness mechanism per lesson.”
- Decision: adopt its loop, tool, permission, context, prompt, recovery, and
  optional external-tool lessons; defer subagents, teams, background tasks,
  cron, worktrees, and other mechanisms unrelated to the first playable
  assistant.
- Ordered curriculum: `docs/learning-plan.md`.
- Immediate prerequisite: the owner personally composes and runs the real card
  decision entry point before protocol validation, route choice, or game
  integration begins.

## Curriculum pivot — 2026-07-16

- Owner feedback: Milestone 1 spent too much learning time on Python dict and
  branch mechanics, so the Agent runtime was not visible enough.
- Decision: preserve Milestone 1 as observation/legal-action groundwork, but do
  not expand card scoring or its evaluation set now.
- New direction: learn an inspectable Agent loop in this order: one offline
  tool turn, one real model-backed turn, explicit context lifecycle, then trace
  evaluation and safety.
- Ownership change: AI scaffolds routine Python data access, fixtures, the
  scripted model, and tool implementation. The owner writes the state
  transition that recognizes a tool request, executes an allowed tool, appends
  the result to context, and continues or stops.
- Next acceptance evidence: exactly two scripted model turns, one validated
  `get_card_facts` call, one appended tool result, and one legal final decision
  in the execution trace.

## Assessment rubric

Score each dimension from 0 to 4, for a total out of 20:

| Dimension | What counts as evidence |
| --- | --- |
| Conceptual understanding | The owner explains context, model response, tool boundary, state transition, and the neighboring concepts currently in scope |
| Behavioral correctness | Owner-written Agent logic validates allowed tool calls, feeds results into the next turn, stops correctly, and returns only legal actions |
| Evaluation discipline | Deterministic tests and traces support claims about model turns, tool calls, context changes, stop conditions, and failure cases |
| Scope and simplicity | A small direct solution without premature abstractions |
| Ownership and explanation | The owner can explain, modify, and defend the Agent transition or context rule they wrote; routine Python scaffolding is not treated as owner evidence |

Do not score deliberately deferred capabilities. Identify which evidence came from owner-written work and which came from AI scaffolding.

## Learning entries

### 2026-07-21 — Phase 2A: route observation and legal actions

- Primary concept: observation boundary
- Supporting concept: dynamic legal action space
- Human-owned code: `build_route_observation`, which preserves player facts
  and full map topology while deriving `reachable_node_ids` from the current
  node's outgoing edges
- AI-supported work: synthetic map fixture, function signature and docstring,
  explicit parameter/source/consumer contract, deterministic acceptance test,
  field-name diagnosis, test execution, and reference reflection
- Behavior and test evidence: the route test passed with all four nodes visible
  while only `elite_1` and `shop_1` were reachable from `start`; `rest_2`
  remained visible for future planning but was absent from the current legal
  actions; all ten project tests passed

| Dimension | Score (0-4) | Evidence |
| --- | ---: | --- |
| Conceptual understanding | 4 | Owner correctly explained that a future rest node belongs in the observation but cannot be selected on the current step. |
| Behavioral correctness | 4 | Owner's final function retained character, HP, act, current node, and the full node list, then derived exactly the current node's outgoing IDs. |
| Evaluation discipline | 3 | A deterministic test separately checked player facts, visible topology, reachable IDs, and exclusion of a future node; the test and fixture were AI-authored and cover one valid map shape. |
| Scope and simplicity | 4 | The implementation is one direct state transformation with no route policy, provider code, registry, or premature shared abstraction. |
| Ownership and explanation | 3 | Owner implemented the whole transformation from the contract and preserved its structure, but needed exact corrections to distinguish top-level `current_node_id` from node-level `outgoing_node_ids` and to use the fixture's `id` field. |

- Total: 18/20
- Demonstrated strength: kept planning context (`nodes`) separate from the
  immediate action boundary (`reachable_node_ids`) instead of hiding future
  topology or making every visible node selectable.
- Concept gap or uncertainty: exposing a bounded action set does not yet
  enforce that a model's final route decision belongs to it; final-action
  validation remains a later route decision boundary.
- Reference reflection: observations may be richer than actions because an
  Agent needs future consequences to reason, while the environment accepts
  only immediately reachable actions. The test proves state shaping for one
  valid manual snapshot; it does not prove route quality, malformed-map
  handling, or live-game integration.
- Next exercise: Phase 2B, run one offline route tool turn in which a scripted
  model inspects a reachable path, consumes the tool result, and returns a
  reachable node using the existing provider-neutral Agent loop.
- What would raise the target score by one point: add an owner-authored second
  fixture where the current node changes and show that `reachable_node_ids`
  changes while full topology remains available.

### 2026-07-21 — Phase 1D: independent-turn context isolation

- Primary concept: context lifecycle
- Supporting concept: state ownership
- Human-owned code: regression assertions in
  `test_two_independent_turns_start_with_fresh_provider_context`, proving that
  the first request of each independent turn has no `previous_response_id`
  while the second request continues from that same turn's first response
- AI-supported work: identified `OpenAIResponsesModel` as the owner of provider
  conversation state, adjusted `FakeResponses` to represent two complete
  turns, supplied the four-request acceptance contract, reviewed incomplete
  and inverted assertions, and ran deterministic verification
- Behavior and test evidence: the owner-authored test observed exactly four
  requests; requests zero and two had no previous response ID, request one
  referenced `resp-live-1`, and request three referenced `resp-live-3`; the
  focused test and all five live-decision tests passed

| Dimension | Score (0-4) | Evidence |
| --- | ---: | --- |
| Conceptual understanding | 3 | Owner predicted that independent decisions must not share context; the mentor supplied the more exact mechanism that function calls are not inherently isolated and isolation comes from constructing a fresh state-owning adapter. |
| Behavioral correctness | 4 | The final four-request assertions accurately cover both within-turn continuation and between-turn reset against the existing implementation. |
| Evaluation discipline | 3 | Owner authored the regression assertions and corrected a test that first passed with missing evidence, then failed because of an inverted expectation; the test does not distinguish two different observation payloads or inspect trace-object identity. |
| Scope and simplicity | 4 | No production reset API or abstraction was added because the existing adapter lifecycle already provides the required boundary. |
| Ownership and explanation | 3 | Owner supplied the core assertions and the high-level isolation explanation, but needed targeted corrections for complete request-count evidence, the fourth request index, and equality direction. |

- Total: 17/20
- Demonstrated strength: tested both halves of the lifecycle rule instead of
  treating context isolation as disabling `previous_response_id` everywhere.
- Concept gap or uncertainty: sharing an API client is safe here only because
  conversation state belongs to a newly created adapter; hoisting that adapter
  into shared application state would change the result. The current test
  proves provider-ID isolation, not that two distinct observation payloads or
  returned traces cannot be mixed.
- Reference reflection: retain `previous_response_id` for the model/tool/model
  sequence inside one Agent turn, then discard it when a new independent game
  decision begins. A client is a transport dependency, not automatically a
  conversation. The absence of a production change is meaningful evidence
  that the existing composition boundary is already correct.
- Next exercise: Phase 2A, define a manual route observation that separates
  full map topology from the smaller dynamic legal action set
  `reachable_node_ids`.
- What would raise the target score by one point: use two distinguishable
  observation fixtures and assert that turn two's first request contains only
  the second observation while both returned traces remain independently
  bounded.

### 2026-07-21 — Phase 1C: tool-request gate

- Primary concept: pre-execution tool boundary
- Supporting concept: generic capability allowlist versus task-specific
  argument validation
- Human-owned code: `validate_tool_request`, which rejects tool names outside
  the card task and rejects `card_id` values outside the current
  `offered_card_ids` before returning validated arguments
- AI-supported work: explicit parameter/source/consumer contract, generic
  registry membership check in `run_agent_turn`, guarded card-tool wrapper,
  fake responses and mock-handler tests, test execution, design discussion, and
  reference reflection
- Behavior and test evidence: all four live-decision tests and both Agent-loop
  tests passed; unknown tools raised before dispatch, `card_x` raised before
  `get_card_facts`, the mocked handler was not called, and a legal tool request
  still completed the full model/tool/final turn

| Dimension | Score (0-4) | Evidence |
| --- | ---: | --- |
| Conceptual understanding | 4 | Owner explained why validation must happen before handler execution, identified missing-tool and invalid-argument failures, and challenged premature hardcoding by asking when a generic validator or decorator would be justified. |
| Behavioral correctness | 4 | Owner's validator rejected disallowed names and out-of-scope card IDs, returned valid arguments unchanged, and preserved the successful Agent turn. |
| Evaluation discipline | 3 | Deterministic tests separately covered registry rejection, task argument rejection, no handler execution, and the legal happy path; tests remained AI-authored and malformed argument shapes were not evaluated. |
| Scope and simplicity | 4 | Owner kept two direct checks and deferred decorator/registry abstraction until a second route-tool use case exists. |
| Ownership and explanation | 4 | Owner implemented the complete core on the first attempt from the visible contract and defended an alternative generic design with a relevant trade-off question. |

- Total: 19/20
- Demonstrated strength: distinguished a reusable capability boundary from a
  dynamic STS2 argument rule and ensured rejection occurs before side effects.
- Concept gap or uncertainty: the current evidence does not cover missing,
  extra, or wrong-type arguments; a generic validator interface should wait for
  the route tool to reveal the second concrete rule.
- Next exercise: isolate two independent Agent turns so a second decision does
  not inherit the first turn's `previous_response_id`, observation, or tool
  result.
- What would raise the target score by one point: add one owner-authored test
  for a malformed argument shape and explain the exact pre-execution claim it
  supports.
- Mentor preference: after verified code, AI now supplies the reference
  reflection and advances without requiring a separate owner response; this is
  recorded in `AGENTS.md`, `docs/mentor-workflow.md`, and the project teaching
  Skill.

### 2026-07-21 — Phase 1B: final card-action gate

- Primary concept: final-action validation
- Supporting concept: dynamic legal action space
- Human-owned code: `validate_card_decision`, which derives legal choices from
  `offered_card_ids` and conditional `skip`, returns a valid decision unchanged,
  and raises `ValueError` for an invented or currently disabled action
- AI-supported work: explicit parameter/source/consumer contract, validator
  signature and integration point, direct and full-turn acceptance tests, test
  execution, review, and evidence-boundary explanation
- Behavior and test evidence: both deterministic tests passed; `card_x` and
  `skip` when `can_skip` was false were rejected, `card_a` was returned
  unchanged, and the existing complete fake model/tool turn still returned the
  legal `shrug_it_off` decision

| Dimension | Score (0-4) | Evidence |
| --- | ---: | --- |
| Conceptual understanding | 3 | Owner correctly placed dynamic business validation in `validate_card_decision`, separated it from provider translation and generic orchestration, and explained that observation comes from game facts while decision comes from the completed Agent turn. |
| Behavioral correctness | 4 | Owner's first implementation accepted offered IDs and conditionally legal skip, rejected all other choices, returned the original decision, and passed both direct and integrated happy-path tests. |
| Evaluation discipline | 2 | Deterministic tests covered invalid card, disabled skip, valid card, and full-turn compatibility, but the tests were AI-authored and the owner could not name a claim they do not prove. |
| Scope and simplicity | 4 | The gate used two direct checks and one error, added no abstraction or dependency, and left the provider adapter and generic loop unchanged. |
| Ownership and explanation | 4 | Owner implemented the complete gate without code hints after receiving the explicit input contract and accurately explained both parameter origins and the gate's safety purpose. |

- Total: 17/20
- Demonstrated strength: kept task-specific legality outside both the OpenAI
  adapter and provider-neutral Agent loop while enforcing the latest
  observation at the return boundary.
- Concept gap or uncertainty: a passing legality test proves protocol behavior
  for the covered inputs; it does not prove the card is strategically good,
  that every model response is well-shaped, or that tool requests are safe.
- Next exercise: add a tool-request gate that rejects an unknown tool or a card
  ID outside the current offered set before any handler executes.
- What would raise the target score by one point: state that the current tests
  prove covered action membership rules but do not prove strategy quality or
  untested malformed/tool-call behavior.

### 2026-07-21 — Phase 1A: owner-operated real API card decision

- Primary concept: end-to-end Agent composition
- Supporting concept: Agent turn versus model API turn
- Human-owned code: `run_live_decision`, which loads the card fixture, builds
  the bounded observation and local catalog, injects the OpenAI client into the
  provider adapter, registers the card-fact tool, and starts the existing Agent
  loop
- AI-supported work: entry-point signature and `main`, fake Responses client,
  offline acceptance test, progressive wiring hints, exact final local snippet,
  test/live execution, official API-key explanation, and review
- Behavior and test evidence: the deterministic fake-client test made exactly
  two provider requests and produced
  `observation -> tool_call -> tool_result -> final`; the owner-written entry
  then ran successfully against GPT-5.6-sol and returned `shrug_it_off` after a
  correlated `get_card_facts` result; the fixture resource warning was removed

| Dimension | Score (0-4) | Evidence |
| --- | ---: | --- |
| Conceptual understanding | 2 | Owner correctly concluded that repeated model calls belong to `run_agent_turn`, questioned why a separate composition root exists, and identified `client.responses.create` as the network call; the final explanation still confused composition with observation and described the whole loop as one iteration. |
| Behavioral correctness | 4 | Owner-written `run_live_decision` correctly constructed the catalog, bounded observation, model adapter, tool closure, and generic-loop invocation; both fake and real provider paths completed the required happy path. |
| Evaluation discipline | 2 | Deterministic and live evidence were both collected, but the test was AI-authored and the owner chose not to explain what fake versus live evidence can and cannot establish. |
| Scope and simplicity | 4 | The implementation remained one direct composition function and reused the existing loop, adapter, and tool instead of duplicating model-response handling. |
| Ownership and explanation | 2 | Owner typed and corrected the complete function and noticed the risk of duplicating `run_agent_turn`; substantial parameter/wiring guidance was needed, including the exact final local fragment, and the boundary explanation remained partial. |

- Total: 14/20
- Demonstrated strength: recognized that manually handling the first model
  response in `run_live_decision` would duplicate the state transition already
  owned by `run_agent_turn`.
- Concept gap or uncertainty: reading a composition function as a data-flow
  contract—where each injected parameter comes from, which existing component
  consumes it, and what different forms of evidence establish.
- Next exercise: implement a final-action gate with an explicit parameter and
  return-value table before scaffolding, rejecting any card ID or `skip` that is
  not legal in the supplied observation.
- What would raise the target score by one point: before writing the next core,
  explain the source and consumer of each parameter, then state one claim its
  deterministic test proves and one it does not prove.
- Mentor-process correction: future checkpoints must show parameter source,
  shape, use, return consumer, reusable components, and “do not reimplement”
  boundaries explicitly; this rule is now recorded in
  `docs/mentor-workflow.md` and the project teaching Skill.

### 2026-07-17 — Milestone 3A: one real GPT-5.6-sol Agent turn

- Primary concept: model/provider boundary
- Supporting concept: structured response normalization
- Human-owned code: `normalize_openai_response` conversion from OpenAI output
  items to provider-neutral `tool_call` or `final` events
- AI-supported work: system instructions, Responses API adapter, function tool
  and decision schemas, dependency setup, fake OpenAI client, acceptance test,
  live-call command, and targeted Python help
- Behavior and test evidence: all three offline tests passed; Python 3.9 syntax
  validation passed; a real `gpt-5.6-sol` run requested
  `get_card_facts(shrug_it_off)`, consumed the correlated tool result, and
  returned a legal structured final decision; a diagnostic confirmed multiple
  function calls are rejected instead of silently dropped

| Dimension | Score (0-4) | Evidence |
| --- | ---: | --- |
| Conceptual understanding | 3 | Owner explained that the provider adapter handles concrete API calls while the Agent loop consumes an abstract response contract; needed correction that a card-specific required-tool rule should not be hardcoded into the generic loop. |
| Behavioral correctness | 4 | Owner-written normalizer handled zero or one function call, parsed JSON arguments and final structured output, and explicitly rejected multiple calls; both fake and live provider paths satisfied the internal contract. |
| Evaluation discipline | 3 | Owner questioned the API output-array shape and implemented an explicit multiple-call boundary; evidence included deterministic tests, a focused diagnostic, and a live trace, though the tests remained AI-authored. |
| Scope and simplicity | 4 | The iteration added one stateful provider adapter, one normalizer, one tool schema, and no framework; parallel calls, retries, and production hardening remained deliberately deferred. |
| Ownership and explanation | 3 | Owner implemented the provider boundary and defended the adapter/orchestrator separation; the prompt was explicitly delegated to AI and the protocol-validation layer still required guidance. |

- Total: 17/20
- Demonstrated strength: noticed that `response.output` is an array and ensured
  unsupported parallel function calls fail visibly instead of losing requests.
- Concept gap or uncertainty: provider translation, generic orchestration, and
  task-specific protocol validation are three separate boundaries.
- Next exercise: add an independent validator that rejects a final trace unless
  the task's configured required tool appears before it, without changing the
  OpenAI adapter or hardcoding the rule in `run_agent_turn`.
- What would raise the target score by one point: explain why some valid Agent
  turns need no tool and demonstrate a configurable validator that enforces
  required tool use only for this card-choice task.

### 2026-07-16 — Milestone 2A: one offline tool-using Agent turn

- Primary concept: tool use
- Supporting concept: Agent state transition and basic context update
- Human-owned code: `run_agent_turn` transition loop
- AI-supported work: local `get_card_facts` tool, scripted model setup,
  fixture reuse, trace acceptance test, Python argument/data-access help, and
  test execution
- Behavior and test evidence: the owner-written loop produced the trace
  `instructions -> observation -> tool_call -> tool_result -> final`; the
  second model turn received the correlated tool result; both project tests
  passed

| Dimension | Score (0-4) | Evidence |
| --- | ---: | --- |
| Conceptual understanding | 3 | Owner explained that a tool response must be retained for the next model call and identified `decision` versus audit/debug `trace`; needed help separating response `type`, tool `name`, and tool `arguments`. |
| Behavioral correctness | 4 | Owner-written loop executed the allowed happy-path tool request, preserved `call_id` and tool name, fed facts into the next turn, stopped on the final response, and returned a legal decision with the complete trace. |
| Evaluation discipline | 1 | The AI-authored trace test passed, but the owner could not yet distinguish “the model saw a tool result” from “the final decision causally depended on that result”; failure cases were deliberately deferred. |
| Scope and simplicity | 3 | The implementation stayed in one direct loop with one local tool and no new dependency; an unused `MAX_LOOP_TURNS` constant remains, but no framework or premature abstraction was introduced. |
| Ownership and explanation | 3 | Owner implemented and iteratively corrected the transition loop and explained the purpose of context, decision, and trace; detailed protocol and test claims still required guidance. |

- Total: 14/20
- Demonstrated strength: implemented the essential Agent transition that feeds
  a correlated tool result into a subsequent model turn instead of treating
  the tool call as the final answer.
- Concept gap or uncertainty: temporal ordering is not causal evidence; a tool
  result appearing before a final response does not prove the response used it.
- Next exercise: make the scripted model's final response conditional on the
  actual `tool_result` content, then show that changing or removing that result
  changes the outcome.
- What would raise the target score by one point: explain the exact claim each
  trace assertion supports and give one counterexample in which the trace order
  is correct but the final decision ignores the tool result.

### 2026-07-16 — Milestone 1A: one legal offline card choice

- Primary concept: legal action space
- Supporting concept: observation
- Human-owned code: `choose_card` decision policy
- AI-supported work: wiki-backed fixture, function scaffold, acceptance test, test execution, targeted review
- Behavior and test evidence: the deterministic acceptance test passed; diagnostics showed a legal card when skip was disabled, `skip` for an empty skippable choice set, and `ValueError` when no legal action existed

| Dimension | Score (0-4) | Evidence |
| --- | ---: | --- |
| Conceptual understanding | 3 | Owner explained observation, offered-card legality, policy, and decision output; needed correction that observation is bounded input and skip depends on `can_skip`. |
| Behavioral correctness | 4 | Owner-written policy returned only offered-card IDs or legal `skip` in the acceptance case and reviewed boundary diagnostics. |
| Evaluation discipline | 1 | The deterministic test was AI-authored and passed, but the owner could not yet explain what its assertions prove or do not prove. |
| Scope and simplicity | 3 | The solution stayed within one direct function and added no dependency or premature abstraction; some conditions and counters remain more complex than the current behavior requires. |
| Ownership and explanation | 3 | Owner wrote and repeatedly corrected the policy and explained its intended rule; the explanation of the final skip condition was slightly stronger than the actual code. |

- Total: 14/20
- Demonstrated strength: preserved the legal-action boundary while correcting data-shape and control-flow errors through targeted hints.
- Concept gap or uncertainty: distinguishing behavior verified by assertions from strategy quality and untested branches.
- Next exercise: write one owner-authored test that disables skip and verifies the returned card ID is one of the offered IDs.
- What would raise the target score by one point: explain which claim each assertion supports and name one important claim the test cannot support.

Use this template for later entries:

```markdown
### YYYY-MM-DD — Milestone and behavior

- Primary concept:
- Supporting concept:
- Human-owned code:
- AI-supported work:
- Behavior and test evidence:

| Dimension | Score (0-4) | Evidence |
| --- | ---: | --- |
| Conceptual understanding |  |  |
| Behavioral correctness |  |  |
| Evaluation discipline |  |  |
| Scope and simplicity |  |  |
| Ownership and explanation |  |  |

- Total: /20
- Demonstrated strength:
- Concept gap or uncertainty:
- Next exercise:
- What would raise the target score by one point:
```
