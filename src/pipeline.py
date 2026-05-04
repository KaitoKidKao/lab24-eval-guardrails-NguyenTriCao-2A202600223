"""Production RAG Pipeline — Bài tập NHÓM: ghép M1+M2+M3+M4."""

import os, sys, time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.m1_chunking import load_documents, chunk_hierarchical
from src.m2_search import HybridSearch
from src.m3_rerank import CrossEncoderReranker
from src.m4_eval import load_test_set, evaluate_ragas, failure_analysis, save_report
from src.m5_enrichment import enrich_chunks
from config import RERANK_TOP_K


def build_pipeline():
    """Build production RAG pipeline."""
    print("=" * 60)
    print("PRODUCTION RAG PIPELINE")
    print("=" * 60)

    # Step 1: Load & Chunk (M1)
    print("\n[1/3] Chunking documents...")
    docs = load_documents()
    all_chunks = []
    for doc in docs:
        parents, children = chunk_hierarchical(doc["text"], metadata=doc["metadata"])
        for child in children:
            all_chunks.append({"text": child.text, "metadata": {**child.metadata, "parent_id": child.parent_id}})
    print(f"  {len(all_chunks)} chunks from {len(docs)} documents")

    # Step 2: Enrichment (M5)
    print("\n[2/4] Enriching chunks (M5)...")
    # Giới hạn 30 chunks đầu tiên để chạy demo cho nhanh
    limit = 30
    enriched = enrich_chunks(all_chunks[:limit], methods=["contextual"])
    
    if enriched:
        # Mix enriched chunks with the rest (or just use enriched for testing)
        enriched_data = [{"text": e.enriched_text, "metadata": e.auto_metadata} for e in enriched]
        remaining_data = all_chunks[limit:]
        all_chunks = enriched_data + remaining_data
        print(f"  Enriched {len(enriched)} chunks (First {limit} chunks)")
    else:
        print("  ⚠️  M5 not implemented — using raw chunks (fallback)")

    # Step 3: Index (M2)
    print("\n[3/4] Indexing (BM25 + Dense)...")
    search = HybridSearch()
    search.index(all_chunks)

    # Step 4: Reranker (M3)
    print("\n[4/4] Loading reranker...")
    reranker = CrossEncoderReranker()

    return search, reranker


def run_query(query: str, search: HybridSearch, reranker: CrossEncoderReranker) -> tuple[str, list[str]]:
    """Run single query through pipeline."""
    # 1. Retrieval (Hybrid)
    results = search.search(query)
    
    # 2. Reranking
    docs = [{"text": r.text, "score": r.score, "metadata": r.metadata} for r in results]
    reranked = reranker.rerank(query, docs, top_k=RERANK_TOP_K)
    contexts = [r.text for r in reranked] if reranked else [r.text for r in results[:3]]

    # 3. Generation (LLM)
    from openai import OpenAI
    from config import OPENAI_API_KEY
    
    client = OpenAI(api_key=OPENAI_API_KEY)
    context_str = "\n\n".join([f"--- Context {i+1} ---\n{c}" for i, c in enumerate(contexts)])
    
    try:
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": """Bạn là một trợ lý ảo phân tích tài liệu chuyên nghiệp. 
                Nhiệm vụ của bạn là trả lời câu hỏi CHỈ dựa trên các ngữ cảnh được cung cấp bên dưới.
                
                QUY TẮC QUAN TRỌNG:
                1. KHÔNG sử dụng kiến thức bên ngoài ngữ cảnh.
                2. Nếu ngữ cảnh không chứa thông tin để trả lời, hãy nói: 'Tôi không tìm thấy thông tin này trong tài liệu.'
                3. Trích dẫn thông tin chính xác từ ngữ cảnh. KHÔNG suy diễn hoặc thêm thắt.
                4. Giữ câu trả lời khách quan, trung thực và súc tích."""},
                {"role": "user", "content": f"Dưới đây là các đoạn ngữ cảnh trích xuất từ tài liệu:\n{context_str}\n\nDựa trên các đoạn trên, hãy trả lời câu hỏi: {query}"},
            ],
            temperature=0.1, # Giảm sáng tạo để tăng tính trung thực
        )
        answer = resp.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error in LLM Generation: {e}")
        answer = contexts[0] if contexts else "Không tìm thấy thông tin."
        
    return answer, contexts


def evaluate_pipeline(search: HybridSearch, reranker: CrossEncoderReranker):
    """Run evaluation on test set."""
    print("\n[Eval] Running queries...")
    test_set = load_test_set()
    questions, answers, all_contexts, ground_truths = [], [], [], []
    latencies = []

    for i, item in enumerate(test_set):
        t0 = time.perf_counter()
        answer, contexts = run_query(item["question"], search, reranker)
        latencies.append((time.perf_counter() - t0) * 1000)
        
        questions.append(item["question"])
        answers.append(answer)
        all_contexts.append(contexts)
        ground_truths.append(item["ground_truth"])
        print(f"  [{i+1}/{len(test_set)}] {item['question'][:50]}...")

    print("\n[Eval] Running RAGAS...")
    results = evaluate_ragas(questions, answers, all_contexts, ground_truths)

    print("\n" + "=" * 60)
    print("PRODUCTION RAG SCORES")
    print("=" * 60)
    for m in ["faithfulness", "answer_relevancy", "context_precision", "context_recall"]:
        s = results.get(m, 0)
        print(f"  {'✓' if s >= 0.75 else '✗'} {m}: {s:.4f}")

    failures = failure_analysis(results.get("per_question", []))
    save_report(results, failures)
    
    # Bonus: Latency Breakdown
    import numpy as np
    print("\n" + "=" * 60)
    print("LATENCY BREAKDOWN (PER QUERY)")
    print("=" * 60)
    print(f"  Avg Latency: {np.mean(latencies):.1f}ms")
    print(f"  Min Latency: {np.min(latencies):.1f}ms")
    print(f"  Max Latency: {np.max(latencies):.1f}ms")
    
    return results


if __name__ == "__main__":
    start = time.time()
    search, reranker = build_pipeline()
    evaluate_pipeline(search, reranker)
    print(f"\nTotal: {time.time() - start:.1f}s")
