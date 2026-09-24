# Testing & Evaluation Benchmark Framework

## Clinical Benchmark Evaluation
- **Benchmark Script**: `eval_lab_management_benchmark.py`
- **Dataset**: 20 complex clinical test cases covering prior authorization requirements, medical necessity criteria, diagnostic test indications, and coverage exceptions across clinical policies (e.g. Laboratory Management).

## Evaluation Metrics
1. **Prior Auth Accuracy**: Direct comparison against ground-truth prior auth determination (`Yes`/`No`/`Add-On`).
2. **TOC Routing Precision**: Verifies that Stage 2 LLM router correctly targets the relevant policy document key and candidate section IDs.
3. **Retrieval Completeness**: Evaluates whether scoped hybrid retrieval with Sibling Condition Completion pulls all required criteria sub-blocks.
4. **JSON Synthesis Validity**: Assesses schema compliance, absence of malformed syntax, and presence of mandatory clinical fields (`status`, `indications`, `non_indications`, `exceptions`, `required_documentation`).

## Execution Command
```bash
python eval_lab_management_benchmark.py --doc Cigna_Lab_Management --queries 20
```
