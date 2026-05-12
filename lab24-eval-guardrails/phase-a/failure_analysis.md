# Phase A.3: Failure Cluster Analysis

## Overview
This document analyzes the failures identified during the RAGAS evaluation (Phase A.2).

## Result Summary (v1)
- **Faithfulness**: 0.57 (Low)
- **Answer Relevancy**: 0.51 (Low)
- **Context Precision**: 0.74 (Good)
- **Context Recall**: 0.61 (Fair)

## Failure Cluster 1: Hallucination despite relevant context
- **Symptoms**: High Context Precision but low Faithfulness.
- **Root Cause Hypothesis**: The LLM might be using its internal knowledge instead of strictly adhering to the provided Vietnamese legal/financial chunks.
- **Potential Fix**: Tighten system prompt to "ONLY use the provided context".

## Failure Cluster 2: Vague Answers
- **Symptoms**: Low Answer Relevancy.
- **Root Cause Hypothesis**: The queries from the synthetic generator might be too specific or abstract for the current chunk size, leading to incomplete answers.
- **Potential Fix**: Increase `RERANK_TOP_K` or use larger parent chunks.

## Failure Cluster 3: Retrieval Gaps
- **Symptoms**: Fair Context Recall (0.61).
- **Root Cause Hypothesis**: BM25 might be missing some semantic matches, or the dense embedding model (cohere) needs more specific tuning for Những văn bản pháp luật tiếng Việt dài.
- **Potential Fix**: Improve chunk enrichment (add more HyQA questions).

## Conclusion
The current pipeline is robust in retrieval (Precision) but weak in grounding and relevancy. Moving forward, we should focus on prompt engineering for better faithfulness and increasing context window for better relevancy.
