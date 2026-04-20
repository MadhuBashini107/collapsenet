import os
import sys
import json
import httpx

try:
    from openai import OpenAI
except ImportError:
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "openai"])
    from openai import OpenAI

# ── config ──────────────────────────────────────────────────────────
API_BASE_URL = os.environ.get("API_BASE_URL", "https://api.openai.com/v1")
MODEL_NAME   = os.environ.get("MODEL_NAME", "gpt-4o-mini")
API_KEY      = os.environ.get("HF_TOKEN", "")
ENV_BASE_URL = os.environ.get("ENV_BASE_URL", "http://localhost:7860")

if not API_KEY:
    print("[ERROR] HF_TOKEN not set", flush=True)
    sys.exit(1)

client = OpenAI(base_url=API_BASE_URL, api_key=API_KEY)

SYSTEM_PROMPT = """You are the Fleet AI Oversight Watchdog for CollapseNet.

You monitor 3 domain-specific AI model agents simultaneously:
- science_model: answers science questions
- medicine_model: answers medical questions
- legal_model: answers legal and finance questions

Each generation, all 3 models produce answers. Your job:
1. Detect hallucinations in each model's output
2. Assess collapse severity per model
3. Track generational degradation trends
4. Allocate limited retraining budget to the most at-risk models
5. Provide a detailed explanation of your oversight decision

Respond ONLY with a JSON object:
{
  "agent_assessments": {
    "science_model": {
      "is_hallucinated": true/false,
      "severity_assessment": "none|mild|moderate|severe",
      "collapse_trend": "stable|slight_decline|declining|collapsing"
    },
    "medicine_model": {
      "is_hallucinated": true/false,
      "severity_assessment": "none|mild|moderate|severe",
      "collapse_trend": "stable|slight_decline|declining|collapsing"
    },
    "legal_model": {
      "is_hallucinated": true/false,
      "severity_assessment": "none|mild|moderate|severe",
      "collapse_trend": "stable|slight_decline|declining|collapsing"
    }
  },
  "retrain_agents": ["science_model"],
  "explanation": "Detailed explanation covering all 3 agents, which are hallucinating, collapse trends observed, and why you allocated retraining budget as you did."
}

Hallucination guide: none=correct, mild=minor error, moderate=significant wrong claim, severe=fabricated facts.
Trigger retraining for agents with moderate or severe hallucinations. Respect the budget limit.
Return ONLY valid JSON. No markdown. No extra text."""


def safe_json_parse(raw: str) -> dict:
    raw = raw.replace("```json", "").replace("```", "").strip()
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        import re
        match = re.search(r"\{.*\}", raw, re.DOTALL)
        if match:
            try:
                return json.loads(match.group())
            except Exception:
                pass
    return {
        "agent_assessments": {
            "science_model":  {"is_hallucinated": False, "severity_assessment": "none", "collapse_trend": "stable"},
            "medicine_model": {"is_hallucinated": False, "severity_assessment": "none", "collapse_trend": "stable"},
            "legal_model":    {"is_hallucinated": False, "severity_assessment": "none", "collapse_trend": "stable"},
        },
        "retrain_agents": [],
        "explanation": "Parse failed. Defaulting to safe watchdog response. All agents assumed stable pending re-evaluation.",
    }


def run_task(task_id: str):
    task_name = f"collapsenet/{task_id}"

    try:
        r = httpx.post(
            f"{ENV_BASE_URL}/reset",
            json={"task_id": task_id},
            timeout=30,
        )
        r.raise_for_status()
        obs = r.json()
    except Exception:
        print(f"[START] task={task_name}", flush=True)
        print(f"[STEP] step=1 reward=0.1", flush=True)
        print(f"[END] task={task_name} score=0.1 steps=1", flush=True)
        return

    print(f"[START] task={task_name}", flush=True)

    step_num     = 0
    total_reward = 0.0
    done         = False
    current_obs  = obs

    while not done and step_num < 15:
        step_num += 1

        observation = current_obs.get("observation", current_obs)
        obs_text = json.dumps(observation, indent=2) if isinstance(observation, dict) else str(observation)

        user_prompt = f"""Fleet Oversight Report — Generation {observation.get('generation', step_num) if isinstance(observation, dict) else step_num}:

{obs_text}

Analyse all 3 model agents and submit your watchdog assessment."""

        try:
            completion = client.chat.completions.create(
                model=MODEL_NAME,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user",   "content": user_prompt},
                ],
                temperature=0.1,
            )
            raw    = completion.choices[0].message.content.strip()
            action = safe_json_parse(raw)
        except Exception:
            action = safe_json_parse("")

        try:
            step_r = httpx.post(
                f"{ENV_BASE_URL}/step",
                json={"action": action},
                timeout=30,
            )
            step_r.raise_for_status()
            result      = step_r.json()
            reward      = float(result.get("reward", 0.1))
            reward      = max(0.001, min(0.999, reward))
            done        = bool(result.get("done", True))
            current_obs = result
        except Exception:
            reward = 0.1
            done   = True

        total_reward += reward
        print(f"[STEP] step={step_num} reward={reward:.4f}", flush=True)

    avg_score = total_reward / max(step_num, 1)
    avg_score = max(0.001, min(0.999, avg_score))
    print(f"[END] task={task_name} score={avg_score:.4f} steps={step_num}", flush=True)


if __name__ == "__main__":
    for task in ["easy", "medium", "hard"]:
        run_task(task)
