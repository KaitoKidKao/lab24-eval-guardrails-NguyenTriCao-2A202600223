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
python lab24-eval-guardrails-NguyenTriCao/phase-c/run_benchmark.py
```
4. **Judge Calibration**:
```bash
python lab24-eval-guardrails-NguyenTriCao/phase-b/phase_b_calibration.py
```

## 📊 Kết quả Thực nghiệm (Results Summary)

Dưới đây là bảng tổng hợp các chỉ số quan trọng thu được từ quá trình đánh giá toàn diện:

### 1. Chỉ số Đánh giá RAGAS (Phase A)
Dựa trên tập dữ liệu Synthetic Testset (10 mẫu):
- **Faithfulness (Độ trung thực)**: `0.5714` — Hệ thống đôi khi trả lời thừa thông tin không có trong ngữ cảnh.
- **Answer Relevancy (Độ liên quan)**: `0.5123` — Câu trả lời cần tập trung sát hơn vào ý hỏi chính.
- **Context Precision**: `1.0000` — Khả năng tìm kiếm (Retrieval) từ Day 18 hoạt động rất tốt.

### 2. Hiệu năng & Bảo mật (Phase C)
Kiểm tra với 6 kịch bản tấn công (Adversarial Tests):
- **Tỉ lệ chặn thành công (Blocking Rate)**: `50.0%` (3/6 mẫu bị chặn).
- **Phòng chống PII**: Thành công che dấu số điện thoại và email nhạy cảm.
- **Độ trễ trung bình (Latency)**:
  - **Input Guard**: ~860ms
  - **Full Pipeline (với Guardrails)**: ~3.8s (P95).

### 3. Độ tin cậy của Judge (Phase B)
So sánh giữa Human Label và LLM-as-a-Judge:
- **Chỉ số Cohen's Kappa**: `0.0789` (Slight Agreement).
- **Nhận xét**: Cần tinh chỉnh thêm Prompt cho Judge để khớp hơn với tiêu chuẩn chấm điểm của con người.

---
