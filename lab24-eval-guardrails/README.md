# Lab 24 — Full Evaluation & Guardrail System

## Nguyễn Trí Cao - 2A202600223 

[GitHub](https://github.com/KaitoKidKao/lab24-eval-guardrails-NguyenTriCao-2A202600223)

## Overview
Dự án này triển khai hệ thống đánh giá và bảo mật toàn diện cho pipeline RAG (Sản xuất). 
Hệ thống bao gồm 4 giai đoạn chính: Đánh giá tự động RAGAS, Đánh giá bằng LLM-as-a-Judge, Lớp bảo mật Guardrails (Input/Output) và Tài liệu Blueprint.

## Setup
1. Cài đặt các gói cần thiết:
```bash
pip install -r requirements.txt
pip install ragas presidio-analyzer presidio-anonymizer scikit-learn groq
```
2. Cấu hình file `.env` với:
- `OPENAI_API_KEY`
- `COHERE_API_KEY`
- `GROQ_API_KEY` (cho Llama Guard 3)

## Project Structure
- **phase-a/**: RAGAS Evaluation (Synthetic Testset, Results, Failure Analysis).
- **phase-b/**: LLM-as-a-Judge (Pairwise, Absolute, Human Calibration).
- **phase-c/**: Guardrails (PII, Topic, Safety, Latency Benchmark).
- **phase-d/**: Technical Blueprint (Architecture, SLOs).

## How to Run Tests
1. **RAGAS Evaluation**:
```bash
python lab24-eval-guardrails/phase-a/phase_a_run_eval.py
```
2. **Adversarial Guardrail Test**:
```bash
python lab24-eval-guardrails/phase-c/run_adversarial.py
```
3. **Latency Benchmark**:
```bash
python lab24-eval-guardrails/phase-c/run_benchmark.py
```
4. **Judge Calibration**:
```bash
python lab24-eval-guardrails/phase-b/phase_b_calibration.py
```

## Results Summary
- **Faithfulness**: 0.57 (v1)
- **Answer Relevancy**: 0.51 (v1)
- **Guardrail Latency**: < 500ms (P95)
- **Safety Gate**: Active (Llama Guard 3)
- **Adversarial Accuracy**: 50.0% (Blocking success rate)
