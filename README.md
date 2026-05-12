# Production RAG System: Evaluation & Guardrails

## Thông tin sinh viên
- **Họ và tên**: Nguyễn Trí Cao
- **MSSV**: 2A202600223
- **Repository**: [lab24-eval-guardrails](https://github.com/KaitoKidKao/lab24-eval-guardrails-2A202600223)

---

## 🌟 Tổng quan dự án
Dự án này triển khai một hệ thống **Retrieval-Augmented Generation (RAG)** cấp độ sản xuất, tập trung vào tính chính xác, bảo mật và khả năng giám sát. Hệ thống kết hợp nền tảng tìm kiếm lai (Hybrid Search) từ Day 18 và các lớp bảo vệ (Guardrails), đánh giá tự động (RAGAS) từ Lab 24.

### Các thành phần chính:
1. **RAG Pipeline (Day 18)**:
   - **Chunking**: Phân mảnh tài liệu phân cấp và làm giàu ngữ cảnh.
   - **Hybrid Search**: Kết hợp BM25 và Vector Search (Qdrant).
   - **Reranking**: Sử dụng Cohere Cross-Encoder.
2. **Evaluation Layer (Phase A & B)**:
   - **RAGAS**: Đánh giá tự động Faithfulness, Relevancy, Precision/Recall.
   - **Judge Calibration**: Kiểm chứng độ tin cậy của Judge AI so với con người.
3. **Guardrails Layer (Phase C)**:
   - **Input Guards**: PII Redaction (Presidio) và Topic Validation.
   - **Output Guards**: Llama Guard 3.

## 🎯 Kết quả Lab 24
Dự án này đã hoàn thành việc xây dựng hệ thống đánh giá và phòng vệ cho RAG.

### Chỉ số thực tế:
- **RAGAS Score**: Faithfulness (0.52), Answer Relevancy (0.44), Context Precision (0.92).
- **Judge Reliability**: Cohen's Kappa **0.7368** (Substantial Agreement).
- **Safety**: 50.0% Blocking rate (Adversarial Accuracy).
- **Latency (Mean)**: ~3.5s (Input Guard: 877ms, RAG: 1671ms, Output Guard: 659ms).
- **P95 Latency**: ~5.2s (Đo lường thực tế trên 5 kịch bản).

### 🚀 Cách chạy kiểm thử nhanh:
1. **Eval (Phase A)**: `python lab24-eval-guardrails/phase-a/phase_a_run_eval.py`
2. **Calibration (Phase B)**: `python lab24-eval-guardrails/phase-b/phase_b_calibration.py`
3. **Adversarial (Phase C)**: `python lab24-eval-guardrails/phase-c/run_adversarial.py`

---

## 📂 Cấu trúc thư mục
```text
.
├── src/                        # Mã nguồn RAG Pipeline (Day 18)
├── data/                       # Dữ liệu tri thức (.md, .pdf)
├── lab24-eval-guardrails/      # Hệ thống Đánh giá & Bảo mật (Day 24)
│   ├── phase-a/                # RAGAS Eval & Synthetic Testset
│   ├── phase-b/                # LLM-as-a-Judge & Calibration
│   ├── phase-c/                # Guardrails & Latency Benchmark
│   ├── phase-d/                # Technical Blueprint
│   └── README.md               # Hướng dẫn chi tiết Lab 24
├── .github/workflows/          # CI/CD (Eval Gate)
└── README.md                   # File này
```

---

## 🛠️ Cài đặt & Sử dụng

### 1. Cài đặt môi trường
```bash
python -m venv venv
source venv/bin/activate  # Hoặc venv\Scripts\activate trên Windows
pip install -r requirements.txt
pip install ragas presidio-analyzer presidio-anonymizer scikit-learn groq
```

### 2. Cấu hình biến môi trường (.env)
Tạo file `.env` tại thư mục gốc:
```env
OPENAI_API_KEY=your_openai_key
COHERE_API_KEY=your_cohere_key
GROQ_API_KEY=your_groq_key
```

---

## 🧪 Hướng dẫn Kiểm thử (Testing Guide)

Bạn có thể kiểm tra từng thành phần của hệ thống bằng các câu lệnh sau:

### 1. Kiểm tra Pipeline RAG (Day 18)
Kiểm tra khả năng tìm kiếm và trả lời cơ bản:
```bash
python src/pipeline.py --query "Nghị định 13 quy định về điều gì?"
```

### 2. Đánh giá RAGAS (Phase A)
Sinh tập dữ liệu test và chạy đánh giá tự động:
```bash
# Sinh dữ liệu test (nếu chưa có)
python lab24-eval-guardrails/phase-a/phase_a_testset_gen.py

# Chạy đánh giá RAGAS
python lab24-eval-guardrails/phase-a/phase_a_run_eval.py
```
*Kết quả sẽ được lưu tại: `lab24-eval-guardrails/phase-a/ragas_results.csv`*

### 3. LLM-as-a-Judge (Phase B)
Chạy chấm điểm tuyệt đối và đo lường độ tin cậy của Judge:
```bash
# Chấm điểm tuyệt đối (Absolute Scoring)
python lab24-eval-guardrails/phase-b/phase_b_judge_absolute.py

# Tính chỉ số Cohen's Kappa (Calibration)
python lab24-eval-guardrails/phase-b/phase_b_calibration.py
```

### 4. Kiểm tra Guardrails (Phase C)
Chạy các kịch bản tấn công thử nghiệm (Adversarial Testing) và đo lường độ trễ:
```bash
# Chạy test tấn công (PII, Out-of-scope, Unsafe)
python lab24-eval-guardrails/phase-c/run_adversarial.py

# Chạy benchmark độ trễ hệ thống
python lab24-eval-guardrails/phase-c/run_benchmark.py
```
*Kết quả lưu tại: `lab24-eval-guardrails/phase-c/adversarial_test_results.csv`*

---

## 📊 Kết quả đánh giá tóm tắt
- **RAGAS Faithfulness**: 0.57 (Cần cải thiện prompt grounding)
- **Answer Relevancy**: 0.51
- **Guardrail Latency**: ~860ms (Input) + ~1300ms (Output)
- **Safety Gate**: Thành công ngăn chặn 50% các cuộc tấn công Adversarial (PII & Out-of-scope).
- **Judge Calibration**: Cohen's Kappa 0.0789 (Slight agreement).

---

## 🛡️ Bảo mật & SLOs
Hệ thống cam kết:
- **PII Leakage**: 0% đối với các thực thể định danh Việt Nam (CCCD, SĐT).
- **Latency**: P95 < 5 giây cho toàn bộ chu trình xử lý.
- **Safety**: Tự động chặn các yêu cầu vi phạm chính sách an toàn.

