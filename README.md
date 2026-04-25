# From Bio-Math to Building AI That Watches AI

*Meta PyTorch OpenEnv Hackathon × Scaler School of Technology, April 2026*

---

It was 2023. I had just completed my 12th grade with bio-math and joined college. My college gave me programming modules on day one — nearly 12 of them, each with 40 to 50 questions. I had never written a single line of code in my life.

My friends told me to use AI to get through the work quickly, then learn from the code. So that's what I did. But I kept getting errors. So many errors. I didn't know what was wrong. I didn't know if the AI was wrong, or if I was wrong. I couldn't tell the difference. So I did what any confused first-year student does . I asked the AI again. It gave me another answer. Also confident. Also wrong.

My friends completed their modules in their first year. I was stuck at the second module while they moved on. I finished all of them in December 2025. It took me nearly two years to do what they did in months, not because I wasn't trying, but because I spent those two years unable to tell when my tools were lying to me.

---

April 2026. I joined a hackathon with no background in reinforcement learning.

While preparing, I kept running into that same feeling from 2023 — the AI sounding completely sure of itself, the answer being wrong. This time I knew it was wrong, because I had learned it the hard way. And this time, instead of just feeling frustrated, I wanted to understand why it keeps happening.

I found out it has a name: model collapse. When AI models train on AI-generated data, each generation gets slightly more wrong, slightly more confident. The errors don't look like errors. They look like facts — stated cleanly, with no hesitation. And nobody catches it until the damage is already done. Until a student has spent two years not knowing who to trust. Until a patient gets the wrong dosage. Until a defendant gets the wrong advice.

---

I didn't want to just read about it. I wanted to build something that catches it. I didnt want another Madhu, going through the same.

So I built CollapseNet , an environment where three AI agents, covering science, medicine, and law, slowly collapse across generations, and a watchdog has to catch them before it's too late. The part that scared me most when I was researching wasn't that one model could go wrong. It was that one wrong model could corrupt the others, because they all share the same training data. A science model hallucinates a legal fact. That answer enters the shared pool. The legal model trains on it. Now the legal model is wrong too. And it doesn't know it. That's what CollapseNet simulates. That's what the watchdog is trained to stop.

I trained the watchdog using GRPO directly on this environment. The reward went from 0.90 to 0.989 over 17 steps. It learned to find patient zero. It learned to act before the spread became irreversible.

And you might ask — how do I know the watchdog isn't just gaming the system? I thought about that too. So I didn't give it one judge. I gave it six. It has to satisfy all of them at once — hallucination detection, severity assessment, collapse trend tracking, retraining allocation, explanation quality, and Mercor reward scaling. If it finds a shortcut that fools one, the others pull its score down. There is no single loophole to exploit. It has to actually get it right.

---

I built this in a week. From scratch. With no RL background.

But I had something better than a background . I had two years of knowing exactly what it feels like to be on the receiving end of a confident, hallucinating AI. I think that's worth something.


---

**Live environment:** https://huggingface.co/spaces/madhuuuu10/collapsenet  
**Dashboard:** https://madhuuuu10-collapsenet.hf.space/dashboard  
**Trained model:** https://huggingface.co/madhuuuu10/collapsenet-watchdog