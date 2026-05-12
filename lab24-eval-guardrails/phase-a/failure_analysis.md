# Phase A.3: Failure Cluster Analysis

## 1. Bottom 10 Questions Analysis
Dưới đây là danh sách 10 câu hỏi có kết quả tệ nhất (điểm Faithfulness hoặc Relevancy = 0), trích xuất từ đợt chạy 50+ samples.

| ID | Câu hỏi (User Input) | Faithfulness | Relevancy | Context Recall | Vấn đề chính |
|:---|:---|:---:|:---:|:---:|:---|
| 4 | Bộ trưởng Bộ Công an là ai và có vai trò gì... | 0.0 | 0.0 | 0.66 | LLM không trích xuất được thông tin cụ thể từ ngữ cảnh pháp lý |
| 14 | Luật bảo vệ dữ liệu cá nhân là gì... | 0.0 | 0.0 | 0.66 | Câu hỏi định nghĩa rộng, LLM báo không tìm thấy |
| 26 | Tại sao việc cung cấp dữ liệu cá nhân không được phép... | 0.0 | 0.0 | 1.0 | Context có thông tin nhưng LLM từ chối trả lời |
| 45 | What are the responsibilities of the data transfer party... | 0.0 | 0.0 | 0.33 | Câu hỏi tiếng Anh, Context tiếng Việt (Cross-lingual failure) |
| 46 | Nghị định này có những biện pháp bảo vệ dữ liệu nào? | 0.0 | 0.0 | 0.60 | Retrieval lấy được mảnh lẻ, không tổng hợp được toàn bộ biện pháp |
| 68 | What are the implications for data controllers... | 0.0 | 0.0 | 0.50 | Lỗi logic khi kết hợp thông tin giữa Điều 13 và Điều 14 |
| 70 | What are the requirements for transferring... | 0.0 | 0.0 | 0.50 | Không xử lý được query tiếng Anh trên tập dữ liệu tiếng Việt |
| 81 | What constitutes personal data according to Decree 13... | 0.0 | 0.0 | 0.33 | Thuật ngữ tiếng Anh không khớp với vector của văn bản tiếng Việt |
| 82 | Nghị định quy định trách nhiệm của Bộ Thông tin... | 0.0 | 0.0 | 0.50 | Trả lời sai do context bị cắt vụn (Chunking issues) |
| 102| What are the requirements for the Hồ sơ đánh giá... | 0.0 | 0.0 | 0.37 | Mất thông tin chi tiết trong quá trình nén context |

---

## 2. Identified Failure Clusters

### Cluster 1: Cross-Lingual Semantic Gap (English Query -> Vietnamese Context)
*   **Symptom**: Điểm Relevancy và Faithfulness bằng 0 cho hầu hết các câu hỏi bằng tiếng Anh, mặc dù Context Recall vẫn có (LLM báo "Tôi không tìm thấy thông tin").
*   **Example Questions**:
    *   *Question 45*: "What are the responsibilities of the data transfer party..."
    *   *Question 81*: "What constitutes personal data according to Decree No. 13/2023/NĐ-CP..."
*   **Root Cause**: Mismatch giữa không gian vector của query (English) và documents (Vietnamese). Mặc dù model Embedding có hỗ trợ đa ngôn ngữ, nhưng LLM (Judge) gặp khó khăn khi đối chiếu Fact giữa hai ngôn ngữ khác nhau trong bước verify faithfulness.
*   **Proposed Technical Fix**: 
    1.  Triển khai **Query Translation Layer**: Sử dụng một LLM nhẹ để dịch query sang tiếng Việt trước khi tiến hành Retrieval.
    2.  Nâng cấp Reranker lên **Cohere-rerank-v3-multilingual** để chuẩn hóa điểm số tương đồng xuyên ngôn ngữ.

### Cluster 2: Global Context & Definitional Synthesis Failure
*   **Symptom**: Context Precision cao (lấy đúng đoạn chứa từ khóa) nhưng Context Recall thấp hoặc Faithfulness thấp cho các câu hỏi mang tính định nghĩa hoặc bao quát.
*   **Example Questions**:
    *   *Question 14*: "Luật bảo vệ dữ liệu cá nhân là gì và nó có những điều khoản nào quan trọng..."
    *   *Question 46*: "Nghị định này có những biện pháp bảo vệ dữ liệu cá nhân nào?"
*   **Root Cause**: Chiến lược **Naive Chunking (Fixed-size)** làm phân mảnh các danh sách hoặc định nghĩa dài (ví dụ: một danh sách 10 biện pháp bị chia làm 3 chunks). LLM chỉ nhận được 1-2 chunks lẻ nên báo thiếu thông tin.
*   **Proposed Technical Fix**:
    1.  Áp dụng **Parent Document Retrieval (PDR)**: Lưu trữ các child chunks nhỏ để retrieval chính xác nhưng trả về Parent Chunk (toàn bộ Điều hoặc Chương) cho LLM để có đủ ngữ cảnh tổng hợp.
    2.  Tăng `window_size` trong quá trình trích xuất tài liệu từ Markdown để giữ nguyên cấu trúc List/Table.

---

## 3. Conclusion
Hệ thống hiện tại mạnh về việc tìm kiếm từ khóa (Keyword matching) nhưng yếu trong việc hiểu ý nghĩa xuyên ngôn ngữ và tổng hợp thông tin bao quát. Việc cải thiện cấu trúc Chunking và thêm lớp Translation cho Query là ưu tiên hàng đầu để nâng điểm Faithfulness.
