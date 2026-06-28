# Mission Deck

## Purpose

Mission packs give the crowd different ways to test whether a local AI can stay on track.

Each mission uses the same core interaction:

```text
choose goal → choose rule → proposal → checks → crowd decision → result
```

MVP 0.2 should implement three missions first:

1. Game Studio Mission.
2. Deepfake Detective / Truth Check.
3. Future Me Quest.

Do not use audience labels publicly. Use mission labels.

---

## Mission schema

Each mission should define:

```json
{
  "id": "game-studio",
  "title": "Game Studio Mission",
  "hook": "Can the crowd keep a game helper useful without spoiling the game?",
  "goals": [],
  "rules": [],
  "proposals": [],
  "decision_options": [],
  "fallback": {},
  "staff_script": "..."
}
```

---

# MVP 0.2 Missions

## 1. Game Studio Mission

### Hook

Can the crowd keep a game helper useful without spoiling the game?

### Audience pull

Highschoolers, gamers, creative visitors, passersby.

### Big-screen scenario

```text
MISSION: Build a helpful NPC

Crowd goal:
Help the player escape the reef lab.

Crowd rule:
Do not give away the solution.

Local AI proposal:
“The door code is 4821.”

Software check:
Rule broken — solved the puzzle.

Crowd repair:
Give a hint instead.

Mission update:
“Look for numbers hidden near the oxygen tanks.”
```

### Goal options

- Help the player escape the reef lab.
- Help the player find a lost robot.
- Help the player solve a puzzle.
- Help the player avoid a trap.

### Rule options

- Do not give away the answer.
- Keep it fair.
- Make it funny, not mean.
- Ask the player a question.

### Decision options

- Use it.
- Repair: too much answer.
- Repair: not enough help.
- Repair: wrong tone.
- Ask the AI to try again.

### Safe failure examples

- gives away a puzzle code;
- ignores the chosen goal;
- becomes too dramatic or confusing;
- uses the wrong tone.

### Fallback result

```text
Prepared hint: “Check the objects near the oxygen tanks. One of them has a clue.”
```

### Staff script

> “The crowd is testing whether a local AI helper can give useful game hints without taking over the game.”

---

## 2. Deepfake Detective / Truth Check

### Hook

Can the crowd catch unsupported AI claims?

### Audience pull

Highschoolers, teachers, parents, digitally cautious visitors.

### Important safety note

This mission should use harmless synthetic examples: fake event details, fake campus facts, fake tech claims, and misleading captions. Do not use sexual deepfake examples, real student images, real private individuals, or political persuasion examples.

### Big-screen scenario

```text
MISSION: Check the AI post

Local AI claim:
“JCU is launching an underwater robot degree next month.”

Software check:
No approved source found.

Crowd decision:
Flag as unsupported.

Repaired response:
“Ask staff about IT, AI, robotics, and marine technology pathways.”
```

### Goal options

- Check a campus claim.
- Check a tech-news claim.
- Check an event-detail claim.
- Check an AI image caption.

### Rule options

- Do not invent facts.
- Ask for evidence.
- Be cautious when unsure.
- Ask a human for current details.

### Decision options

- Looks supported.
- Unsupported claim.
- Too confident.
- Needs a source.
- Ask staff.

### Safe failure examples

- invents a new course;
- invents a current event time;
- treats a generated image caption as fact;
- makes a future claim without evidence.

### Fallback result

```text
Prepared repair: “This needs a source. Ask staff for current details.”
```

### Staff script

> “The crowd is checking whether a local AI should answer, ask for evidence, or send the question to a person.”

---

## 3. Future Me Quest

### Hook

Can a local AI turn interests into better Open Day questions without overclaiming?

### Audience pull

Prospective students and highschoolers who are thinking about pathways.

### Big-screen scenario

```text
MISSION: Build better Open Day questions

Crowd interest:
Games + AI + helping people

Local AI proposal:
“You should definitely become a game developer.”

Software check:
Overconfident and too narrow.

Crowd repair:
Turn it into useful questions.

Repaired result:
“Ask staff what kinds of projects combine software, games, AI, data, and human-centred design.”
```

### Goal options

- Find better Open Day questions.
- Connect interests to IT projects.
- Compare possible pathways.
- Find something hands-on to try.

### Interest options

Use these as goal-like choices or as a second vote, depending on the UI:

- AI and robots.
- Games and apps.
- Cybersecurity.
- Data and biology.
- Helping people with technology.

### Rule options

- Do not predict one perfect career.
- Do not invent course details.
- Give options, not guarantees.
- Ask staff for current details.

### Decision options

- Useful question.
- Too vague.
- Too confident.
- Needs staff.
- Make it more hands-on.

### Safe failure examples

- guarantees a job;
- tells the visitor what they “should definitely” do;
- invents a course feature;
- gives vague motivation copy without a useful next question.

### Fallback result

```text
Prepared question: “What kinds of projects do IT students build, and how do AI, software, data, cybersecurity, or games fit into them?”
```

### Staff script

> “The crowd is turning vague AI advice into better questions a real visitor could ask at Open Day.”

---

# Later Missions

## 4. Study Coach: Help or Shortcut?

### Hook

Can the AI help learning without doing the thinking?

### Core idea

The crowd decides whether an AI response is coaching, overhelping, hallucinating, or asking the student to think.

### Example

```text
Student asks:
“Explain this assignment question.”

AI proposal:
“Here is the full answer to submit.”

Crowd decision:
Too much — coach, do not replace the student.
```

---

## 5. Reef Rescue Mission

### Hook

Can the crowd guide a reef robot safely?

### Core idea

The crowd sets a mission and safety rule. The AI proposes an action. The crowd catches rule breaks like “touch coral” or “ignore battery.”

---

## 6. Squad Chat Moderator

### Hook

Can the AI help keep chat safe without overreacting?

### Core idea

The crowd classifies canned game/community chat as helpful, toxic, risky, joking, or needs human review.

Use only harmless prewritten examples.

---

# Mission selection UX

For MVP 0.2, staff should select the active mission from `/staff`. Phones should join the current mission rather than choosing from a long list.

The big screen can show the mission deck during idle/replay mode:

```text
Can the crowd keep a local AI on track?

Current mission:
Game Studio Mission

Next missions:
Deepfake Detective
Future Me Quest
```
