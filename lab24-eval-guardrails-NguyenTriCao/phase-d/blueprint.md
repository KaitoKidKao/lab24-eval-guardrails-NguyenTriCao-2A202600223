# Lab 24: Architectural Blueprint - Production RAG Evaluation & Guardrails

## 1. System Architecture
The system follows a multi-layered defense-in-depth architecture to ensure the safety, relevance, and quality of RAG outputs.

### 1.1 Components
- **Input Guardrail Layer**:
    - **PII Redactor**: Uses Presidio + Custom Regex to mask sensitive Vietnamese data (CCCD, Phone, Email).
    - **Topic Validator**: Zero-shot LLM classification to ensure queries are within Finance/Legal scope.
- **RAG Pipeline (Day 18)**:
    - **Chunking**: Hierarchical chunking with context enrichment.
    - **Retrieval**: Hybrid search (BM25 + Dense) with Qdrant.
    - **Reranking**: Cross-encoder reranking (Cohere).
    - **Generation**: GPT-4o-mini with strict grounding instructions.
- **Output Guardrail Layer**:
    - **Safety Filter**: Llama Guard 3 (via Groq) / OpenAI Moderation API.
- **Evaluation Engine**:
    - **RAGAS**: Automated multi-metric evaluation (Faithfulness, Relevancy, Precision, Recall).
    - **LLM-as-Judge**: Custom Pairwise and Absolute scoring for deep quality assessment.

### 1.2 Data Flow
1. User Query -> PII Redaction -> Topic Validation.
2. If Valid -> RAG Retrieval -> Rerank -> LLM Generate Answer.
3. Answer -> Safety Filter -> Final Response.

## 2. Performance SLOs (Service Level Objectives)
- **Latency**:
    - Guardrails (Input + Output): < 500ms (P95, parallel execution).
    - Total End-to-End: < 3000ms (P95).
- **Quality**:
    - Faithfulness (RAGAS): > 0.85.
    - Answer Relevancy (RAGAS): > 0.80.
- **Safety**:
    - PII Leakage: 0% (in tested samples).
    - Unsafe Output Rate: < 1%.

## 3. Incident Response Playbook
| Incident | Detection | Mitigation |
|----------|-----------|------------|
| PII Leak detected | RAGAS / Manual Audit | Update Regex patterns; Wipe history |
| High Hallucination | RAGAS Faithfulness < 0.7 | Adjust temperature; Improve chunk enrichment |
| High Latency | Latency Benchmarking > 5s | Optimize Reranker top-k; Use faster LLM |
| Out-of-scope query loop | Topic Guard logs | Refine Topic prompt; Update system instructions |

## 4. Cost Analysis (Estimated)
- **RAGAS Evaluation**: ~$0.05 per 100 questions (using gpt-4o-mini).
- **Guardrails**: ~$0.01 per 1000 requests (Groq is currently free/low cost).
- **RAG Execution**: ~$0.02 per request (Retrieval + Rerank + Gen).

## 5. Continuous Improvement
- **Weekly Evaluation**: Run RAGAS on a subset of production logs.
- **Human-in-the-loop**: Randomly audit LLM-as-Judge scores against human labels (Calibration).
- **Adversarial Training**: Regularly update the test set with new "jailbreak" attempts.
