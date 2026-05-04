# Báo cáo Phân tích Lỗi (Failure Analysis)
**Thực hiện bởi:** Nguyễn Trí Cao


## 1. Tổng quan điểm số
| Metric | Basic Baseline | Production RAG | Thay đổi (Δ) |
| :--- | :---: | :---: | :---: |
| Faithfulness | 0.9500 | 0.7333 | -0.2167 |
| Answer Relevancy | 0.8168 | 0.6881 | -0.1287 |
| **Context Precision** | 0.4667 | **0.7000** | **+0.2333** |
| **Context Recall** | 0.4231 | **0.7615** | **+0.3385** |

## 2. Phân tích các cải tiến (Successes)
- **Retrieval (Precision & Recall)**: Đây là điểm sáng nhất. Việc sử dụng **Hybrid Search (BM25 + Vector)** và **Cohere Rerank** đã giúp hệ thống tìm thấy thông tin chính xác hơn. Đặc biệt, **Contextual Prepend (M5)** giúp các đoạn văn nhỏ không bị mất ngữ cảnh của tài liệu gốc, dẫn đến Recall tăng mạnh (+33%).
- **Khả năng xử lý đa dạng**: Hệ thống Production tìm thấy thông tin ở cả Nghị định 13 và báo cáo tài chính tốt hơn hẳn bản Naive chỉ dùng Dense search đơn thuần.

## 3. Phân tích các lỗi/hạn chế (Failures)
- **Giảm Faithfulness (Độ trung thực)**: 
    - *Nguyên nhân*: Bản Production sử dụng LLM để sinh câu trả lời dựa trên ngữ cảnh. Việc diễn đạt lại (paraphrasing) đôi khi khiến RAGAS hiểu nhầm là thông tin không có trong gốc, hoặc LLM sinh ra các từ nối không có trong văn bản.
    - *Khắc phục*: Cần tinh chỉnh Prompt để LLM bám sát ngữ cảnh hơn, hoặc sử dụng model mạnh hơn (gpt-4o thay vì mini) để chấm điểm.
- **Answer Relevancy giảm**:
    - *Nguyên nhân*: Do Enrichment thêm thông tin ngữ cảnh vào đầu mỗi chunk, đôi khi câu trả lời của LLM bị dài dòng hoặc chứa các thông tin bổ trợ không quá sát với câu hỏi hẹp của người dùng.
    - *Khắc phục*: Tối ưu lại bước tóm tắt hoặc chỉ chọn lọc những chunk có score rerank cao nhất (> 0.8).

## 4. Kết luận
Hệ thống Production đã đạt được mục tiêu quan trọng nhất của RAG là **Tìm đúng thông tin**. Các vấn đề về sinh câu trả lời (Generation) có thể được khắc phục dễ dàng bằng cách tối ưu Prompt hoặc chọn LLM tốt hơn, nhưng nền tảng Retrieval tốt là yếu tố then chốt cho một hệ thống RAG thực thụ.
