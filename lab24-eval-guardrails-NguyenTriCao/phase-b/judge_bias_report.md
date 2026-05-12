# Phase B.4: Judge Bias Observations

## Overview
This report documents the biases observed in the LLM-as-a-Judge system during the Pairwise and Absolute scoring phases.

## Calibration Results (Phase B.3)
- **Kappa Score**: 0.0789
- **Interpretation**: Slight Agreement. 
- **Observation**: The LLM judge (GPT-4o-mini) tended to score significantly lower than human reviewers on the same samples, indicating a "harsh judge" profile for this specific legal/financial context.

## Observed Biases

### 1. Positional Bias (Pairwise Judge)
- **Evidence**: During the `swap-and-average` test on 7 samples:
    - 5 out of 7 times, Answer B (the second position) was selected as the winner.
- **Observation**: There is a noticeable "Recency Bias" or Position B bias in this specific run.
- **Mitigation Status**: Mitigation implemented via swap-and-average, which correctly identified several "Inconsistent" cases where bias was detected.

### 2. Verbosity Bias (Absolute Scoring)
- **Observation**: Answers that provided more context (reference answers) consistently scored 4-5, while shorter, concise RAG answers often received 1-2, even if they were factually correct but missing "flowery" detail.

### 3. Self-Preference Bias
- **Description**: The LLM judge may prefer structured JSON or list formats typical of OpenAI training data.

## Recommendations for Production
- **Few-shot Prompting**: Include examples of "Good" vs "Bad" concise answers to reduce verbosity bias.
- **Position Randomization**: Continue using position swapping for all pairwise tasks.
- **Regular Audit**: The low Kappa score (0.0789) suggests the Judge's prompt needs further refinement or the task is too subjective for zero-shot evaluation.
