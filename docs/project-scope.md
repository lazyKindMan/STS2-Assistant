# STS2 Agent learning scope

## Project purpose

Build a Slay the Spire 2 assistant as a concrete sandbox for learning Agent
programming: context construction, model turns, tool calls, state transitions,
validation, and evaluation.

Card and route decisions provide understandable inputs, but strategy quality is
not the center of the curriculum. The project is successful when the owner can
read an execution trace and explain why the Agent called a tool, what entered
the model context, how the tool result changed that context, and why the loop
stopped. Maximum win rate, complete game support, and unattended play are not
initial goals.

## Smallest Agent definition

The learning target is this loop:

```text
goal + fresh observation
  -> build bounded context
  -> model returns a tool request or final response
  -> validate and execute one allowed tool
  -> append the tool result to context
  -> model returns a legal final decision
```

The project has already exercised this structure with both a scripted model
and an OpenAI Responses API adapter. The next increment closes the remaining
learning gap by letting the owner compose and operate one real end-to-end card
decision. Route choice follows as a separate decision domain.

The complete phased sequence, reference-syllabus mapping, human-owned cores,
and acceptance evidence are defined in `docs/learning-plan.md`.

## Collaboration contract

Every milestone reserves one key piece of code for the project owner to write personally. AI acts as a tutor, scaffold builder, test author, reviewer, and debugger around that code.

For the current Phase 1A slice:

```text
Human-owned core: run_live_decision composition function
AI-supported work: entry-point signature, deterministic fake-client test, environment check, test execution, live verification, and review
Learning checkpoint: stop after the entry-point scaffold and failing offline test; wait for the owner to compose the real client, observation, tools, and Agent loop
```

AI must not complete the human-owned function unless the owner explicitly requests the full implementation. If the owner asks for help, progress from a conceptual question to a hint, pseudocode, and partial snippet before providing a full answer.

Before moving past the current slice, the owner should be able to explain:

1. Which context is sent into each model turn.
2. How a model tool request differs from a final response.
3. Why one Agent turn may contain multiple model API calls.
4. How the tool result is appended before the next model turn.
5. Which state or stop condition prevents an uncontrolled loop.
6. What the execution trace and test do and do not prove.

## Agent concept curriculum

Use this as a direction, not as permission to teach every concept at once.

| Phase | Primary Agent concepts |
| --- | --- |
| 0. Foundations (complete) | Observation, legal action space, tool loop, provider boundary |
| 1. Real card decision | End-to-end composition, final/tool gates, independent turns |
| 2. Route decision | Map observation, reachable actions, route tool use |
| 3. Shared harness | Runtime prompt/tool assembly, context selection, route intent |
| 4. Evaluation and resilience | Trace policies, malformed output, loop limits, bounded recovery |
| 5. Live game boundary | Fresh-state normalization, revalidation, action execution |
| 6. Playable MVP | Card and route dispatch added in separate increments to one runtime |

Teach one primary concept and at most one supporting concept in each iteration. Record completed concepts and evidence in `docs/learning-journal.md`.

## Phased implementation

Use `docs/learning-plan.md` as the executable curriculum. Its order is:

```text
completed foundations
  -> owner-operated real card decision
  -> card tool/final safety gates
  -> independent-turn context isolation
  -> offline then real route decision
  -> shared card/route harness
  -> trace evaluation and bounded recovery
  -> one selected live game boundary
  -> card and route screen dispatch in separate increments
```

Do not collapse adjacent arrows into one iteration. A real API demonstration
does not replace an offline deterministic test, and a valid final choice does
not prove that the tool/context protocol was followed.

## Source decisions

- Use the [STS2 wiki card list](https://slaythespire.wiki.gg/wiki/Slay_the_Spire_2:Cards_List) for small, reviewed card-fact snapshots.
- Never call the wiki from normal tests.
- Treat `/Users/logan/PycharmProjects/CharTyr-STS2-Agent` as a read-only architecture reference.
- Reuse its state/action separation and fresh-state discipline.
- Defer its full Mod, HTTP, MCP, SSE, planner/combat handoff, and persistent knowledge stack.
- Read `skills/build-sts2-agent-increments/references/sources-and-lessons.md` for the detailed research notes and CodeGraph status.

## Definition of done for every increment

An increment is done only when:

1. It introduces one observable behavior and one learning concept.
2. Its input and expected output are written down.
3. The smallest relevant automated test passes.
4. Its trace makes model turns, tool calls, and stop conditions inspectable when
   those concepts are in scope.
5. No returned action falls outside the supplied legal choices.
6. The owner can explain the context change or state transition introduced.
7. New abstractions can be explained in plain language.
8. Deliberately omitted work is recorded.
9. The iteration stops before starting the next milestone.

## Current boundary

Start Phase 1A with one owner-written `run_live_decision` composition function
and a deterministic fake-client test. The slice may make a live OpenAI call for
acceptance evidence, but it does not add route choice, retries, live game action
execution, MCP, persistent memory, or multi-agent orchestration.
