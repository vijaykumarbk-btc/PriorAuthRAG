# Evaluation & Benchmarking Suite

The project incorporates evaluation frameworks to validate retrieval precision and recall against golden medical prior authorization questions.

## Benchmark Datasets & Reports

1. **30-Question Evaluation Report**:
   - [`EVALUATION_REPORT_30Q.md`](../../EVALUATION_REPORT_30Q.md)
   - Evaluates retrieval performance across diverse clinical case scenarios.
   - Measures exact criteria hit rate, false positive retrieval, and heading context completeness.

2. **Lab Management Benchmark**:
   - Evaluator: [`eval_lab_management_benchmark.py`](../../eval_lab_management_benchmark.py)
   - Results: [`data/benchmark_results_lab_management_20q.json`](../../data/benchmark_results_lab_management_20q.json)
   - Tests targeted 20-question query set on complex genetic testing and lab panels.

3. **Lumbar Evaluation**:
   - Guidelines and query checklists documented in [`EVALUATION FOR LUMBAR.MD`](../../EVALUATION%20FOR%20LUMBAR.MD).

## Running Evaluation

```bash
# Run Lab Management benchmark evaluation
python eval_lab_management_benchmark.py
```
