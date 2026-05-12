import re
from presidio_analyzer import AnalyzerEngine, PatternRecognizer, Pattern
from presidio_anonymizer import AnonymizerEngine

class PIIGuard:
    def __init__(self):
        self.analyzer = AnalyzerEngine()
        self.anonymizer = AnonymizerEngine()
        
        # Add Vietnamese specific patterns
        # 1. CCCD (Citizen ID) - 12 digits
        cccd_pattern = Pattern(name="cccd", regex=r"\b\d{12}\b", score=0.8)
        cccd_recognizer = PatternRecognizer(supported_entity="VN_CCCD", patterns=[cccd_pattern])
        self.analyzer.registry.add_recognizer(cccd_recognizer)
        
        # 2. VN Phone Number
        phone_pattern = Pattern(name="vn_phone", regex=r"\b(0|84)(3|5|7|8|9)\d{8}\b", score=0.8)
        phone_recognizer = PatternRecognizer(supported_entity="VN_PHONE", patterns=[phone_pattern])
        self.analyzer.registry.add_recognizer(phone_recognizer)

    def process(self, text):
        # Analyze
        results = self.analyzer.analyze(text=text, language='en', entities=["PHONE_NUMBER", "EMAIL_ADDRESS", "PERSON", "VN_CCCD", "VN_PHONE"])
        
        # Anonymize
        anonymized_result = self.anonymizer.anonymize(
            text=text,
            analyzer_results=results
        )
        
        return anonymized_result.text, len(results) > 0

def test_pii():
    guard = PIIGuard()
    test_inputs = [
        "Chào tôi là Nguyễn Văn A, số điện thoại của tôi là 0912345678.",
        "Gửi mail cho tôi tại abc@gmail.com nhé.",
        "Số CCCD của tôi là 012345678901.",
        "Câu hỏi này không có thông tin cá nhân."
    ]
    
    results = []
    print("Testing PII Guardrail...")
    for text in test_inputs:
        redacted, detected = guard.process(text)
        results.append({
            "original": text,
            "redacted": redacted,
            "pii_detected": detected
        })
        print(f"Original: {text}")
        print(f"Redacted: {redacted}")
        print("-" * 20)
        
    import pandas as pd
    df = pd.DataFrame(results)
    df.to_csv("lab24-eval-guardrails/phase-c/pii_test_results.csv", index=False)
    print("Results saved to phase-c/pii_test_results.csv")

if __name__ == "__main__":
    test_pii()
