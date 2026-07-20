const phaseVoteTypes = {
  goal_vote: "goal",
  rule_vote: "rule",
  check_vote: "check",
};

const pipelineOrder = {
  goal_vote: ["step-goal"],
  rule_vote: ["step-goal", "step-rule"],
  proposal: ["step-goal", "step-rule", "step-proposal", "step-checks"],
  check_vote: ["step-goal", "step-rule", "step-proposal", "step-checks"],
  result: ["step-goal", "step-rule", "step-proposal", "step-checks", "step-decision", "step-updated"],
  fallback: ["step-goal", "step-rule", "step-proposal", "step-checks", "step-decision", "step-updated"],
  replay: ["step-goal", "step-rule", "step-proposal", "step-checks", "step-decision", "step-updated"],
};

let latestState = null;

function qs(id) {
  return document.getElementById(id);
}

function setText(id, value) {
  const node = qs(id);
  if (node) node.textContent = value || "";
}

async function postJson(url, body = {}) {
  const response = await fetch(url, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
  if (!response.ok) {
    const text = await response.text();
    throw new Error(text);
  }
  render(await response.json());
}

function render(state) {
  latestState = state;
  setText("mission-title", state.mission_title);
  setText("mission-phase", `${state.mode.toUpperCase()} · ${state.phase.replaceAll("_", " ")} · round ${state.round}`);
  setText("question", state.question);
  setText("feedback", state.fallback_message || "Vote received by the shared local server.");
  setText("fallback", state.fallback_message || "");

  const proposal = state.proposal ? state.proposal.caption : "Waiting for the crowd to set direction.";
  setText("proposal", proposal);
  renderChoices(state);
  renderSelections(state);
  renderChecks(state);
  renderPipeline(state);
}

function renderSelections(state) {
  const selections = state.selections || {};
  setText("selected-goal", selections.goal ? selections.goal.label : "Waiting for the goal vote");
  setText("selected-rule", selections.rule ? selections.rule.label : "Waiting for the rule vote");
  setText("selected-decision", selections.decision ? selections.decision.label : "Waiting for the crowd decision");
  setText("result", state.result ? state.result.message : "Waiting for the round result");
}

function renderChoices(state) {
  const node = qs("choices");
  if (!node) return;
  node.innerHTML = "";

  if (!state.choices || state.choices.length === 0) {
    const empty = document.createElement("p");
    empty.className = "muted";
    empty.textContent = state.phase === "fallback" ? "Replay mode is active." : "No vote open right now.";
    node.appendChild(empty);
    return;
  }

  const voteType = phaseVoteTypes[state.phase];
  for (const choice of state.choices) {
    const button = document.createElement("button");
    const count = state.votes[choice.id] || 0;
    button.textContent = count > 0 ? `${choice.label} (${count})` : choice.label;
    button.addEventListener("click", async () => {
      button.disabled = true;
      try {
        await postJson("/api/vote", { vote_type: voteType, choice_id: choice.id });
      } catch (error) {
        setText("feedback", "That vote is not open right now.");
      } finally {
        button.disabled = false;
      }
    });
    node.appendChild(button);
  }
}

function renderChecks(state) {
  const node = qs("checks");
  if (!node) return;
  node.innerHTML = "";
  for (const [name, value] of Object.entries(state.checks || {})) {
    const item = document.createElement("span");
    item.className = `check check-${value}`;
    item.textContent = `${name}: ${value}`;
    node.appendChild(item);
  }
}

function renderPipeline(state) {
  for (const id of Object.values(pipelineOrder).flat()) {
    const node = qs(id);
    if (node) node.classList.remove("active");
  }
  for (const id of pipelineOrder[state.phase] || []) {
    const node = qs(id);
    if (node) node.classList.add("active");
  }
}

function connectWebSocket() {
  const scheme = window.location.protocol === "https:" ? "wss" : "ws";
  const socket = new WebSocket(`${scheme}://${window.location.host}/ws`);
  socket.addEventListener("message", (event) => render(JSON.parse(event.data)));
  socket.addEventListener("close", () => setTimeout(connectWebSocket, 1500));
}

async function pollState() {
  try {
    const response = await fetch("/api/state");
    render(await response.json());
  } catch (error) {
    setText("mission-phase", "Offline");
  }
}

function bindStaffControls() {
  for (const button of document.querySelectorAll("[data-staff-action]")) {
    button.addEventListener("click", () => postJson(button.dataset.staffAction));
  }
  for (const button of document.querySelectorAll("[data-staff-select]")) {
    button.addEventListener("click", () => {
      postJson("/api/staff/select-mission", { mission_id: button.dataset.staffSelect });
    });
  }
  for (const button of document.querySelectorAll("[data-staff-mode]")) {
    button.addEventListener("click", () => {
      postJson("/api/staff/mode", { mode: button.dataset.staffMode });
    });
  }
  for (const button of document.querySelectorAll("[data-staff-reset]")) {
    button.addEventListener("click", () => {
      postJson("/api/staff/reset", { scope: button.dataset.staffReset });
    });
  }
}

async function refreshJoinUrl() {
  const joinUrlNode = qs("join-url");
  const qrCode = document.querySelector(".qr-code");
  if (!joinUrlNode && !qrCode) return;

  try {
    const response = await fetch("/api/join-url", { cache: "no-store" });
    const data = await response.json();
    if (joinUrlNode) joinUrlNode.textContent = data.url;
    if (qrCode) qrCode.src = `/qr.svg?t=${Date.now()}`;
  } catch (error) {
    if (joinUrlNode) joinUrlNode.textContent = "Join URL unavailable";
  }
}

bindStaffControls();
refreshJoinUrl();
pollState();
connectWebSocket();
setInterval(() => {
  if (latestState) pollState();
}, 4000);
