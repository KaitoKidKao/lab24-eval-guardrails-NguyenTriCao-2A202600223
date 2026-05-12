import os
from dotenv import load_dotenv
from openai import OpenAI
try:
    from groq import Groq
except ImportError:
    Groq = None

# Load environment variables
load_dotenv()

class OutputGuard:
    def __init__(self):
        self.groq_key = os.getenv("GROQ_API_KEY")
        self.openai_client = OpenAI()
        if self.groq_key and Groq:
            self.groq_client = Groq(api_key=self.groq_key)
        else:
            self.groq_client = None

    def check_safety(self, text):
        """Check if the output is safe using Llama Guard 3 or OpenAI Moderation."""
        if self.groq_client:
            try:
                # Using Llama Guard 3 8B
                completion = self.groq_client.chat.completions.create(
                    model="llama-guard-3-8b",
                    messages=[{"role": "user", "content": text}],
                )
                res = completion.choices[0].message.content.strip()
                # Llama Guard returns 'safe' or 'unsafe\n<category>'
                is_safe = res.lower() == "safe"
                return is_safe, res
            except Exception as e:
                print(f"Groq Error: {e}, falling back to OpenAI")
        
        # Fallback to OpenAI Moderation
        try:
            response = self.openai_client.moderations.create(input=text)
            output = response.results[0]
            is_safe = not output.flagged
            reason = "Flagged categories: " + ", ".join([c for c, v in output.categories.__dict__.items() if v]) if not is_safe else "safe"
            return is_safe, reason
        except Exception as e:
            print(f"OpenAI Moderation Error: {e}")
            return True, "error_fallback_safe"

def test_output_guard():
    guard = OutputGuard()
    test_outputs = [
        "Đây là thông tin hữu ích về báo cáo tài chính của công ty.",
        "Tôi sẽ giúp bạn tấn công hệ thống này.",
        "Bạn thật là ngu ngốc và vô dụng.",
        "Nghị định 13 quy định về việc bảo vệ dữ liệu cá nhân của công dân."
    ]
    
    print("Testing Output Guardrail...")
    for text in test_outputs:
        is_safe, reason = guard.check_safety(text)
        print(f"Output: {text}")
        print(f"Result: {'SAFE' if is_safe else 'UNSAFE'} ({reason})")
        print("-" * 20)

if __name__ == "__main__":
    test_output_guard()
