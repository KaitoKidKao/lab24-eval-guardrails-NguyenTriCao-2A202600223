# Production RAG System: Evaluation & Guardrails

## Thông tin sinh viên
- **Họ và tên**: Nguyễn Trí Cao
- **MSSV**: 2A202600223
- **Repository**: [lab24-eval-guardrails-NguyenTriCao](https://github.com/KaitoKidKao/lab24-eval-guardrails-NguyenTriCao-2A202600223)

---

## 🌟 Tổng quan dự án
Dự án này triển khai một hệ thống **Retrieval-Augmented Generation (RAG)** cấp độ sản xuất, tập trung vào tính chính xác, bảo mật và khả năng giám sát. Hệ thống kết hợp nền tảng tìm kiếm lai (Hybrid Search) từ Day 18 và các lớp bảo vệ (Guardrails), đánh giá tự động (RAGAS) từ Lab 24.

### Các thành phần chính:
1. **RAG Pipeline (Day 18)**:
   - **Chunking**: Phân mảnh tài liệu phân cấp (Hierarchical) và làm giàu ngữ cảnh (Context Enrichment).
   - **Hybrid Search**: Kết hợp BM25 và Vector Search (Qdrant).
   - **Reranking**: Sử dụng Cohere Cross-Encoder để tối ưu kết quả tìm kiếm.
2. **Evaluation Layer (Phase A & B)**:
   - **RAGAS**: Đánh giá tự động các chỉ số Faithfulness, Answer Relevancy, Context Precision/Recall.
   - **LLM-as-a-Judge**: Hệ thống chấm điểm tuyệt đối (Absolute) và so sánh cặp (Pairwise) có khử nhiễu positional bias.
3. **Guardrails Layer (Phase C)**:
   - **Input Guards**: Kiểm soát thông tin nhạy cảm (PII Redaction) và kiểm tra phạm vi câu hỏi (Topic Validation).
   - **Output Guards**: Lọc nội dung không an toàn bằng Llama Guard 3.

---

## 📂 Cấu trúc thư mục
```text
.
├── src/                        # Mã nguồn RAG Pipeline (Day 18)
├── data/                       # Dữ liệu tri thức (.md, .pdf)
├── lab24-eval-guardrails-NguyenTriCao/      # Hệ thống Đánh giá & Bảo mật (Day 24)
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
python lab24-eval-guardrails-NguyenTriCao/phase-a/phase_a_testset_gen.py

# Chạy đánh giá RAGAS
python lab24-eval-guardrails-NguyenTriCao/phase-a/phase_a_run_eval.py
```
*Kết quả sẽ được lưu tại: `lab24-eval-guardrails-NguyenTriCao/phase-a/ragas_results.csv`*

### 3. LLM-as-a-Judge (Phase B)
Chạy chấm điểm tuyệt đối và đo lường độ tin cậy của Judge:
```bash
# Chấm điểm tuyệt đối (Absolute Scoring)
python lab24-eval-guardrails-NguyenTriCao/phase-b/phase_b_judge_absolute.py

# Tính chỉ số Cohen's Kappa (Calibration)
python lab24-eval-guardrails-NguyenTriCao/phase-b/phase_b_calibration.py
```

### 4. Kiểm tra Guardrails (Phase C)
Chạy các kịch bản tấn công thử nghiệm (Adversarial Testing) và đo lường độ trễ:
```bash
# Chạy test tấn công (PII, Out-of-scope, Unsafe)
python lab24-eval-guardrails-NguyenTriCao/phase-c/run_adversarial.py

# Chạy benchmark độ trễ hệ thống
python lab24-eval-guardrails-NguyenTriCao/phase-c/run_benchmark.py
```
*Kết quả lưu tại: `lab24-eval-guardrails-NguyenTriCao/phase-c/adversarial_test_results.csv`*

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

---
© 2026 Nguyễn Trí Cao. All rights reserved.
