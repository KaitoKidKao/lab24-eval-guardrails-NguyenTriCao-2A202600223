import os, sys
import pandas as pd
from dotenv import load_dotenv

# Fix Windows encoding issue
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Add paths
sys.path.insert(0, os.path.join(os.getcwd(), "lab24-eval-guardrails", "phase-c"))
from input_guard_pii import PIIGuard
from input_guard_topic import TopicGuard

load_dotenv()

def run_adversarial_tests():
    print("Running adversarial tests...")
    df = pd.read_csv("lab24-eval-guardrails/phase-c/adversarial_test_inputs.csv")
    pii_guard = PIIGuard()
    topic_guard = TopicGuard()
    
    results = []
    for _, row in df.iterrows():
        input_text = row['input']
        expected = row['expected_action']
        
        # Check PII
        redacted, pii_detected = pii_guard.process(input_text)
        
        # Check Topic
        in_scope, topic_reason = topic_guard.is_in_scope(input_text)
        
        action = "PASS"
        if pii_detected:
            action = "REDACT"
        if not in_scope:
            action = "BLOCK"
            
        results.append({
            "category": row['category'],
            "input": input_text,
            "expected_action": expected,
            "actual_action": action,
            "pii_detected": pii_detected,
            "in_scope": in_scope,
            "match": expected == action
        })
    
    res_df = pd.DataFrame(results)
    res_df.to_csv("lab24-eval-guardrails/phase-c/adversarial_test_results.csv", index=False)
    print("Results saved to lab24-eval-guardrails/phase-c/adversarial_test_results.csv")
    print(f"Accuracy: {res_df['match'].mean() * 100:.1f}%")

if __name__ == "__main__":
    run_adversarial_tests()
