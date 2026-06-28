# Research Notes

## Core anchor

Paper [1] from the literature review is a key design anchor:

**Vaccaro, Almaatouq & Malone (2024), “When combinations of humans and AI are useful: A systematic review and meta-analysis.”**

Design implication:

> Human-AI collaboration is not automatically better. It depends on the task and interaction design. Evidence is more promising for creative/content-generation tasks than for decision-making tasks.

For this demo, that means:

- use creative, bounded missions;
- do not ask the crowd to decide factual truth;
- do not claim that “crowd + AI is always smarter”;
- evaluate whether the interface helps people keep the local AI on track.

## Local SLM rationale

The demo frames local SLMs as useful because they may offer:

- lower latency;
- lower operating cost;
- offline/local operation;
- privacy advantages;
- task-specific deployment.

But local does not mean automatically correct or safe. The system still needs constraints, checks, fallback, and human oversight.

## Human-in-the-loop design implication

The crowd must have real influence over the outcome. Superficial “approval” is not enough.

In this demo, the crowd:

- sets goals;
- sets rules;
- judges whether the proposal stayed on track;
- chooses repair direction.

Staff retain final reset/fallback authority.

## Co-creative design implication

The mission loop should be iterative:

```text
human direction → AI-style proposal → software checks → human repair → result
```

This is stronger than one prompt followed by one generated output.

## Collective intelligence caution

The crowd can express preference or detect obvious mismatch, but majority vote is not truth.

Use voting for:

- goals;
- constraints;
- usefulness;
- repair direction.

Do not use voting as proof that a factual claim is correct.

## Trust calibration implication

Do not show vague “confidence” numbers as if they make the AI trustworthy.

Show inspectable state instead:

```text
Crowd chose...
Proposal says...
Rule check...
Evidence check...
Crowd decision...
```

## MVP 0.2 research position

MVP 0.2 intentionally uses deterministic proposals. This lets the team test the human-in-the-loop interaction before introducing model variability.

The research question for the prototype becomes:

> Does making the control loop visible help visitors understand that useful AI systems require goals, rules, evidence, human judgement, and fallback?
