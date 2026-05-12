import os, sys, asyncio, time
import pandas as pd
from dotenv import load_dotenv

# Fix Windows encoding issue
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Add paths
sys.path.insert(0, os.getcwd())
sys.path.insert(0, os.path.join(os.getcwd(), "lab24-eval-guardrails", "phase-c"))
from full_pipeline import ProtectedRAG
from src.pipeline import build_pipeline

load_dotenv()

async def run_benchmark():
    print("Starting latency benchmark...")
    search, reranker = build_pipeline()
    rag = ProtectedRAG(search, reranker)
    
    test_queries = [
        "Nghị định 13 quy định gì?",
        "Tên tôi là Nguyễn Văn A, số điện thoại 0912345678.",
        "Báo cáo tài chính là gì?",
        "Làm sao để đầu tư chứng khoán?",
        "Cách tính thuế thu nhập cá nhân?"
    ]
    
    results = []
    for q in test_queries:
        t0 = time.perf_counter()
        answer, stats = await rag.query(q)
        total_latency = (time.perf_counter() - t0) * 1000
        
        results.append({
            "query": q,
            "total_latency_ms": total_latency,
            "input_guard_latency_ms": stats.get("input_guards", {}).get("input_guard_latency_ms", 0),
            "rag_latency_ms": stats.get("rag_latency_ms", 0),
            "output_guard_latency_ms": stats.get("output_guard_latency_ms", 0)
        })
    
    df = pd.DataFrame(results)
    df.to_csv("lab24-eval-guardrails/phase-c/latency_benchmark.csv", index=False)
    print("Benchmark saved to lab24-eval-guardrails/phase-c/latency_benchmark.csv")
    print(df.describe())

if __name__ == "__main__":
    asyncio.run(run_benchmark())
