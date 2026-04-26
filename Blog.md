# From Bio-Math to Building AI That Watches AI

*Meta PyTorch OpenEnv Hackathon × Scaler School of Technology, April 2026*

---

It was 2023. I had just completed 12th grade with bio-math and joined college. On day one, my college handed me programming modules — nearly 12 of them, each with 40 to 50 questions. I had never written a single line of code in my life.

My friends told me to use AI to get through the work quickly, then learn from the code. Genius plan. So that's what I did. But I kept getting errors. So many errors. I didn't know if the AI was wrong or if I was wrong. So I did what any reasonable person would do — I asked the AI again. It gave me another answer. Also confident. Also wrong. I asked again. Still wrong, but now with more enthusiasm.

The breaking point came quietly. I'd ask the AI to print something using a do-while loop. It would give me a while loop. Confidently. Like it had done exactly what I asked. It hadn't. And I couldn't always tell — because I didn't know enough yet to know the difference. The code looked right. It just wasn't. My modules had hidden test cases, and the AI's answers kept failing them in ways I couldn't see until it was too late.

That's when I gave up on AI entirely. I went back to basics — books, YouTube videos, anything that would actually explain what was happening instead of just handing me broken code with a smile. My friends had finished their modules in their first year. I finished all 12 in December 2025. Two years after everyone else. When I finally did, there was relief, there was pride — but mostly I just wished I had done it sooner. I wished someone had caught the problem earlier. I wished something had told me: this answer is wrong, don't trust it.

---

April 2026. I joined a hackathon with no background in reinforcement learning. Bold choice.

While preparing, I kept running into that same feeling from 2023 — the AI sounding completely sure of itself, the answer being wrong. This time I knew it was wrong, because I had learned it the hard way. And this time, instead of just feeling frustrated, I wanted to understand why it keeps happening.

I found out it has a name: model collapse. When AI models train on AI-generated data, each generation gets slightly more wrong, slightly more confident. The errors don't look like errors. They look like facts — stated cleanly, with no hesitation. And nobody catches it until the damage is already done. Until a student spends two years not knowing who to trust. Until a patient gets the wrong dosage. Until a defendant gets the wrong advice.

I didn't want another Madhu to go through what I went through.

---

So I built CollapseNet.

Three AI agents — science, medicine, and legal — answer real factual questions across generations. Each generation, one of them starts to slip. The answers stay confident. They just stop being right. A watchdog monitors all three simultaneously, trying to catch who collapsed first and stop the damage before it spreads.

But here's the part that surprised me when I started building — I didn't expect hallucination to cause this much trouble. I thought one model going wrong would be contained. It isn't. All three agents share the same training data pool. When the science model hallucinates a legal fact, that answer enters the pool. The legal model trains on it. Now the legal model is wrong too. And it doesn't know it. The contamination spreads like a virus, silently, across domain boundaries, and nobody on the outside can tell anything is wrong because every answer still sounds perfectly confident.

That's what scared me. That's exactly what happened to me in 2023 — I got confident wrong answers and had no way to know. I built CollapseNet so something could know.

---

I wanted to understand exactly what was happening inside the system, so I built a live dashboard. Not for judges — for myself. I needed to see the collapse in real time, watch the contamination spread from one agent to another, understand how a model gets contaminated before I could build something to stop it. The dashboard shows each agent's collapse indicator rising generation by generation, the moment contamination jumps between domains, and the watchdog's decisions in real time. Watching it for the first time — seeing the science model hallucinate and the legal model's indicator start climbing — I didn't expect it to be that visible. That clean. That fast.


![screencapture-madhuuuu10-collapsenet-hf-space-dashboard-2026-04-26-08_53_57](https://cdn-uploads.huggingface.co/production/uploads/69d1fea67ccb13fe3cdb94e2/0iDxnYF0-x8Oz5IGHSzmm.png)


![screencapture-madhuuuu10-collapsenet-hf-space-dashboard-2026-04-26-08_55_12](https://cdn-uploads.huggingface.co/production/uploads/69d1fea67ccb13fe3cdb94e2/uc_zgCjYJoEJW4kRHFPLH.png)


![screencapture-madhuuuu10-collapsenet-hf-space-dashboard-2026-04-26-08_55_44](https://cdn-uploads.huggingface.co/production/uploads/69d1fea67ccb13fe3cdb94e2/kqUla4qt2hT2hT9mC2tPR.png)


![screencapture-madhuuuu10-collapsenet-hf-space-dashboard-2026-04-26-08_56_59](https://cdn-uploads.huggingface.co/production/uploads/69d1fea67ccb13fe3cdb94e2/YrZvVxOoYKC1hNmcRI9jc.png)

The watchdog doesn't get to cheat either. I didn't give it one judge. I gave it six — hallucination detection, severity assessment, collapse trend tracking, retraining allocation, explanation quality, and Mercor reward scaling. All six have to be satisfied at the same time. If the watchdog finds a shortcut that fools one, the others pull its score down. There is no single loophole. It has to actually get it right. Unlike a certain AI I used to know.

I trained it using GRPO directly on this environment. The reward went from 0.90 to 0.989 over 17 steps. It learned to find patient zero. It learned to act before the spread became irreversible.



![image](https://cdn-uploads.huggingface.co/production/uploads/69d1fea67ccb13fe3cdb94e2/ouu-fDE9fs0bejnRS0aZs.png)

---

What makes CollapseNet different from other environments is the contamination mechanism. Most environments simulate one model collapsing in isolation. CollapseNet simulates what actually happens in the real world — collapse that spreads. The cross-agent contamination follows real spread rates between domains: science infects medicine fastest, medicine infects legal, and so on. Add time pressure — the watchdog has a limited number of steps to act before all three agents are corrupted — and you have something that genuinely forces the model to think strategically, not just react.

The environment works on any domain. Science, medicine, and legal are the starting point. But the same architecture could simulate financial models contaminating each other, news agents spreading misinformation, or code generation models propagating bad patterns. The collapse mechanism is general. The watchdog is trainable on any version of it.

---

I built this in a week. From scratch. With no RL background.

But I had something better than a background — I had two years of knowing exactly what it feels like to be on the receiving end of a confident, hallucinating AI. Turns out that's pretty good motivation.

---

**Live environment:** https://huggingface.co/spaces/madhuuuu10/collapsenet


**Dashboard:** https://madhuuuu10-collapsenet.hf.space/dashboard


**Trained model:** https://huggingface.co/madhuuuu10/collapsenet-watchdog
