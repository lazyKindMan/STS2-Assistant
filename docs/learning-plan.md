# STS2 Agent teaching and implementation plan

## Goal

Build an inspectable Slay the Spire 2 Agent that can use the current game
state to:

1. choose one legal card reward or skip;
2. choose one currently reachable map node;
3. explain the decision and preserve an auditable execution trace;
4. eventually execute the selected action through one game boundary and read
   fresh state afterward.

The model supplies strategic judgment. This repository builds the harness:
observations, legal actions, context, tools, validation, state transitions,
traces, recovery, and the game interface. Win-rate optimization is not the
first learning target.

## How the reference syllabus is adapted

The teaching pattern comes from
`/Users/logan/PycharmProjects/learn-claude-code`: keep one Agent loop stable and
add one harness mechanism per lesson. We borrow the pattern, not all twenty
features.

| Reference topic | STS2 adaptation | Timing |
| --- | --- | --- |
| s01 Agent Loop | model response -> tool execution -> tool result -> next model turn or stop | Already practiced |
| s02 Tool Use | small read-only card/map knowledge tools behind a dispatch map | Already practiced; extend for routes |
| s03 Permission | validate tool calls and legal game actions before execution | Before any live action |
| s04 Hooks | only introduce after two cross-cutting needs actually exist | Optional, later |
| s05 Planning | a revisable route intention, not a generic coding todo list | After route decisions work |
| s06 Subagent | no current product need | Deferred |
| s07 Skill Loading | load task-specific card or map guidance only if prompt/knowledge size justifies it | Optional, after two decision types |
| s08 Context Compact | explicit fresh-state selection and a small context budget; no four-layer compactor yet | Before multi-turn game sessions |
| s09 Memory | game-session route intent only; not self-updating long-term memory | After route decisions work |
| s10 System Prompt | assemble card/map instructions from the actual decision type and tools | After both concrete modes exist |
| s11 Error Recovery | bounded retries and explicit terminal failures | After deterministic protocol tests |
| s12-s18 tasks, background, teams, worktrees | unrelated to the first playable assistant | Deferred |
| s19 MCP | one possible game integration boundary, not a mandatory architecture | Integration phase only |
| s20 Comprehensive | all selected mechanisms return to one provider-neutral loop | Final consolidation |

Two rules override the reference order:

- card choice and route choice are implemented in separate increments;
- no abstraction is introduced until card and route provide two concrete
  usages.

## Current baseline

Completed evidence:

- a manual card observation with an explicit legal action space;
- an offline provider-neutral Agent loop with one correlated tool result;
- an OpenAI Responses API adapter and structured response normalizer;
- offline tests for the loop and provider boundary;
- one AI-operated live GPT-5.6-sol trace proving the provider path can work.

The important remaining gap is that the owner has not yet written and operated
a repository entry point that composes the real client, observation, tools,
Agent loop, and final trace.

## Target runtime shape

```text
raw current game state
  -> normalize observation + enumerate legal actions
  -> select decision type and bounded context
  -> call model with only the relevant tools
  -> validate requested tool + arguments
  -> execute read-only knowledge tool
  -> append correlated tool result
  -> call model again until final or limit
  -> validate final action against the observation
  -> return decision + trace
  -> optional live phase: re-read state, validate again, execute, re-observe
```

Keep these boundaries visible even when their first implementation is a plain
function:

- **Game gateway** reads or acts on the external game.
- **Observation normalizer** converts raw state to bounded card or map facts.
- **Legal-action enumerator** is authoritative for what may be selected now.
- **Context builder** decides what the model sees this turn.
- **Provider adapter** translates one vendor API to internal model events.
- **Agent loop** repeats model/tool transitions and enforces a turn limit.
- **Tool/action guard** validates before local or external execution.
- **Decision validator** rejects invented or stale actions.
- **Trace evaluator** checks protocol behavior independently of strategy quality.

## Roadmap

Each slice adds one observable behavior, reserves one human-owned core, and
ends with deterministic evidence plus a plain-language reflection.

### Phase 0 — Agent foundations (complete)

| Slice | Observable behavior | Primary concept | Human-owned core |
| --- | --- | --- | --- |
| 0A | Return only an offered card ID or legal skip | observation and legal action space | `choose_card` rule |
| 0B | Feed one local tool result into a second model turn | tool use and state transition | `run_agent_turn` |
| 0C | Translate OpenAI output items to provider-neutral events | provider boundary | `normalize_openai_response` |

### Phase 1 — One owner-operated real card decision

#### 1A. Real API entry point — current next slice

- Behavior: one command/function loads a manual observation, creates the real
  OpenAI client, runs the tool loop, and prints a legal decision plus trace.
- Acceptance: the trace contains
  `observation -> tool_call -> tool_result -> final`; one Agent turn may contain
  two or more model API calls.
- Human-owned core: `run_live_decision` composition function.
- AI support: entry-point signature, deterministic fake-client test, review,
  environment check, and live verification.
- Deliberately absent: retries, route choice, game action execution.

#### 1B. Final-action gate

- Behavior: an invented card ID or illegal `skip` is rejected before it is
  returned to a caller.
- Acceptance: `card_x` fails when the observation offers only
  `card_a/card_b/card_c`; an offered ID passes.
- Human-owned core: `validate_card_decision`.

#### 1C. Tool-call gate

- Behavior: the harness does not execute an unregistered tool or query facts
  for a card outside the current offered IDs.
- Acceptance: `get_card_facts(card_x)` is rejected before the handler runs.
- Human-owned core: `validate_tool_request`.

#### 1D. Independent-turn isolation

- Behavior: two independent card decisions using the same application process
  do not leak `previous_response_id`, observations, or tool results.
- Acceptance: the first API request of turn two contains its new observation
  and no response ID from turn one.
- Human-owned core: the turn start/reset rule.

### Phase 2 — Route choice as a second decision domain

#### 2A. Route observation and legal actions

- Behavior: a manual map snapshot exposes full useful topology separately from
  the smaller set of nodes reachable on the current step.
- Acceptance: the decision may return only a reachable node ID.
- Human-owned core: `build_route_observation`.

#### 2B. One offline route tool turn

- Behavior: a scripted model inspects one reachable node/path through a local
  read-only tool, consumes the result, and returns one legal node.
- Acceptance: trace order matches the card loop while route data and tools are
  different.
- Human-owned core: the route tool request/argument contract.

#### 2C. One real route decision

- Behavior: the real provider chooses a currently reachable node from the
  manual map snapshot and returns a reason plus trace.
- Acceptance: the final node is in `reachable_node_ids`; no game action is
  executed yet.
- Human-owned core: `run_live_route_decision` composition function.

### Phase 3 — Generalize only after two concrete usages

#### 3A. Runtime task assembly

- Behavior: `card` and `route` turns expose different instructions, schemas,
  tools, and final validators while sharing the same Agent loop.
- Acceptance: a card turn cannot see route tools and a route turn cannot call
  card-only tools.
- Human-owned core: `build_turn_spec`.
- Reference lesson: s10 runtime prompt assembly based on real state, not keyword
  guessing.

#### 3B. Bounded context builder

- Behavior: each model turn records which current observation, relevant tool
  results, and optional route plan were included or omitted.
- Acceptance: a stale observation is replaced rather than accumulated; any
  budget omission is visible in the trace.
- Human-owned core: `build_model_context` selection rule.

#### 3C. Revisable route intent

- Behavior: a short session plan can prefer future nodes across map steps, but
  the newest reachable set always overrides stale intent.
- Acceptance: when a planned node becomes unreachable, the Agent chooses only
  from the fresh legal actions and records that it revised the plan.
- Human-owned core: `update_route_plan`.
- Reference lesson: adapt planning and memory to game-session state; do not add
  a generic task system or persistent self-editing memory.

### Phase 4 — Evaluation and resilience

Run these as separate small iterations, one failure behavior at a time.

| Slice | Observable behavior | Primary concept | Human-owned core |
| --- | --- | --- | --- |
| 4A | A trace policy can require a configured tool before final without hardcoding OpenAI or card rules into the loop | protocol evaluation | `validate_trace` |
| 4B | Malformed final output becomes an explicit terminal error/fallback, not a Python key failure | model-output safety | final-event validation rule |
| 4C | Repeated tool calls stop at a defined limit with a traceable reason | bounded autonomy | loop-limit transition |
| 4D | One selected transient API failure retries within a fixed budget, then stops | error recovery | recovery state transition |

Strategy evaluation remains separate: a small human-reviewed set may compare
decision reasons and preferences, but it must not weaken legal/protocol tests.

### Phase 5 — One live game boundary

Choose direct HTTP or MCP after inspecting the available game adapter; do not
implement both. Use `/Users/logan/PycharmProjects/CharTyr-STS2-Agent` only as a
read-only contract reference.

#### 5A. Read current card-reward state

- Behavior: fetch one raw live state and normalize it to the already-tested
  card observation without executing an action.
- Human-owned core: `normalize_card_reward_state`.

#### 5B. Execute one card action safely

- Behavior: re-read state, verify the chosen card/skip is still legal, execute
  it, then return fresh post-action state.
- Human-owned core: `execute_card_decision_safely`.

#### 5C. Read current map state

- Behavior: normalize full topology and currently reachable nodes from one live
  map state without moving.
- Human-owned core: `normalize_map_state`.

#### 5D. Execute one route action safely

- Behavior: re-read state, validate the chosen node is still reachable, move,
  and return fresh post-action state.
- Human-owned core: `execute_route_decision_safely`.

Card execution and route execution remain separate iterations.

### Phase 6 — Consolidate the playable MVP

#### 6A. Card screen through the unified runtime

- Behavior: the application recognizes a supported card-reward state and runs
  the card turn through the shared harness.
- Human-owned core: the card dispatch transition.

#### 6B. Map screen through the unified runtime

- Behavior: in a later iteration, the same application recognizes a supported
  map state and runs the route turn.
- Human-owned core: the route dispatch transition.

The finished MVP is inspectable and bounded, not autonomous gameplay. Combat,
shops, events, relic decisions, OCR/UI automation, multi-agent delegation,
background workers, cron, RAG, vector databases, RL, and win-rate training stay
outside scope until explicitly selected after this plan.

## Teaching protocol for every slice

```text
CONCEPT
  define one harness concept
  -> connect it to the current STS2 behavior
  -> user predicts/designs the transition
IMPLEMENT
  AI supplies fixture/signature/failing test
  -> user writes exactly one human-owned core
REVIEW
  inspect the attempt
  -> run the smallest deterministic test
  -> make one correction at a time
REFLECT
  user explains input, legal actions, context change, stop rule, and evidence
DONE
  score 5 dimensions, update journal, choose the next slice
```

Live API calls demonstrate integration but never replace deterministic tests.
The teaching plan may be adjusted from journal evidence, but later mechanisms
must not jump ahead of an unfinished prerequisite.

## Immediate next step

Resume Phase 1A with `开始本轮`. The first concept check is the distinction
between one Agent turn and its multiple model API calls. After the answer, AI
will scaffold the runnable entry point and failing offline test, then stop for
the owner's implementation.
