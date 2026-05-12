# Production RAG System: Evaluation & Guardrails

## Thông tin sinh viên
- **Họ và tên**: Nguyễn Trí Cao
- **MSSV**: 2A202600223
- **Lớp**: AICB-P2T3
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

### 3. Chạy thử nghiệm
- **Đánh giá RAGAS**: `python lab24-eval-guardrails/phase-a/phase_a_run_eval.py`
- **Kiểm tra Guardrails**: `python lab24-eval-guardrails/phase-c/run_adversarial.py`
- **Đo lường Latency**: `python lab24-eval-guardrails/phase-c/run_benchmark.py`

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
