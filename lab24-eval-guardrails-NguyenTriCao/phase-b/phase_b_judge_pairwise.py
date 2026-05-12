import os, sys, json, time
import pandas as pd
from dotenv import load_dotenv
from openai import OpenAI

# Fix Windows encoding issue
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

load_dotenv()
client = OpenAI()

def get_json_eval(prompt):
    """Helper to get and parse JSON response from LLM."""
    try:
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Bạn là một trọng tài đánh giá câu trả lời. Chỉ trả về JSON duy nhất."},
                {"role": "user", "content": prompt}
            ],
            response_format={ "type": "json_object" },
            temperature=0.0
        )
        data = json.loads(resp.choices[0].message.content)
        # Standardize winner to A, B, or tie
        winner = str(data.get("winner", "tie")).upper()
        if "1" in winner or "A" in winner: winner = "A"
        elif "2" in winner or "B" in winner: winner = "B"
        else: winner = "tie"
        return winner, data.get("reason", "No reason provided")
    except Exception as e:
        print(f"Error parsing JSON: {e}")
        return "tie", str(e)

def pairwise_judge_swap(question, answer_a, answer_b, ground_truth=None):
    prompt_template = """Đánh giá hai câu trả lời cho câu hỏi sau.
Câu hỏi: {question}
Câu trả lời mẫu: {ground_truth}

Ứng viên 1: {ans_1}
Ứng viên 2: {ans_2}

Hãy so sánh và chọn người chiến thắng. 
Trả về JSON format: {{"winner": "1" hoặc "2" hoặc "tie", "reason": "giải thích ngắn gọn"}}
"""

    # Run 1: Original (1=A, 2=B)
    p1 = prompt_template.format(question=question, ground_truth=ground_truth, ans_1=answer_a, ans_2=answer_b)
    run1_winner_raw, reason1 = get_json_eval(p1)
    
    # Map raw winner back to A/B
    run1_winner = "A" if run1_winner_raw == "A" else ("B" if run1_winner_raw == "B" else "tie")

    # Run 2: Swapped (1=B, 2=A)
    p2 = prompt_template.format(question=question, ground_truth=ground_truth, ans_1=answer_b, ans_2=answer_a)
    run2_winner_raw, reason2 = get_json_eval(p2)
    
    # Map raw winner back to A/B (If winner is 1 (B), then it's B. If winner is 2 (A), then it's A)
    run2_winner = "B" if run2_winner_raw == "A" else ("A" if run2_winner_raw == "B" else "tie")

    # Logic Swap-and-average
    if run1_winner == run2_winner:
        final_winner = run1_winner
    else:
        final_winner = "tie" # Conflict or actual tie
        
    return final_winner, run1_winner, run2_winner

def run_bench():
    results_path = os.path.join("lab24-eval-guardrails", "phase-a", "ragas_results.csv")
    if not os.path.exists(results_path):
        print("Error: ragas_results.csv not found.")
        return

    df = pd.read_csv(results_path).head(30) # Chạy trên ít nhất 30 questions
    if len(df) < 30:
        print(f"Warning: Only found {len(df)} samples in CSV. Running on all available.")

    final_data = []
    print(f"Starting Pairwise Bench on {len(df)} samples...")
    
    for i, row in df.iterrows():
        q = row['user_input']
        a = row['response']
        ref = row['reference']
        
        winner_swap, r1_win, r2_win = pairwise_judge_swap(q, a, ref, ground_truth=ref)
        
        final_data.append({
            "question": q,
            "winner_after_swap": winner_swap,
            "run1_winner": r1_win,
            "run2_winner": r2_win
        })
        print(f"[{i+1}] {winner_swap} (R1:{r1_win}, R2:{r2_win})")

    out_df = pd.DataFrame(final_data)
    out_path = os.path.join("lab24-eval-guardrails", "phase-b", "pairwise_results.csv")
    out_df.to_csv(out_path, index=False, encoding='utf-8-sig')
    print(f"\nSaved {len(out_df)} results to {out_path}")

if __name__ == "__main__":
    run_bench()
