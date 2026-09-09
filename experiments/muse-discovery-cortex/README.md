# Muse Discovery Cortex — pilot

A small, reproducible prototype for testing the hypothesis that an agent can improve discovery by adding an explicit **question → mechanism graph → contradiction/verification → hypothesis → experiment** layer around ordinary task execution.

This is **not an implementation of Meta Muse** and does not claim access to Muse internals. Meta describes Muse as a personal agent with long-horizon execution, subagents, persistent context, browser/tool use, and a separate Sentinel safety layer. This repository tests a complementary cognitive layer offline.

## Pilot result

On the included 13-case synthetic cross-domain smoke benchmark:

- Direct keyword baseline: **6/13 = 46.2%**
- Discovery Cortex: **13/13 = 100.0%**
- Absolute improvement: **+53.8 percentage points**

⚠️ This is **not evidence of superiority over frontier AI**. The cases and intent mappings are deliberately small and partly hand-authored. The result only validates that the prototype's discovery pipeline executes and can recover the benchmark's predefined mechanism pairs.

## Run

```bash
python benchmark.py
python -m unittest -v
```

The benchmark fails if the Discovery Cortex does not beat the baseline, making the result suitable as a regression smoke test.

## Architecture

```text
problem
  ↓
question / intent detection
  ↓
mechanism graph
  ↓
cross-domain bridge candidates
  ↓
contradiction / falsification questions
  ↓
hypothesis
  ↓
proposed experiment
```

## Next research step

Replace the hand-authored intent hints with a real model-backed semantic layer, blind the benchmark labels, expand to 100+ problems, and evaluate against a strong agent baseline with independent judging and confidence calibration.
