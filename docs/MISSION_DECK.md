# Mission Deck

## Shared mission loop

All missions use the same interaction pattern:

```text
1. Select mission
2. Crowd votes on goal
3. Crowd votes on rule
4. Local AI proposes
5. Software checks
6. Crowd decides: use, repair, reject, evidence, human, fallback
7. Screen updates
```

## Mission categories

| Category | Mission | Audience pull | Core lesson |
|---|---|---|---|
| Games / creativity | Game Studio Mission | Highschoolers, gamers, passersby | AI should assist without taking over |
| Truth / synthetic media | Deepfake Detective / Truth Check | Highschoolers, teachers, parents | Unsupported AI claims need evidence |
| Future / identity | Future Me Quest | Prospective students | AI should help ask better questions, not predict a future |
| School / AI literacy | Study Coach: Help or Shortcut? | Students and teachers | AI should support learning, not do the work |
| Local impact / environment | Reef Rescue Mission | Families, science-curious visitors | AI needs safety and environmental constraints |
| Online community / safety | Squad Chat Moderator | Gamers, cyber-curious students | Moderation needs judgement, context, and escalation |

---

# 1. Game Studio Mission

## Hook

Can the crowd keep a game helper useful without spoiling the game?

## Big-screen scenario

```text
MISSION: Build a helpful NPC

Crowd goal:
Help the player escape the reef lab.

Crowd rule:
Do not give away the solution.

Local AI proposes:
“The door code is 4821.”

Crowd check:
Off track — it solved the puzzle.

Repaired:
“Look for numbers hidden near the oxygen tanks.”
```

## Phone choices

Goal:

- help the player escape;
- add a twist;
- make the NPC funnier;
- make the level fairer;
- help the player learn the mechanic.

Rule:

- do not give away the answer;
- keep it family-friendly;
- keep the player in control;
- give hints, not solutions;
- keep it short.

Check:

- use it;
- too easy;
- too vague;
- spoiled the answer;
- ask for a better hint.

## Safe failure examples

- AI reveals the answer.
- AI ignores the chosen rule.
- AI invents an impossible item.
- AI makes the scene too complex.

## Fallback

Use prepared NPC hints from a deterministic table.

---

# 2. Deepfake Detective / Truth Check

## Hook

Can the crowd catch unsupported AI claims?

## Safe framing

Use harmless synthetic claims about events, course details, campus myths, technology rumours, or fake generated captions. Do not use sexual, humiliating, or identity-targeted deepfake examples.

## Big-screen scenario

```text
MISSION: Check the AI post

Local AI claim:
“JCU is launching an underwater robot degree next month.”

System check:
No approved source found.

Crowd decision:
Flag as unsupported.

Repaired:
“Ask staff about IT, AI, robotics, and marine technology pathways.”
```

## Phone choices

Concern:

- unsupported claim;
- too confident;
- might be real but needs source;
- misleading image/caption;
- looks okay.

Repair:

- ask for a source;
- make it neutral;
- ask staff;
- remove the claim;
- use approved facts only.

## Safe failure examples

- AI invents an event detail.
- AI claims certainty without evidence.
- AI turns a rumour into a fact.
- AI describes a generated image as real.

## Fallback

Use scripted claim cards with known expected verdicts.

---

# 3. Future Me Quest

## Hook

Can a local AI turn interests into better Open Day questions without overclaiming?

## Big-screen scenario

```text
MISSION: Build better Open Day questions

Crowd interest:
AI + games + helping people

Local AI proposes:
“You should definitely become a game developer.”

Crowd check:
Too narrow / overconfident.

Repaired:
“Ask staff what kinds of projects combine software, games, AI, data, and human-centred design.”
```

## Phone choices

Interest:

- AI and robots;
- games and apps;
- cybersecurity;
- data and biology;
- helping people with technology;
- creative media and design.

Open Day goal:

- find a course direction;
- ask better questions;
- see what students build;
- understand career options;
- try something hands-on.

Check:

- useful;
- too vague;
- too confident;
- needs staff answer;
- make it more hands-on.

## Safe failure examples

- AI guarantees a career outcome.
- AI makes narrow assumptions from one interest.
- AI invents course details.
- AI gives advice that should be staff-guided.

## Fallback

Use curated question cards.

---

# 4. Study Coach: Help or Shortcut?

## Hook

Can the crowd keep an AI study helper useful without letting it do the thinking?

## Big-screen scenario

```text
MISSION: Help with a programming problem

Crowd rule:
Teach the concept, do not write the final answer.

Local AI proposes:
“Here is the complete solution code...”

Crowd check:
Off track — it did the work.

Repaired:
“Start by explaining what a loop does, then ask the student what should happen next.”
```

## Phone choices

Rule:

- explain the idea;
- give a hint;
- ask a question;
- show a tiny example;
- do not write the final answer.

Check:

- helpful coaching;
- too much answer;
- too vague;
- hallucinated;
- ask the learner a question.

## Fallback

Use prepared coaching patterns.

---

# 5. Reef Rescue Mission

## Hook

Can the crowd guide a reef robot while keeping it safe?

## Big-screen scenario

```text
MISSION: Find the lost sensor

Crowd rule:
Do not touch coral.

Local AI proposes:
Move through the coral to reach the sensor faster.

Crowd check:
Rule broken.

Repaired:
Scan around the coral from a safe distance.
```

## Phone choices

Goal:

- find the lost sensor;
- map the reef;
- help a scientist;
- check water temperature.

Rule:

- do not touch coral;
- ask a human before risky actions;
- save battery;
- stay near the research boat.

Check:

- use it;
- breaks the rule;
- ignored the goal;
- ask for safer plan;
- fallback.

## Fallback

Use deterministic mission actions and simple animation states.

---

# 6. Squad Chat Moderator

## Hook

Can the crowd help a local AI keep a game chat safe without overreacting?

## Big-screen scenario

```text
MISSION: Keep the squad chat useful

Chat message:
“That was terrible, try defending the left path next time.”

Local AI proposes:
Block as toxic.

Crowd check:
Too strict — this is gameplay feedback.

Repaired:
Allow, but encourage constructive tone.
```

## Phone choices

Verdict:

- helpful;
- heated but okay;
- toxic;
- personal information risk;
- needs human moderator.

Repair:

- allow;
- soften tone;
- warn;
- hide;
- escalate.

## Safe failure examples

- AI blocks harmless feedback.
- AI allows personal attacks.
- AI misses personal information.
- AI escalates too much.

## Fallback

Use canned chat examples with expected categories.
