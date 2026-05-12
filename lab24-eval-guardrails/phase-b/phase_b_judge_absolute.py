import os, sys
import pandas as pd
import json
from dotenv import load_dotenv
from openai import OpenAI

# Fix Windows encoding issue
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Load environment variables
load_dotenv()

client = OpenAI()

def absolute_scoring(question, answer, ground_truth=None):
    """Absolute scoring (G-Eval style) on a scale of 1-5."""
    
    prompt = f"""Bạn là một chuyên gia đánh giá chất lượng RAG. 
Hãy đánh giá câu trả lời sau đây dựa trên thang điểm từ 1 đến 5.

Tiêu chí:
1: Rất tệ - Hoàn toàn sai hoặc không liên quan.
2: Tệ - Có nhiều lỗi sai hoặc thiếu sót nghiêm trọng.
3: Trung bình - Trả lời được ý chính nhưng còn thiếu chi tiết hoặc cách diễn đạt chưa tốt.
4: Tốt - Chính xác và đầy đủ, chỉ có lỗi nhỏ không đáng kể.
5: Xuất sắc - Hoàn hảo, chính xác, đầy đủ và trình bày chuyên nghiệp.

Câu hỏi: {question}
Câu trả lời mẫu (Ground Truth): {ground_truth if ground_truth else "N/A"}
Câu trả lời cần đánh giá: {answer}

Hãy đưa ra điểm số (1-5) theo định dạng JSON:
{{"reasoning": "...", "score": X}}
"""

    try:
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.0,
            response_format={"type": "json_object"}
        )
        result = json.loads(resp.choices[0].message.content)
        return result.get("score", 0), result.get("reasoning", "")
    except Exception as e:
        print(f"Error in absolute judge: {e}")
        return 0, str(e)

def run_absolute_bench():
    results_path = os.path.join("lab24-eval-guardrails", "phase-a", "ragas_results.csv")
    if not os.path.exists(results_path):
        print("Waiting for Phase A results...")
        return
        
    df = pd.read_csv(results_path).head(30)
    
    scores = []
    print(f"Running Absolute Scoring on {len(df)} samples...")
    for i, row in df.iterrows():
        question = row['user_input']
        answer = row['response']
        gt = row['reference']
        
        score, reasoning = absolute_scoring(question, answer, ground_truth=gt)
        scores.append({
            "question": question,
            "answer": answer,
            "score": score,
            "reasoning": reasoning
        })
        print(f"  [{i+1}] Score: {score}")
        
    res_df = pd.DataFrame(scores)
    output_path = os.path.join("lab24-eval-guardrails", "phase-b", "absolute_scores.csv")
    res_df.to_csv(output_path, index=False)
    print(f"Absolute scores saved to {output_path}")

if __name__ == "__main__":
    run_absolute_bench()
