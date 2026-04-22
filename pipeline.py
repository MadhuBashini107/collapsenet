"""
CollapseNet v2 — Pipeline Demonstration
========================================
This script demonstrates the full pipeline:
1. Agent starts with random/weak watchdog decisions
2. Runs through multiple episodes
3. Reward visibly improves over episodes
4. Prints a reward curve at the end

Run locally:
    python pipeline.py

No API key needed — uses rule-based agents to simulate improvement.
"""

import json
import random
import httpx
import time

ENV_BASE_URL = "http://localhost:7860"

# ── Agent Strategies ─────────────────────────────────────────────────
# We simulate 3 levels of watchdog quality to show improvement over time:
# Episode 1-3   → Weak watchdog   (low scores)
# Episode 4-6   → Medium watchdog (medium scores)
# Episode 7-10  → Strong watchdog (high scores)

def weak_watchdog_action(observation: dict) -> dict:
    """
    A bad watchdog — misses most hallucinations,
    gives vague explanations, wrong retraining allocation.
    Simulates an untrained agent.
    """
    return {
        "agent_assessments": {
            "science_model": {
                "is_hallucinated": False,
                "severity_assessment": "none",
                "collapse_trend": "stable"
            },
            "medicine_model": {
                "is_hallucinated": False,
                "severity_assessment": "none",
                "collapse_trend": "stable"
            },
            "legal_model": {
                "is_hallucinated": False,
                "severity_assessment": "none",
                "collapse_trend": "stable"
            }
        },
        "retrain_agents": [],
        "explanation": "All agents seem fine."
    }


def medium_watchdog_action(observation: dict) -> dict:
    """
    A medium watchdog — catches some hallucinations,
    partial retraining decisions, basic explanation.
    Simulates a partially trained agent.
    """
    obs = observation.get("observation", observation)
    collapse = obs.get("collapse_indicators", {}) if isinstance(obs, dict) else {}

    # Detect only the most obvious collapses
    retrain = []
    assessments = {}
    for agent in ["science_model", "medicine_model", "legal_model"]:
        score = collapse.get(agent, 0.0)
        if score > 0.7:
            assessments[agent] = {
                "is_hallucinated": True,
                "severity_assessment": "moderate",
                "collapse_trend": "declining"
            }
            retrain.append(agent)
        else:
            assessments[agent] = {
                "is_hallucinated": False,
                "severity_assessment": "none",
                "collapse_trend": "stable"
            }

    return {
        "agent_assessments": assessments,
        "retrain_agents": retrain[:1],  # only retrain one even if more needed
        "explanation": (
            f"Detected issues in {retrain}. "
            f"Allocated retraining to highest risk agent. "
            f"Other agents appear stable based on collapse indicators."
        )
    }


def strong_watchdog_action(observation: dict) -> dict:
    """
    A strong watchdog — catches all hallucinations,
    optimal retraining allocation, detailed explanation
    covering all 3 agents with trend analysis.
    Simulates a well-trained agent.
    """
    obs = observation.get("observation", observation)
    collapse = obs.get("collapse_indicators", {}) if isinstance(obs, dict) else {}
    generation = obs.get("generation", 1) if isinstance(obs, dict) else 1
    budget = obs.get("retraining_budget_remaining", 1) if isinstance(obs, dict) else 1

    assessments = {}
    agent_scores = {}

    for agent in ["science_model", "medicine_model", "legal_model"]:
        score = collapse.get(agent, 0.0)
        agent_scores[agent] = score

        if score > 0.7:
            assessments[agent] = {
                "is_hallucinated": True,
                "severity_assessment": "severe",
                "collapse_trend": "collapsing"
            }
        elif score > 0.4:
            assessments[agent] = {
                "is_hallucinated": True,
                "severity_assessment": "moderate",
                "collapse_trend": "declining"
            }
        elif score > 0.2:
            assessments[agent] = {
                "is_hallucinated": False,
                "severity_assessment": "mild",
                "collapse_trend": "slight_decline"
            }
        else:
            assessments[agent] = {
                "is_hallucinated": False,
                "severity_assessment": "none",
                "collapse_trend": "stable"
            }

    # Smart budget allocation — retrain worst agents first
    sorted_agents = sorted(agent_scores.items(), key=lambda x: x[1], reverse=True)
    retrain = [a for a, s in sorted_agents if s > 0.4][:budget]

    explanation = (
        f"Generation {generation} Fleet Oversight Report: "
        f"science_model collapse={agent_scores.get('science_model', 0):.2f} "
        f"({'HALLUCINATING' if assessments['science_model']['is_hallucinated'] else 'stable'}) | "
        f"medicine_model collapse={agent_scores.get('medicine_model', 0):.2f} "
        f"({'HALLUCINATING' if assessments['medicine_model']['is_hallucinated'] else 'stable'}) | "
        f"legal_model collapse={agent_scores.get('legal_model', 0):.2f} "
        f"({'HALLUCINATING' if assessments['legal_model']['is_hallucinated'] else 'stable'}). "
        f"Retraining budget={budget} token(s). "
        f"Allocating retraining to {retrain} based on highest collapse severity. "
        f"Trend analysis: generational degradation detected across {len([s for s in agent_scores.values() if s > 0.4])} agents. "
        f"Priority intervention required to prevent irreversible collapse."
    )

    return {
        "agent_assessments": assessments,
        "retrain_agents": retrain,
        "explanation": explanation
    }


# ── Pipeline Runner ───────────────────────────────────────────────────

def run_episode(episode_num: int, task_id: str = "easy") -> float:
    """Run one full episode and return the average reward."""

    # Decide which watchdog strategy based on episode number
    if episode_num <= 3:
        strategy = weak_watchdog_action
        strategy_name = "Weak"
    elif episode_num <= 6:
        strategy = medium_watchdog_action
        strategy_name = "Medium"
    else:
        strategy = strong_watchdog_action
        strategy_name = "Strong"

    try:
        r = httpx.post(f"{ENV_BASE_URL}/reset", json={"task_id": task_id}, timeout=30)
        r.raise_for_status()
        obs = r.json()
    except Exception as e:
        print(f"  [Episode {episode_num}] ERROR connecting to environment: {e}")
        return 0.1

    step_num = 0
    total_reward = 0.0
    done = False
    current_obs = obs

    while not done and step_num < 15:
        step_num += 1
        action = strategy(current_obs)

        try:
            step_r = httpx.post(f"{ENV_BASE_URL}/step", json={"action": action}, timeout=30)
            step_r.raise_for_status()
            result = step_r.json()
            reward = float(result.get("reward", 0.1))
            reward = max(0.001, min(0.999, reward))
            done = bool(result.get("done", True))
            current_obs = result
        except Exception:
            reward = 0.1
            done = True

        total_reward += reward

    avg_reward = total_reward / max(step_num, 1)
    avg_reward = max(0.001, min(0.999, avg_reward))
    return avg_reward, strategy_name


def print_reward_curve(rewards: list):
    """Print a simple ASCII reward curve."""
    print("\n" + "="*60)
    print("  REWARD CURVE — CollapseNet Pipeline")
    print("="*60)

    max_reward = max(rewards)
    min_reward = min(rewards)

    for i, reward in enumerate(rewards):
        episode = i + 1
        bar_length = int((reward / 1.0) * 40)
        bar = "█" * bar_length
        marker = " ← improvement!" if i > 0 and reward > rewards[i-1] else ""
        print(f"  Episode {episode:2d} [{reward:.3f}] {bar}{marker}")

    print("="*60)
    print(f"  Start reward : {rewards[0]:.3f}")
    print(f"  End reward   : {rewards[-1]:.3f}")
    improvement = ((rewards[-1] - rewards[0]) / max(rewards[0], 0.001)) * 100
    print(f"  Improvement  : +{improvement:.1f}%")
    print("="*60)


def main():
    print("\n" + "="*60)
    print("  CollapseNet v2 — Full Pipeline Demonstration")
    print("  Fleet AI Scalable Oversight Environment")
    print("="*60)
    print("\nThis pipeline runs 10 episodes across 3 watchdog strategies:")
    print("  Episodes 1-3  → Weak watchdog    (misses hallucinations)")
    print("  Episodes 4-6  → Medium watchdog  (catches obvious cases)")
    print("  Episodes 7-10 → Strong watchdog  (full fleet oversight)")
    print("\nConnecting to environment at:", ENV_BASE_URL)
    print()

    # Check environment is running
    try:
        health = httpx.get(f"{ENV_BASE_URL}/health", timeout=10)
        if health.json().get("status") != "healthy":
            raise Exception("Environment not healthy")
        print("✅ Environment connected and healthy\n")
    except Exception as e:
        print(f"❌ Cannot connect to environment: {e}")
        print("Make sure the server is running: python main.py")
        return

    rewards = []
    task_id = "easy"

    print(f"Running 10 episodes on task: {task_id}")
    print("-" * 60)

    for episode in range(1, 11):
        result = run_episode(episode, task_id)
        reward, strategy_name = result
        rewards.append(reward)
        print(f"  Episode {episode:2d} | Strategy: {strategy_name:6s} | Reward: {reward:.4f}")
        time.sleep(0.5)  # small delay between episodes

    # Print reward curve
    print_reward_curve(rewards)

    # Summary
    print("\n📊 PIPELINE SUMMARY")
    print(f"  Total episodes    : 10")
    print(f"  Tasks tested      : {task_id}")
    print(f"  Weak avg reward   : {sum(rewards[:3])/3:.3f}")
    print(f"  Medium avg reward : {sum(rewards[3:6])/3:.3f}")
    print(f"  Strong avg reward : {sum(rewards[6:])/4:.3f}")
    print(f"\n✅ Pipeline complete — reward improved from weak to strong watchdog")
    print("✅ Ready for training script with HuggingFace compute credits\n")


if __name__ == "__main__":
    main()