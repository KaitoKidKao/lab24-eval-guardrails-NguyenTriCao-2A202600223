# Individual Reflection — Lab 18

**Tên:** Nguyễn Trí Cao  
**Module phụ trách:** M1, M2, M3, M4, M5 (Toàn bộ Pipeline)

---

## 1. Đóng góp kỹ thuật

- **Module đã implement**: Đã hoàn thành 100% các module từ M1 đến M5, tích hợp đầy đủ Cohere Reranker và Hybrid Search.
- **Các điểm nhấn kỹ thuật**:
    - Xây dựng hệ thống Hybrid Search kết hợp BM25 và Vector Search thông qua RRF.
    - Triển khai **Contextual Prepend (M5)** giúp hệ thống đạt độ chính xác (Precision) và khả năng tìm kiếm (Recall) vượt trội.
    - Thiết lập hệ thống đánh giá tự động bằng RAGAS với 15 test cases chất lượng cao.
- **Bonus Implementation**: Tự tay triển khai báo cáo **Latency Breakdown** chi tiết và tối ưu **Faithfulness đạt 0.90**.

## 2. Kiến thức học được

- **Tầm quan trọng của Reranking**: Học được rằng Reranking là "vùng đệm" quan trọng nhất để loại bỏ nhiễu trước khi LLM sinh câu trả lời, giúp tiết kiệm token và tăng độ chính xác.
- **Evaluation driven development**: Thay vì chỉ code "mò", việc dùng RAGAS giúp tôi biết chính xác module nào đang yếu (ví dụ: Faithfulness thấp do Prompt chưa chuẩn) để sửa đổi có mục đích.
- **Data Enrichment**: Kỹ thuật làm giàu dữ liệu giúp giải quyết triệt để vấn đề "mất ngữ cảnh" khi tài liệu bị chia nhỏ.

## 3. Khó khăn & Cách giải quyết

- **Khó khăn**: Lỗi Rate Limit của Cohere Trial Key (chỉ cho phép 10 calls/min) khi chạy đánh giá 15 câu hỏi cùng lúc.
- **Cách giải quyết**: Triển khai cơ chế **throttling (time.sleep)** thông minh trong vòng lặp đánh giá để đảm bảo pipeline chạy ổn định mà không bị crash. Đồng thời tinh chỉnh `temperature=0.0` để tối ưu tính trung thực của câu trả lời.
- **Debug**: Xử lý các lỗi Unicode trên môi trường Windows terminal khi in các ký tự tiếng Việt.

## 4. Nếu làm lại

- **Tối ưu hiệu năng**: Tôi sẽ sử dụng `ThreadPoolExecutor` để chạy song song các bước nạp dữ liệu (Indexing) và làm giàu dữ liệu (Enrichment) nhằm giảm thời gian chuẩn bị ban đầu.
- **Mở rộng**: Thử nghiệm thêm module **Agentic RAG** để hệ thống có thể tự quyết định khi nào cần tra cứu thêm thông tin nếu câu trả lời ban đầu chưa đủ độ tin cậy.

## 5. Tự đánh giá

| Tiêu chí | Tự chấm (1-5) | Ghi chú |
|----------|---------------|---------|
| Hiểu bài giảng | 5 | Nắm vững các kỹ thuật Advanced RAG |
| Code quality | 5 | Code sạch, có comment đầy đủ, xử lý lỗi tốt |
| Hoàn thành yêu cầu | 5 | Hoàn thành 100% + Full Bonus |
| Problem solving | 5 | Giải quyết tốt lỗi Rate Limit và Unicode Windows |
