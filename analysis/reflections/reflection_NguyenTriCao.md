# Individual Reflection — Lab 18

**Tên:** Nguyễn Trí Cao  
**Module phụ trách:** M1, M2, M3, M4, M5 (Làm cá nhân)

---

## 1. Đóng góp kỹ thuật

- Module đã implement: Tất cả các module từ M1 đến M5.
- Các hàm/class chính đã viết: 
    - `chunk_hierarchical`, `chunk_semantic` (M1)
    - `HybridSearch`, `reciprocal_rank_fusion` (M2)
    - `CrossEncoderReranker` (M3)
    - `evaluate_ragas`, `failure_analysis` (M4)
    - `enrich_chunks`, `contextual_prepend` (M5)
- Số tests pass: 37/37

## 2. Kiến thức học được

- Khái niệm mới nhất: Kỹ thuật **Contextual Prepend** để giải quyết vấn đề mất ngữ cảnh khi chunking và thuật toán **RRF (Reciprocal Rank Fusion)** trong Hybrid Search.
- Điều bất ngờ nhất: Reranking là bước cực kỳ quan trọng giúp lọc nhiễu, Recall tăng mạnh (+33%) sau khi áp dụng đầy đủ pipeline.
- Kết nối với bài giảng (slide nào): Slide về Advanced Retrieval Strategies (Module 2) và RAG Evaluation Metrics (Module 4).

## 3. Khó khăn & Cách giải quyết

- Khó khăn lớn nhất: Debug các lỗi xung đột phiên bản của `ragas` và `pydantic`, cũng như xử lý các trường hợp LLM sinh ra câu trả lời không bám sát ngữ cảnh (hallucination).
- Cách giải quyết: Tinh chỉnh System Prompt, giảm `temperature` xuống 0.1 và sử dụng `gpt-4o-mini` để tối ưu chi phí trong quá trình đánh giá.
- Thời gian debug: ~4 giờ.

## 4. Nếu làm lại

- Sẽ làm khác điều gì: Sử dụng xử lý bất đồng bộ (Asyncio) cho Module 5 để làm giàu dữ liệu (Enrichment) nhanh hơn vì bước này gọi API LLM rất nhiều lần.
- Module nào muốn thử tiếp: Module 1 với kỹ thuật Semantic Chunking dựa trên embedding thay vì chỉ dùng regex đơn thuần.

## 5. Tự đánh giá

| Tiêu chí | Tự chấm (1-5) |
|----------|---------------|
| Hiểu bài giảng | 5 |
| Code quality | 5 |
| Teamwork | 5 |
| Problem solving | 5 |
