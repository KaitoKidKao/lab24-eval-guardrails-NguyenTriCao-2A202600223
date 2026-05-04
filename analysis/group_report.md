# Báo cáo Nhóm - Production RAG Pipeline
**Thực hiện bởi:** Nguyễn Trí Cao

## Thành viên & Module

| Tên | Module | Hoàn thành | Tests pass |
|-----|--------|-----------|-----------|
| Nguyễn Trí Cao | M1: Chunking | ☑ | 13/13 |
| Nguyễn Trí Cao | M2: Search | ☑ | 5/5 |
| Nguyễn Trí Cao | M3: Rerank | ☑ | 5/5 |
| Nguyễn Trí Cao | M4: Eval | ☑ | 4/4 |
| Nguyễn Trí Cao | M5: Enrichment | ☑ | 10/10 |

## 1. Giới thiệu
Dự án nhằm xây dựng một hệ thống RAG (Retrieval-Augmented Generation) chất lượng cao, có khả năng xử lý các tài liệu phức tạp (Nghị định Chính phủ, Báo cáo tài chính). Hệ thống vượt qua các hạn chế của RAG cơ bản bằng cách áp dụng các kỹ thuật tiên tiến trong tìm kiếm và xử lý dữ liệu.

## 2. Kiến trúc Hệ thống
Hệ thống bao gồm 5 module cốt lõi:
- **M1: Chunking phân cấp**: Chia tài liệu thành các đoạn lớn (Parent) và nhỏ (Child) để cân bằng giữa ngữ cảnh và độ chi tiết.
- **M2: Hybrid Search**: Kết hợp BM25 (tìm kiếm từ khóa) và Dense Vector (tìm kiếm ngữ nghĩa) thông qua thuật toán Reciprocal Rank Fusion (RRF).
- **M3: Cohere Reranking**: Sử dụng Cross-Encoder để xếp hạng lại top kết quả, đảm bảo tính liên quan cao nhất trước khi đưa vào LLM.
- **M4: Đánh giá RAGAS**: Sử dụng bộ metrics chuẩn công nghiệp (Faithfulness, Relevancy, Precision, Recall).
- **M5: Data Enrichment**: Triển khai **Contextual Prepend** - tự động thêm tóm tắt tài liệu và metadata vào từng chunk, giúp LLM luôn nắm bắt được ngữ cảnh tổng thể.

## 3. Các điểm Bonus đã triển khai (Total +10đ)
- **[+5đ] High-Quality Faithfulness**: Tối ưu hóa Generation và Prompt giúp hệ thống đạt điểm **Faithfulness = 0.9000** (Vượt mốc 0.85).
- **[+3đ] M5 Enrichment**: Tích hợp pipeline làm giàu dữ liệu tự động, giải quyết vấn đề "mất ngữ cảnh" của các chunk nhỏ.
- **[+2đ] Latency Breakdown**: Triển khai báo cáo thời gian thực hiện chi tiết cho từng giai đoạn của Pipeline.

## 4. Latency Breakdown (Thực tế)
Dưới đây là bảng phân rã thời gian xử lý trung bình cho mỗi câu hỏi (dựa trên 15 test cases):

| Giai đoạn | Thời gian trung bình (ms) | Tỷ trọng |
|-----------|-------------------------|----------|
| **1. Retrieval** | 369.8 ms | 16% |
| **2. Reranking** | 394.4 ms | 17% |
| **3. Generation**| 1534.9 ms | 67% |
| **Tổng cộng** | **2299.1 ms** | **100%** |

*Nhận xét: Phần lớn thời gian nằm ở bước Generation của LLM. Tốc độ Retrieval và Reranking cực kỳ nhanh, phù hợp cho môi trường Production thực tế.*

## 5. Kết quả & Bài học kinh nghiệm
- Việc xử lý dữ liệu (Chunking & Enrichment) chiếm 80% thành công của hệ thống RAG.
- **Cohere Reranker** là "cứu cánh" quan trọng nhất để cải thiện Context Precision, đặc biệt là với các tài liệu có cấu trúc phức tạp như Báo cáo tài chính.
- Hệ thống đã đạt trạng thái sẵn sàng cho Production với độ tin cậy cao.
