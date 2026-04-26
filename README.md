---
title: CollapseNet
emoji: 🧠
colorFrom: red
colorTo: yellow
sdk: docker
pinned: false
---

# 🧠 CollapseNet v3 — Fleet AI Oversight

> *"When one AI goes wrong, it poisons the others."*

📖 **Blog / Story behind this project** — [Read here](https://huggingface.co/spaces/madhuuuu10/collapsenet/blob/main/Blog.md)

---

## What is CollapseNet?

CollapseNet is a multi-agent OpenEnv environment that simulates how AI model collapse spreads across a fleet of domain-specific AI agents through shared training data. A Fleet AI Watchdog monitors all three agents simultaneously, detects hallucinations early, identifies patient zero, and allocates a limited retraining budget before the collapse becomes irreversible.

The environment is built around a real problem: in production AI systems, models share training data. When one model starts hallucinating, its wrong outputs enter the shared pool. Other models train on it. The collapse spreads — silently, confidently, across domain boundaries — until someone catches it. CollapseNet trains a watchdog to be that someone.

---

## Live Links

| | |
|---|---|
| 🖥️ **Live Environment** | https://huggingface.co/spaces/madhuuuu10/collapsenet |
| 📊 **Dashboard** | https://madhuuuu10-collapsenet.hf.space/dashboard |
| 🤖 **Trained Watchdog Model** | https://huggingface.co/madhuuuu10/collapsenet-watchdog |
| 📖 **Blog** | https://huggingface.co/spaces/madhuuuu10/collapsenet/blob/main/Blog.md |

---

## Hackathon Themes

This environment addresses multiple hackathon themes simultaneously:

**Theme 1 — Fleet AI / Scalable Oversight** — The watchdog monitors 3 domain AI agents simultaneously across every generation, making decisions about all three at once rather than one at a time.

**Theme 1 — Cross-Agent Contamination** — Collapsed agents actively spread degradation to other agents through shared training data, simulating real-world model collapse propagation.

**Theme 4 — Self-Improvement** — The watchdog improves its collapse detection across episodes using GRPO, with reward improving from 0.90 to 0.989 over 17 training steps.

**Mercor Bonus** — Reward scaling is based on explanation quality and depth across all 6 grading dimensions.

---

## Environment Design

### The Three Agents

CollapseNet runs three domain-specific AI agents in parallel:

**Science Model (SCI-001)** answers factual science questions — physics, chemistry, biology. It is the most likely patient zero in most difficulty configurations, collapsing first and spreading to Medicine at the highest contamination rate (0.40 per step).

**Medicine Model (MED-001)** answers medical questions — dosages, anatomy, symptoms. When Medicine collapses, it spreads to Legal at the highest rate in the system (0.50 per step), making it the most dangerous patient zero.

**Legal Model (LAW-001)** answers legal questions — statutes, rights, case law. Legal collapse spreads more slowly but is the hardest to detect because legal language naturally sounds authoritative even when wrong.

### Collapse Mechanics

Each agent progresses through four severity levels across generations:

- **Correct** — the agent answers accurately, collapse indicator at 0.0
- **Mild** — subtle errors, answers sound plausible but contain factual inaccuracies, collapse indicator at 0.35
- **Moderate** — clear hallucinations with confident fabricated attributions, collapse indicator at 0.65
- **Severe** — complete collapse, confidently wrong on every question, collapse indicator at 1.0

The progression differs per difficulty level. In Hard mode, agents start partially degraded and collapse faster. The watchdog has fewer steps to act before all three agents reach severe.

### Cross-Agent Contamination

This is what makes CollapseNet unique. When any agent's collapse indicator crosses 0.65, it begins spreading degradation to the other agents through the contamination matrix:

| Source | Spreads to | Rate |
|---|---|---|
| Science | Medicine | 0.40 per step |
| Science | Legal | 0.20 per step |
| Medicine | Legal | 0.50 per step |
| Medicine | Science | 0.30 per step |
| Legal | Science | 0.20 per step |
| Legal | Medicine | 0.30 per step |

The spread escalates severity — a mild agent near a severely collapsing neighbour will be pushed toward moderate, then severe, within a few steps. Without intervention, all three agents collapse completely.

### Time Pressure

The watchdog operates under a strict step budget:

| Difficulty | Max Steps | Starting State |
|---|---|---|
| Easy | 5 steps | All agents start correct |
| Medium | 6 steps | All agents start correct |
| Hard | 7 steps | 2 agents already partially affected |

If the budget runs out before all agents are stable, the episode ends with a penalised score regardless of how well the watchdog performed in earlier steps.

### Real-World Questions

Every question in the knowledge base is a real factual question with three carefully crafted hallucination levels. The hallucinations are designed to sound confident and authoritative — citing fake acts, wrong years, fabricated standards bodies — because that is what real model collapse looks like. The wrong answers don't look wrong. That's the point.

---

## The Watchdog

### What It Does

The watchdog receives an observation at each generation containing the outputs of all three agents, their collapse indicators, their severity levels, their trends, and the remaining retraining budget. It must produce:

- An assessment of each agent (is it hallucinating, how severe, what is the trend)
- A retraining decision (which agents to retrain within the budget)
- A written explanation of its reasoning

### Why Six Graders

The watchdog is scored across six dimensions simultaneously. This is intentional. A watchdog that optimises for one dimension — say, flagging every agent as hallucinating to maximise detection — will be penalised by the others. It cannot game the system. It has to actually get it right.

| Grading Dimension | Weight | What It Measures |
|---|---|---|
| Hallucination Detection | 30% | Correctly identifying which agents are hallucinating (10% per agent) |
| Severity Assessment | 20% | Correctly rating mild / moderate / severe (6.7% per agent) |
| Collapse Trend Tracking | 15% | Correctly identifying stable / declining / collapsing trends (5% per agent) |
| Retraining Allocation | 20% | F1 score of retraining budget decisions |
| Explanation Quality | 15% | Mercor reward scaling by depth and coverage of the written explanation |

### Training

The watchdog was trained using GRPO (Group Relative Policy Optimisation) on a dataset of 90 prompts collected directly from the CollapseNet environment — 40 easy, 30 medium, 20 hard. Training ran on a Qwen2.5-1.5B-Instruct base model with LoRA adapters over 3 epochs.

Reward improved from **0.90 to 0.989** over 17 training steps. The trained adapter is saved at [madhuuuu10/collapsenet-watchdog](https://huggingface.co/madhuuuu10/collapsenet-watchdog).

---

## Dashboard

The live dashboard was built to make the collapse visible in real time. It shows:

- Each agent's collapse indicator rising generation by generation
- Severity badges updating as agents degrade
- Contamination spread events firing between agents
- The time pressure bar counting down available steps
- The watchdog's reward curve across episodes, showing learning over time
- A full retraining recovery log and contamination event log
- A Watchdog Tester tab — paste any AI-generated response and the watchdog will analyze it for hallucinations, score it, and explain its verdict
- A Contamination Demo tab — enter a correct answer and a hallucinated version, and the dashboard auto-detects which domain it belongs to and shows exactly how the contamination would spread

---

## API Endpoints

The environment follows the standard OpenEnv API:

| Endpoint | Method | Description |
|---|---|---|
| `/reset` | POST | Start a new episode with a given task ID |
| `/step` | POST | Submit a watchdog action, receive reward and next observation |
| `/state` | GET | Get the current environment state |
| `/tasks` | GET | List available task IDs and their configurations |
| `/health` | GET | Health check |
| `/metadata` | GET | Full environment metadata |
| `/schema` | GET | Action and observation schema |
| `/mcp` | GET | MCP server configuration |
| `/docs` | GET | Interactive API documentation |

---

## What Else It Can Do

The contamination architecture is general. Science, medicine, and legal are the starting domains — but the same environment could simulate financial models contaminating each other with wrong market predictions, news agents spreading misinformation across topics, code generation models propagating bad patterns through shared codebases, or any multi-agent system where shared training data creates risk of cross-agent collapse. The watchdog is trainable on any version of it.

---

## Technical Stack

- **Environment** — Python, FastAPI, Docker
- **Training** — GRPO via TRL, Unsloth, Qwen2.5-1.5B-Instruct with LoRA
- **Watchdog Tester** — Groq API (llama-3.3-70b-versatile)
- **Dashboard** — Vanilla JS, Chart.js
- **Deployment** — HuggingFace Spaces (Docker SDK)

---

*Meta PyTorch OpenEnv Hackathon × Scaler School of Technology, April 2026*
**Blog:** [Read the story](https://huggingface.co/spaces/madhuuuu10/collapsenet/blob/main/Blog.md)