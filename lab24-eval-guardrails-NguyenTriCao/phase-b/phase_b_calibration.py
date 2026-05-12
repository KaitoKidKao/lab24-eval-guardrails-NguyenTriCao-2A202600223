import os, sys
import pandas as pd
from sklearn.metrics import cohen_kappa_score

# Fix Windows encoding issue
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def compute_calibration():
    absolute_scores_path = os.path.join("lab24-eval-guardrails", "phase-b", "absolute_scores.csv")
    human_labels_path = os.path.join("lab24-eval-guardrails", "phase-b", "human_labels.csv")
    
    if not os.path.exists(absolute_scores_path) or not os.path.exists(human_labels_path):
        print("Waiting for scores and labels...")
        return
        
    df_llm = pd.read_csv(absolute_scores_path)
    df_human = pd.read_csv(human_labels_path)
    
    # Merge and align first 10 samples
    df_human = df_human.head(10)
    llm_scores = df_llm['score'].head(10).tolist()
    human_scores = df_human['human_score'].tolist()
    
    # Ensure same length
    min_len = min(len(llm_scores), len(human_scores))
    llm_scores = llm_scores[:min_len]
    human_scores = human_scores[:min_len]
    
    print(f"LLM Scores:   {llm_scores}")
    print(f"Human Scores: {human_scores}")
    
    kappa = cohen_kappa_score(llm_scores, human_scores)
    print(f"\nCohen's Kappa Score: {kappa:.4f}")
    
    if kappa < 0:
        print("Interpretation: Poor agreement (worse than random)")
    elif kappa <= 0.2:
        print("Interpretation: Slight agreement")
    elif kappa <= 0.4:
        print("Interpretation: Fair agreement")
    elif kappa <= 0.6:
        print("Interpretation: Moderate agreement")
    elif kappa <= 0.8:
        print("Interpretation: Substantial agreement")
    else:
        print("Interpretation: Almost perfect agreement")

if __name__ == "__main__":
    compute_calibration()
