import os
import json
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

client = OpenAI()

class TopicGuard:
    def __init__(self, allowed_topics=["Tài chính", "Kế toán", "Pháp luật", "Báo cáo tài chính", "Dữ liệu cá nhân"]):
        self.allowed_topics = allowed_topics

    def is_in_scope(self, query):
        prompt = f"""Phân loại câu hỏi sau đây có thuộc các chủ đề: {', '.join(self.allowed_topics)} hay không.
Chỉ trả lời 'IN_SCOPE' nếu câu hỏi liên quan đến tài chính, kế toán, báo cáo tài chính hoặc quy định pháp luật (đặc biệt là bảo vệ dữ liệu).
Trả lời 'OUT_OF_SCOPE' nếu câu hỏi về các chủ đề khác (thời tiết, giải trí, nấu ăn, v.v.).

Câu hỏi: {query}

Kết quả (JSON): {{"classification": "...", "reason": "..."}}
"""
        try:
            resp = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.0,
                response_format={"type": "json_object"}
            )
            result = json.loads(resp.choices[0].message.content)
            return result.get("classification") == "IN_SCOPE", result.get("reason")
        except Exception as e:
            print(f"Error in topic guard: {e}")
            return True, "Error" # Fallback to allow

def test_topic():
    guard = TopicGuard()
    test_inputs = [
        "Cách xem báo cáo lưu chuyển tiền tệ?",
        "Nghị định 13 quy định gì về bảo vệ dữ liệu?",
        "Thời tiết hôm nay thế nào?",
        "Làm thế nào để nấu món phở ngon?",
        "Quy định về xử phạt vi phạm hành chính trong lĩnh vực kế toán?"
    ]
    
    print("Testing Topic Guardrail...")
    for text in test_inputs:
        in_scope, reason = guard.is_in_scope(text)
        print(f"Query: {text}")
        print(f"Result: {'PASS' if in_scope else 'BLOCK'} ({reason})")
        print("-" * 20)

if __name__ == "__main__":
    test_topic()
