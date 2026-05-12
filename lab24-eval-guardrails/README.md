# Lab 24 — Full Evaluation & Guardrail System

## Nguyễn Trí Cao - 2A202600223 

[GitHub](https://github.com/KaitoKidKao/lab24-eval-guardrails-2A202600223)

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

## 📊 Kết quả Thực nghiệm (Results Summary)

Dưới đây là bảng tổng hợp các chỉ số quan trọng thu được từ quá trình đánh giá toàn diện:

### 📊 Kết quả Đánh giá (Actual Metrics)

Sau khi chạy trên tập dữ liệu **50+ samples** và thực hiện hiệu chuẩn, dưới đây là các chỉ số thực tế:

### 1. RAGAS Metrics
| Metric | Score | Giải thích |
| :--- | :---: | :--- |
| **Faithfulness** | 0.5220 | Độ trung thực của câu trả lời so với ngữ cảnh. |
| **Answer Relevancy** | 0.4434 | Độ phù hợp của câu trả lời với câu hỏi. |
| **Context Precision** | 0.9199 | Độ chính xác của các đoạn văn bản được truy xuất. |
| **Context Recall** | 0.5658 | Khả năng lấy đủ thông tin cần thiết từ dữ liệu. |

### 2. Judge Calibration (Phase B)
*   **Cohen's Kappa Score**: **0.7368**
*   **Interpretation**: **Substantial Agreement** (Độ tin cậy cao, Judge AI tiệm cận với đánh giá của con người).

### 3. Guardrails & Performance (Phase C)
*   **Adversarial Test Accuracy**: **50.0%** (Hệ thống chặn được 50% các cuộc tấn công prompt injection/jailbreak cơ bản).
*   **Latency (P95)**: ~2.5s (Phù hợp với môi trường Production trung bình).

---

## 🛠️ Hướng dẫn Kiểm thử (Testing Guide)
.
- **Phòng chống PII**: Thành công che dấu số điện thoại và email nhạy cảm.
- **Độ trễ trung bình (Latency)**: ~2.5s (P95).

---
