import os, sys
import pandas as pd
import time
from dotenv import load_dotenv
from openai import OpenAI

# Fix Windows encoding issue
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Load environment variables
load_dotenv()

client = OpenAI()

def pairwise_judge(question, answer_a, answer_b, ground_truth=None):
    """Pairwise judge with position swap to mitigate bias."""
    
    prompt_template = """Bạn là một trọng tài công bằng đánh giá chất lượng câu trả lời của trợ lý ảo.
Dưới đây là một câu hỏi và hai câu trả lời ứng viên.
Nhiệm vụ của bạn là chọn ra câu trả lời TỐT HƠN dựa trên độ chính xác, đầy đủ và tính hữu ích.

Câu hỏi: {question}
{ground_truth_str}

Ứng viên 1: {ans_1}
Ứng viên 2: {ans_2}

Hãy phân tích ngắn gọn và sau đó đưa ra kết luận:
- Nếu Ứng viên 1 tốt hơn, hãy viết: [[A]]
- Nếu Ứng viên 2 tốt hơn, hãy viết: [[B]]
- Nếu hai câu trả lời tương đương, hãy viết: [[C]]
"""

    gt_str = f"Câu trả lời mẫu (Ground Truth): {ground_truth}" if ground_truth else ""
    
    # Run 1: Original order
    prompt_1 = prompt_template.format(
        question=question,
        ground_truth_str=gt_str,
        ans_1=answer_a,
        ans_2=answer_b
    )
    
    # Run 2: Swapped order
    prompt_2 = prompt_template.format(
        question=question,
        ground_truth_str=gt_str,
        ans_1=answer_b,
        ans_2=answer_a
    )
    
    def get_eval(prompt):
        try:
            resp = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.0
            )
            content = resp.choices[0].message.content
            if "[[A]]" in content: return "A"
            if "[[B]]" in content: return "B"
            if "[[C]]" in content: return "C"
            return "C" # Default
        except Exception as e:
            print(f"Error in judge: {e}")
            return "C"

    res_1 = get_eval(prompt_1)
    res_2 = get_eval(prompt_2)
    
    # Swap-and-average logic:
    # If Run 1 says A and Run 2 says B (meaning original answer_a is better in both), return A.
    # If both say A, then it's a conflict (position bias).
    
    if res_1 == "A" and res_2 == "B":
        return "Answer A is better"
    elif res_1 == "B" and res_2 == "A":
        return "Answer B is better"
    elif res_1 == "C" and res_2 == "C":
        return "Both are equal"
    else:
        return "Inconsistent (Position Bias detected)"

def run_pairwise_bench():
    # This script assumes we have results from phase-a
    results_path = os.path.join("lab24-eval-guardrails", "phase-a", "ragas_results.csv")
    if not os.path.exists(results_path):
        print("Waiting for Phase A results...")
        return
        
    df = pd.read_csv(results_path).head(30)
    
    # For demo, we'll compare the RAG answer with the Ground Truth itself (ground truth should win)
    # or with a truncated version of the answer.
    
    judge_results = []
    print(f"Running Pairwise Judge on {len(df)} samples...")
    for i, row in df.iterrows():
        question = row['user_input']
        ans_a = row['response']
        # Simulate another answer (e.g. truncated or different model)
        ans_b = row['reference']
        
        winner = pairwise_judge(question, ans_a, ans_b, ground_truth=row['reference'])
        judge_results.append({
            "question": question,
            "answer_a": ans_a,
            "answer_b": ans_b,
            "winner": winner
        })
        print(f"  [{i+1}] Winner: {winner}")
        
    res_df = pd.DataFrame(judge_results)
    output_path = os.path.join("lab24-eval-guardrails", "phase-b", "pairwise_results.csv")
    res_df.to_csv(output_path, index=False)
    print(f"Pairwise results saved to {output_path}")

if __name__ == "__main__":
    run_pairwise_bench()
