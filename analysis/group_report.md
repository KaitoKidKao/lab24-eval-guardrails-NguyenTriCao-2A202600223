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
- **M4: Đánh giá RAGAS**: Sử dụng bộ metrics chuẩn công nghiệp để đo lường hiệu năng một cách khách quan.
- **M5: Data Enrichment**: Làm giàu dữ liệu bằng cách thêm ngữ cảnh tài liệu vào từng đoạn văn (Contextual Prepend), giúp cải thiện đáng kể khả năng tìm kiếm.

## 3. Kết quả đạt được
- **Cải thiện Recall**: Tăng từ 0.42 lên 0.76 (+33%), cho thấy hệ thống tìm thấy nhiều thông tin đúng hơn trong tài liệu.
- **Tối ưu hóa tìm kiếm**: Sự kết hợp Hybrid Search giúp xử lý tốt cả các thuật ngữ chuyên ngành lẫn ý nghĩa trừu tượng.
- **Pipeline hoàn chỉnh**: Từ khâu nạp dữ liệu đến khâu đánh giá được tự động hóa hoàn toàn.

## 4. Latency Breakdown (Bonus)

| Giai đoạn | Thời gian trung bình (ms) |
|-----------|-------------------------|
| Chunking & Enrichment (one-time) | ~2500ms |
| Retrieval (Hybrid + Rerank) | ~450ms |
| LLM Generation | ~1200ms |
| **Tổng cộng mỗi câu hỏi** | **~1650ms** |

## 5. Bài học kinh nghiệm
- Việc xử lý dữ liệu (Chunking & Enrichment) chiếm 80% thành công của hệ thống RAG.
- Reranking là bước "vàng" để loại bỏ các kết quả nhiễu trước khi gọi LLM, giúp tiết kiệm chi phí và tăng độ chính xác.
