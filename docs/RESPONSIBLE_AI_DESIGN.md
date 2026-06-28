# Responsible AI Design

## Core principle

The SLM proposes. The system decides. Humans remain in control.

## Why this matters

Human-AI collaboration is not automatically better than either humans or AI alone. The strongest evidence is more favourable for creative/content tasks than decision tasks, so this demo uses bounded creative missions and human feedback rather than truth-by-majority decision-making.

Local SLMs can reduce latency, cost, and privacy risks, but they are still limited. They can drift from the goal, make unsupported claims, return malformed output, or overhelp.

## Public claim to make

Use:

> Local AI can be useful, but it needs people, rules, evidence, software checks, and fallback to stay on track.

Avoid:

> The crowd and AI are smarter together.

That is too broad and not always supported by evidence.

## Responsibility layers

| Layer | Purpose |
|---|---|
| Constrained UI | Prevent unsafe or messy input before it reaches the model |
| Mission state | Keep clear goals, rules, and allowed actions |
| Structured output | Make model proposals machine-checkable |
| Validators | Enforce intent, schema, rule, evidence, and safety checks |
| Human feedback | Let visitors and staff accept, repair, or reject |
| Fallback | Keep the public demo running safely |
| Logging hygiene | Keep logs technical and non-identifying |

## Checks

### Intent check

Did the proposal follow the winning crowd choice?

### Schema check

Did the proposal match required JSON fields and enums?

### Rule check

Did it follow the mission rule selected by the crowd?

### Evidence check

If it made a factual claim, did it cite an approved local fact?

### Safety check

Is the output suitable for a public Open Day booth?

## Approved check labels

- `pass`
- `warn`
- `fail`
- `not_required`
- `needs_human`
- `fallback_used`

## Safe visible failure

The demo should include safe model failures because they teach the point.

Examples:

- the AI gives away a game puzzle answer;
- the AI invents an event detail;
- the AI overclaims a career path;
- the AI blocks harmless chat feedback;
- the AI suggests a reef action that breaks the rule.

These should be canned or controlled examples, not uncontrolled failures.

## Factual claims

Facts about JCU, courses, dates, jobs, or current events must come from approved content or be rewritten as questions for staff.

Example repair:

```text
Unsupported: “This course guarantees a cybersecurity job.”

Repaired: “Ask staff about cybersecurity, software, data, and AI pathways, and what kinds of projects students work on.”
```

## Do not use majority vote for truth

The crowd can express preference, detect obvious mismatch, or choose repair direction. It should not be treated as an authority for factual correctness.

Use majority vote for:

- mission goal;
- preferred style;
- whether an answer feels useful;
- repair direction;
- whether to ask staff.

Do not use majority vote for:

- whether a factual claim is true;
- whether a real person/image is authentic;
- medical/legal/financial advice;
- contentious political claims.

## Public wording

Use:

- “This shows the system’s control state, not private model reasoning.”
- “The AI is generating a likely continuation, not necessarily a correct answer.”
- “This mode is experimental, so we also have a reliable fallback.”
- “People set the goal, the local AI proposes, and software checks before the result is used.”

Avoid:

- “The AI is thinking.”
- “The AI understands exactly like a person.”
- “This shows the model’s private reasoning.”
- “The AI is always correct.”
- “No human oversight is needed.”
- “This is fully autonomous.”

## Research anchors

See `docs/RESEARCH_NOTES.md` for the literature basis.
