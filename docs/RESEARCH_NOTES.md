# Research Notes

This is a short research anchor file for the demo thesis.

## Anchor idea

Human-AI collaboration is not automatically better. The project should demonstrate careful task design, role design, and feedback loops rather than claim that “crowd + AI is smarter.”

## Paper 1 — Human-AI combinations

**Vaccaro, Almaatouq, and Malone (2024), “When combinations of humans and AI are useful: A systematic review and meta-analysis.”**

Useful takeaway for this demo:

- Human-AI combinations are heterogeneous.
- They can perform worse than the best human-only or AI-only option.
- Creative/content-generation tasks appear more promising than decision tasks.

Design implication:

- Use bounded creative missions, not consequential decision-making.
- Evaluate whether the system improves agency, understanding, and control, not just output quality.
- Do not claim that the crowd makes the AI correct.

Reference:

- https://arxiv.org/abs/2405.06087

## Small language models

SLMs are relevant because they are lower-latency, cheaper, easier to run locally, and better suited to resource-constrained or privacy-sensitive settings. Their limits are part of the demo story.

Design implication:

- Local AI should have a narrow role.
- Surround it with schemas, validators, fallback, and human feedback.
- Do not assume smaller/local means safer or more truthful.

References:

- https://arxiv.org/abs/2411.03350
- https://arxiv.org/abs/2510.13890

## Human-centred AI and meaningful control

Relevant principles:

- high automation can coexist with high human control;
- the human role must have real authority;
- people need compatible representations of what the system is doing;
- accountability must be traceable to human choices and system design.

Design implication:

- Show the control pipeline.
- Give the crowd meaningful choices.
- Give staff real override/reset/fallback controls.

## Trust and automation bias

Explanations alone do not guarantee better judgement. Interfaces should encourage checking, verification, and calibrated trust.

Design implication:

- Show check outcomes, not “AI reasoning.”
- Let visitors catch safe failures.
- Use clear labels such as `unsupported claim`, `breaks rule`, and `needs human`.

## RAG / grounding / abstention

Evidence retrieval and abstention can improve reliability but do not guarantee truth.

Design implication:

- Factual claims need approved sources.
- Unsupported factual claims should become neutral phrasing or staff questions.
- The system should fall back rather than guess.
