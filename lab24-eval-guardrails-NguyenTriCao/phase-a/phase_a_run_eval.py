import os
import sys
import time
import json
import pandas as pd
from dotenv import load_dotenv

# Fix Windows encoding issue
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from datasets import Dataset
from ragas import evaluate
from ragas.metrics import (
    faithfulness,
    answer_relevancy,
    context_precision,
    context_recall,
)
from ragas.llms import LangchainLLMWrapper
from langchain_openai import ChatOpenAI

# Add project root to path to import src
import sys
sys.path.insert(0, os.getcwd())

from src.pipeline import build_pipeline, run_query

# Load environment variables
load_dotenv()

def run_evaluation():
    testset_path = os.path.join("lab24-eval-guardrails", "phase-a", "testset_v1.csv")
    if not os.path.exists(testset_path):
        print(f"Error: {testset_path} not found. Run phase_a_testset_gen.py first.")
        return

    print("Loading test set...")
    df_test = pd.read_csv(testset_path)
    
    # RAGAS 0.4.x might have different column names, ensure they match what we need
    # We need: question, ground_truth
    # Based on TestsetGenerator output, it should have 'question' and 'ground_truth'
    
    print("Building RAG pipeline...")
    search, reranker = build_pipeline()

    questions = []
    answers = []
    all_contexts = []
    ground_truths = []

    print(f"Running pipeline on {len(df_test)} questions...")
    for i, row in df_test.iterrows():
        question = row['user_input']
        ground_truth = row['reference']
        
        print(f"[{i+1}/{len(df_test)}] Question: {question[:50]}...")
        
        # Run query through Day 18 pipeline
        answer, contexts, latency = run_query(question, search, reranker)
        
        questions.append(question)
        answers.append(answer)
        all_contexts.append(contexts)
        ground_truths.append(ground_truth)
        
        # Respect rate limits (6s for Cohere trial)
        time.sleep(6)

    # Create dataset for RAGAS
    data = {
        "question": questions,
        "answer": answers,
        "contexts": all_contexts,
        "ground_truth": ground_truths
    }
    dataset = Dataset.from_dict(data)

    print("Initializing RAGAS evaluator LLM...")
    evaluator_llm = LangchainLLMWrapper(ChatOpenAI(model="gpt-4o-mini"))

    print("Running RAGAS evaluation...")
    metrics = [
        faithfulness,
        answer_relevancy,
        context_precision,
        context_recall,
    ]
    
    # Configure metrics to use our evaluator LLM
    for metric in metrics:
        metric.llm = evaluator_llm

    results = evaluate(dataset, metrics=metrics)
    
    print("\nEvaluation Results:")
    print(results)
    
    # Save results
    results_df = results.to_pandas()
    output_path = os.path.join("lab24-eval-guardrails", "phase-a", "ragas_results.csv")
    results_df.to_csv(output_path, index=False)
    
    summary_path = os.path.join("lab24-eval-guardrails", "phase-a", "ragas_summary.json")
    with open(summary_path, "w") as f:
        json.dump(results.scores, f, indent=4)
    
    print(f"Results saved to {output_path} and {summary_path}")

if __name__ == "__main__":
    if not os.getenv("OPENAI_API_KEY"):
        print("Error: OPENAI_API_KEY not found in environment.")
    else:
        run_evaluation()
