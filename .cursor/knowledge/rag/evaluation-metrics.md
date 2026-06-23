---
title: "Evaluation Metrics"
description: "Hướng dẫn về đánh giá RAG: RAGAS metrics, context precision/recall, answer faithfulness, BLEU vs LLM-based evaluation"
tags: ["evaluation", "ragas", "metrics", "faithfulness", "relevance", "llm-evaluation"]
created: "2026-06-23"
version: "1.0.0"
framework: "Cursor Enterprise Framework"
---

# Evaluation Metrics

## Tổng Quan

Đánh giá RAG systems là thách thức quan trọng vì nó đòi hỏi đánh giá nhiều khía cạnh: quality của retrieval, faithfulness của câu trả lời với context, và relevance của câu trả lời với câu hỏi. Traditional metrics như BLEU và ROUGE có limitations khi đánh giá generation tasks vì chúng chỉ measure surface-level similarity.

RAGAS (RAG Assessment) và các LLM-based evaluation methods cung cấp more nuanced assessment của RAG performance bằng cách sử dụng LLMs để judge quality.

## Mục Đích

Tài liệu này nhằm cung cấp kiến thức toàn diện về evaluation metrics cho RAG systems:

Đầu tiên, chúng ta sẽ tìm hiểu các traditional metrics như BLEU, ROUGE và khi nào chúng hữu ích.

Thứ hai, tài liệu hướng dẫn RAGAS metrics - context precision, context recall, faithfulness, và answer relevance.

Thứ ba, chúng ta sẽ đề cập đến custom LLM-based evaluation methods.

Cuối cùng, tài liệu cung cấp practical implementation và best practices.

## Key Concepts

### 1. Traditional NLP Metrics

#### BLEU Score

BLEU (Bilingual Evaluation Understudy) measures n-gram overlap between candidate and reference texts.

```python
from sacrebleu import sentence_bleu, corpus_bleu

# Sentence-level BLEU
def calculate_bleu(candidate: str, reference: str) -> float:
    """Calculate BLEU score for a single sentence."""
    return sentence_bleu(candidate, [reference]).score

# Corpus-level BLEU
def calculate_corpus_bleu(
    candidates: List[str],
    references: List[str]
) -> dict:
    """Calculate corpus-level BLEU."""
    result = corpus_bleu(candidates, [references])
    
    return {
        "score": result.score,
        "precision": result.precisions,
        "brevity_penalty": result.bp,
        "ref_length": result.ref_len
    }
```

#### ROUGE Score

ROUGE (Recall-Oriented Understudy for Gisting Evaluation) measures overlap of n-grams, word sequences, and word pairs.

```python
from rouge import Rouge

class ROUGEEvaluator:
    """Calculate ROUGE metrics."""
    
    def __init__(self):
        self.rouge = Rouge()
    
    def evaluate(
        self,
        candidate: str,
        reference: str
    ) -> dict:
        """Calculate ROUGE-L, ROUGE-1, ROUGE-2."""
        scores = self.rouge.get_scores(
            candidate,
            reference,
            avg=True
        )
        
        return {
            "rouge-1": scores["rouge-1"]["f"],
            "rouge-2": scores["rouge-2"]["f"],
            "rouge-l": scores["rouge-l"]["f"]
        }
    
    def evaluate_batch(
        self,
        candidates: List[str],
        references: List[str]
    ) -> dict:
        """Calculate average ROUGE scores."""
        scores = self.rouge.get_scores(
            candidates,
            references,
            avg=True
        )
        
        return {
            "rouge-1": scores["rouge-1"]["f"],
            "rouge-2": scores["rouge-2"]["f"],
            "rouge-l": scores["rouge-l"]["f"]
        }
```

### 2. RAGAS Metrics

RAGAS cung cấp four key metrics để evaluate RAG systems:

```python
@dataclass
class RAGASMetrics:
    """
    RAGAS metrics for RAG evaluation.
    
    Reference: https://arxiv.org/abs/2309.15217
    """
    
    # Context metrics
    context_precision: float  # How well retrieved context is ranked
    context_recall: float    # How much relevant context was retrieved
    
    # Answer metrics
    faithfulness: float      # How faithful answer is to context
    answer_relevance: float  # How relevant answer is to question
    answer_similarity: float # Semantic similarity to reference

class RAGASEvaluator:
    """
    Evaluate RAG using RAGAS metrics.
    """
    
    def __init__(self, llm_client, embedding_model):
        self.llm = llm_client
        self.embedding = embedding_model
    
    async def evaluate(
        self,
        question: str,
        answer: str,
        contexts: List[str],
        reference: str = None
    ) -> RAGASMetrics:
        """
        Evaluate RAG system using RAGAS metrics.
        """
        # Calculate context precision
        context_precision = await self._context_precision(
            question, contexts
        )
        
        # Calculate context recall
        context_recall = await self._context_recall(
            contexts, reference
        ) if reference else None
        
        # Calculate faithfulness
        faithfulness = await self._faithfulness(
            question, answer, contexts
        )
        
        # Calculate answer relevance
        answer_relevance = await self._answer_relevance(
            question, answer
        )
        
        return RAGASMetrics(
            context_precision=context_precision,
            context_recall=context_recall or 0.0,
            faithfulness=faithfulness,
            answer_relevance=answer_relevance,
            answer_similarity=0.0  # Calculated if reference provided
        )
```

### 3. Context Precision

Context precision đo lường mức độ các relevant documents được xếp hạng cao trong kết quả retrieval.

```python
async def _context_precision(
    self,
    question: str,
    contexts: List[str],
    k: int = None
) -> float:
    """
    Calculate context precision.
    
    Context Precision@K = (1/K) * Σ Precision@i
    
    where Precision@i = (Relevant items in top i) / i
    """
    k = k or len(contexts)
    
    # Generate expected relevant statements
    expected = await self._generate_relevant_statements(question)
    
    precisions = []
    
    for i, context in enumerate(contexts[:k], 1):
        # Check if context contains relevant information
        is_relevant = await self._check_relevance(context, expected)
        
        precision_at_i = sum(
            1 for ctx in contexts[:i]
            if await self._check_relevance(ctx, expected)
        ) / i
        
        precisions.append(precision_at_i)
    
    return sum(precisions) / len(precisions) if precisions else 0.0

async def _check_relevance(
    self,
    context: str,
    expected_statements: List[str]
) -> bool:
    """
    Check if context contains relevant information.
    """
    prompt = f"""
Given the following question and context, determine if the context 
contains information that helps answer the question.

Question: {question}
Context: {context}

Is the context relevant? (yes/no)
"""
    
    response = await self.llm.complete(prompt)
    
    return "yes" in response.lower()
```

### 4. Context Recall

Context recall đo lường mức độ relevant information trong reference được retrieved trong contexts.

```python
async def _context_recall(
    self,
    contexts: List[str],
    reference: str
) -> float:
    """
    Calculate context recall.
    
    Context Recall = (Ground truth statements in context) / (Total ground truth statements)
    """
    # Extract ground truth statements
    ground_truth_statements = await self._extract_statements(reference)
    
    if not ground_truth_statements:
        return 1.0  # No ground truth = perfect recall
    
    # Combine all contexts
    combined_context = " ".join(contexts)
    
    # Check how many ground truth statements are supported
    supported_count = 0
    
    for statement in ground_truth_statements:
        if await self._statement_supported(statement, combined_context):
            supported_count += 1
    
    return supported_count / len(ground_truth_statements)

async def _extract_statements(self, text: str) -> List[str]:
    """
    Extract atomic statements from text.
    """
    prompt = f"""
Extract atomic statements from the following text. 
Return each statement on a new line.

Text: {text}

Statements:"""
    
    response = await self.llm.complete(prompt)
    
    return [
        line.strip()
        for line in response.split("\n")
        if line.strip()
    ]

async def _statement_supported(
    self,
    statement: str,
    context: str
) -> bool:
    """
    Check if a statement is supported by the context.
    """
    prompt = f"""
Given the context, determine if the following statement is supported.

Context: {context}

Statement: {statement}

Is the statement supported by the context? (yes/no)
"""
    
    response = await self.llm.complete(prompt)
    
    return "yes" in response.lower()
```

### 5. Faithfulness

Faithfulness đo lường mức độ answer được supported bởi retrieved contexts.

```python
async def _faithfulness(
    self,
    question: str,
    answer: str,
    contexts: List[str]
) -> float:
    """
    Calculate faithfulness score.
    
    Faithfulness = (Faithful claims) / (Total claims)
    """
    # Extract claims from answer
    claims = await self._extract_claims(answer)
    
    if not claims:
        return 1.0  # No claims = perfectly faithful
    
    # Combine contexts
    combined_context = " ".join(contexts)
    
    # Check each claim
    faithful_count = 0
    
    for claim in claims:
        if await self._claim_faithful(claim, combined_context):
            faithful_count += 1
    
    return faithful_count / len(claims)

async def _extract_claims(self, text: str) -> List[str]:
    """
    Extract factual claims from text.
    """
    prompt = f"""
Extract factual claims from the following text. 
Focus on objective statements of fact.
Return each claim on a new line.

Text: {text}

Claims:"""
    
    response = await self.llm.complete(prompt)
    
    return [
        line.strip()
        for line in response.split("\n")
        if line.strip() and len(line.strip()) > 10
    ]

async def _claim_faithful(
    self,
    claim: str,
    context: str
) -> bool:
    """
    Check if a claim is faithful to the context.
    """
    prompt = f"""
Given the context, determine if the following claim can be 
derived from the context.

Context: {context}

Claim: {claim}

Is this claim faithful to the context? (yes/no)
"""
    
    response = await self.llm.complete(prompt)
    
    return "yes" in response.lower()
```

### 6. Answer Relevance

Answer relevance đo lường mức độ answer addresses câu hỏi.

```python
async def _answer_relevance(
    self,
    question: str,
    answer: str
) -> float:
    """
    Calculate answer relevance score.
    
    Method: Generate hypothetical questions from answer and 
    measure similarity to original question.
    """
    # Generate questions that the answer might address
    hypothetical_questions = await self._generate_hypothetical_questions(answer)
    
    # Get embeddings
    question_emb = await self.embedding.embed(question)
    hypothetical_embs = await self.embedding.embed_batch(hypothetical_questions)
    
    # Calculate similarities
    import numpy as np
    
    similarities = [
        self._cosine_similarity(question_emb, hyp_emb)
        for hyp_emb in hypothetical_embs
    ]
    
    return np.mean(similarities)

async def _generate_hypothetical_questions(
    self,
    answer: str,
    num_questions: int = 3
) -> List[str]:
    """
    Generate questions that the answer might address.
    """
    prompt = f"""
Generate {num_questions} questions that the following answer might address.
Return each question on a new line.

Answer: {answer}

Questions:"""
    
    response = await self.llm.complete(prompt)
    
    return [
        line.strip()
        for line in response.split("\n")
        if line.strip() and "?" in line
    ]

def _cosine_similarity(self, a: List[float], b: List[float]) -> float:
    """Calculate cosine similarity."""
    import numpy as np
    
    a = np.array(a)
    b = np.array(b)
    
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))
```

## LLM-based Evaluation

### 1. Custom Evaluation Framework

```python
from typing import Dict, List, Optional
from dataclasses import dataclass

@dataclass
class EvaluationResult:
    """Result of a single evaluation."""
    metric_name: str
    score: float
    explanation: str
    metadata: Dict = None

class LLMEvaluator:
    """
    LLM-based evaluator for RAG systems.
    """
    
    def __init__(self, llm_client, embedding_model):
        self.llm = llm_client
        self.embedding = embedding_model
    
    async def evaluate_answer_quality(
        self,
        question: str,
        answer: str,
        context: str,
        criteria: List[str] = None
    ) -> List[EvaluationResult]:
        """
        Evaluate answer quality based on custom criteria.
        """
        if criteria is None:
            criteria = [
                "correctness",
                "completeness",
                "coherence",
                "conciseness"
            ]
        
        results = []
        
        for criterion in criteria:
            result = await self._evaluate_criterion(
                question, answer, context, criterion
            )
            results.append(result)
        
        return results
    
    async def _evaluate_criterion(
        self,
        question: str,
        answer: str,
        context: str,
        criterion: str
    ) -> EvaluationResult:
        """Evaluate a specific criterion."""
        
        rubrics = {
            "correctness": {
                "high": "The answer accurately reflects the context and facts",
                "medium": "The answer is mostly correct with minor inaccuracies",
                "low": "The answer contains significant factual errors"
            },
            "completeness": {
                "high": "The answer fully addresses all aspects of the question",
                "medium": "The answer addresses most aspects of the question",
                "low": "The answer misses key aspects of the question"
            },
            "coherence": {
                "high": "The answer is well-organized and easy to follow",
                "medium": "The answer is mostly coherent with some confusion",
                "low": "The answer is confusing or poorly organized"
            },
            "conciseness": {
                "high": "The answer is focused and doesn't contain unnecessary information",
                "medium": "The answer is reasonably concise",
                "low": "The answer contains significant filler or irrelevant content"
            }
        }
        
        prompt = f"""
Evaluate the following answer based on the criterion: {criterion}

Question: {question}
Answer: {answer}
Context: {context}

Scoring rubric:
- High (1.0): {rubrics[criterion]['high']}
- Medium (0.6): {rubrics[criterion]['medium']}
- Low (0.2): {rubrics[criterion]['low']}

Provide your evaluation in the following format:
Score: [0.0-1.0]
Explanation: [Brief explanation of your score]
"""
        
        response = await self.llm.complete(prompt)
        
        # Parse score
        score = self._parse_score(response)
        explanation = self._parse_explanation(response)
        
        return EvaluationResult(
            metric_name=criterion,
            score=score,
            explanation=explanation
        )
    
    def _parse_score(self, response: str) -> float:
        """Parse score from LLM response."""
        import re
        
        match = re.search(r'Score:\s*([0-9.]+)', response)
        
        if match:
            return float(match.group(1))
        
        return 0.5  # Default score
    
    def _parse_explanation(self, response: str) -> str:
        """Parse explanation from LLM response."""
        import re
        
        match = re.search(r'Explanation:\s*(.+?)(?:\n|$)', response, re.DOTALL)
        
        if match:
            return match.group(1).strip()
        
        return "No explanation provided"
```

### 2. Comparative Evaluation

```python
class ComparativeEvaluator:
    """
    Compare two RAG systems or configurations.
    """
    
    def __init__(self, llm_client):
        self.llm = llm_client
    
    async def compare_systems(
        self,
        question: str,
        answer_a: str,
        answer_b: str,
        context: str
    ) -> Dict[str, any]:
        """
        Compare two answers and determine which is better.
        """
        prompt = f"""
Compare the following two answers to the question. 
Determine which is better and explain why.

Question: {question}

Answer A: {answer_a}

Answer B: {answer_b}

Context: {context}

Provide your comparison in the following format:
Winner: [A/B/Tie]
Score A: [0-10]
Score B: [0-10]
Reasoning: [Brief explanation]
"""
        
        response = await self.llm.complete(prompt)
        
        return self._parse_comparison(response)
    
    def _parse_comparison(self, response: str) -> Dict:
        """Parse comparison result."""
        import re
        
        winner_match = re.search(r'Winner:\s*([AB]|Tie)', response, re.IGNORECASE)
        score_a_match = re.search(r'Score A:\s*([0-9.]+)', response)
        score_b_match = re.search(r'Score B:\s*([0-9.]+)', response)
        reasoning_match = re.search(r'Reasoning:\s*(.+?)(?:\n\n|$)', response, re.DOTALL)
        
        return {
            "winner": winner_match.group(1) if winner_match else "Tie",
            "score_a": float(score_a_match.group(1)) if score_a_match else 0,
            "score_b": float(score_b_match.group(1)) if score_b_match else 0,
            "reasoning": reasoning_match.group(1).strip() if reasoning_match else ""
        }
```

## Best Practices

### 1. Evaluation Pipeline

```python
class RAGEvaluationPipeline:
    """
    Complete evaluation pipeline for RAG systems.
    """
    
    def __init__(
        self,
        llm_client,
        embedding_model,
        evaluators: Dict[str, object] = None
    ):
        self.llm = llm_client
        self.embedding = embedding_model
        self.evaluators = evaluators or {
            "ragas": RAGASEvaluator(llm_client, embedding_model),
            "traditional": TraditionalMetricsEvaluator(),
            "llm": LLMEvaluator(llm_client, embedding_model)
        }
    
    async def evaluate(
        self,
        test_cases: List[dict],
        metrics: List[str] = None
    ) -> Dict:
        """
        Evaluate RAG system on test cases.
        
        Each test case should have:
        - question: str
        - answer: str
        - contexts: List[str]
        - reference: Optional[str]
        """
        if metrics is None:
            metrics = ["ragas", "traditional"]
        
        all_results = []
        
        for i, test_case in enumerate(test_cases):
            print(f"Evaluating test case {i + 1}/{len(test_cases)}")
            
            case_results = await self._evaluate_single(
                test_case,
                metrics
            )
            
            all_results.append({
                "question": test_case["question"],
                "results": case_results
            })
        
        # Aggregate results
        return self._aggregate_results(all_results)
    
    async def _evaluate_single(
        self,
        test_case: dict,
        metrics: List[str]
    ) -> Dict:
        """Evaluate a single test case."""
        results = {}
        
        if "ragas" in metrics:
            ragas = self.evaluators["ragas"]
            ragas_result = await ragas.evaluate(
                question=test_case["question"],
                answer=test_case["answer"],
                contexts=test_case["contexts"],
                reference=test_case.get("reference")
            )
            
            results["ragas"] = {
                "context_precision": ragas_result.context_precision,
                "context_recall": ragas_result.context_recall,
                "faithfulness": ragas_result.faithfulness,
                "answer_relevance": ragas_result.answer_relevance
            }
        
        if "traditional" in metrics:
            trad = self.evaluators["traditional"]
            trad_result = trad.evaluate(
                candidate=test_case["answer"],
                reference=test_case.get("reference", "")
            )
            
            results["traditional"] = trad_result
        
        return results
    
    def _aggregate_results(self, results: List[dict]) -> Dict:
        """Aggregate results across test cases."""
        aggregated = {
            "total_cases": len(results),
            "metrics": {}
        }
        
        # Collect all metric names
        metric_names = set()
        for result in results:
            metric_names.update(result["results"].keys())
        
        # Aggregate each metric
        for metric_name in metric_names:
            values = []
            
            for result in results:
                metric_results = result["results"].get(metric_name, {})
                
                for key, value in metric_results.items():
                    if isinstance(value, (int, float)) and not pd.isna(value):
                        values.append((key, value))
            
            # Group by sub-metric
            grouped = {}
            for key, value in values:
                if key not in grouped:
                    grouped[key] = []
                grouped[key].append(value)
            
            # Calculate statistics
            aggregated["metrics"][metric_name] = {
                key: {
                    "mean": np.mean(vals),
                    "std": np.std(vals),
                    "min": np.min(vals),
                    "max": np.max(vals)
                }
                for key, vals in grouped.items()
            }
        
        return aggregated
```

### 2. A/B Testing Framework

```python
class ABEvaluator:
    """
    A/B testing for RAG configurations.
    """
    
    def __init__(self, evaluator: RAGEvaluationPipeline):
        self.evaluator = evaluator
    
    async def run_ab_test(
        self,
        test_cases: List[dict],
        config_a: dict,
        config_b: dict,
        metric: str = "faithfulness"
    ) -> Dict:
        """
        Run A/B test between two configurations.
        """
        # Evaluate config A
        print("Evaluating configuration A...")
        results_a = await self._evaluate_with_config(
            test_cases,
            config_a
        )
        
        # Evaluate config B
        print("Evaluating configuration B...")
        results_b = await self._evaluate_with_config(
            test_cases,
            config_b
        )
        
        # Statistical significance test
        significance = self._test_significance(
            results_a[metric],
            results_b[metric]
        )
        
        return {
            "config_a": {
                "results": results_a,
                "mean_score": np.mean(results_a[metric])
            },
            "config_b": {
                "results": results_b,
                "mean_score": np.mean(results_b[metric])
            },
            "winner": "A" if np.mean(results_a[metric]) > np.mean(results_b[metric]) else "B",
            "statistical_significance": significance
        }
    
    async def _evaluate_with_config(
        self,
        test_cases: List[dict],
        config: dict
    ) -> Dict:
        """Evaluate with a specific configuration."""
        # This would instantiate the RAG system with the given config
        # and run evaluation
        pass
    
    def _test_significance(
        self,
        values_a: List[float],
        values_b: List[float]
    ) -> Dict:
        """Test statistical significance using t-test."""
        from scipy import stats
        
        t_stat, p_value = stats.ttest_ind(values_a, values_b)
        
        return {
            "t_statistic": t_stat,
            "p_value": p_value,
            "significant": p_value < 0.05
        }
```

### 3. Continuous Evaluation

```python
class ContinuousEvaluator:
    """
    Continuous evaluation monitoring for production RAG systems.
    """
    
    def __init__(
        self,
        evaluator: RAGEvaluationPipeline,
        metrics_storage
    ):
        self.evaluator = evaluator
        self.storage = metrics_storage
    
    async def evaluate_sample(
        self,
        production_logs: List[dict],
        sample_size: int = 100
    ) -> Dict:
        """
        Evaluate a sample of production queries.
        """
        # Sample from production logs
        import random
        sample = random.sample(production_logs, min(sample_size, len(production_logs)))
        
        # Evaluate sample
        test_cases = [
            {
                "question": log["question"],
                "answer": log["answer"],
                "contexts": log["contexts"],
                "reference": log.get("reference")
            }
            for log in sample
        ]
        
        results = await self.evaluator.evaluate(test_cases)
        
        # Store results
        await self.storage.store(results)
        
        # Check for degradation
        alerts = self._check_for_degradation(results)
        
        return {
            "results": results,
            "alerts": alerts
        }
    
    def _check_for_degradation(self, results: Dict) -> List[Dict]:
        """Check if metrics have degraded."""
        alerts = []
        
        # Get historical baseline
        baseline = self.storage.get_baseline()
        
        if not baseline:
            return alerts
        
        # Check each metric
        for metric_name, metrics in results["metrics"].items():
            for sub_metric, stats in metrics.items():
                baseline_value = baseline.get(metric_name, {}).get(sub_metric, {}).get("mean")
                
                if baseline_value:
                    current = stats["mean"]
                    degradation = (baseline_value - current) / baseline_value
                    
                    if degradation > 0.1:  # 10% degradation threshold
                        alerts.append({
                            "metric": f"{metric_name}.{sub_metric}",
                            "baseline": baseline_value,
                            "current": current,
                            "degradation_percent": degradation * 100
                        })
        
        return alerts
```

## Examples

### Example 1: Creating Test Datasets

```python
class TestDatasetCreator:
    """
    Create test datasets for RAG evaluation.
    """
    
    def __init__(self, llm_client):
        self.llm = llm_client
    
    async def create_from_documents(
        self,
        documents: List[dict],
        num_questions_per_doc: int = 5
    ) -> List[dict]:
        """
        Generate question-answer pairs from documents.
        """
        test_cases = []
        
        for doc in documents:
            test_cases.extend(
                await self._generate_for_document(
                    doc,
                    num_questions_per_doc
                )
            )
        
        return test_cases
    
    async def _generate_for_document(
        self,
        document: dict,
        num_questions: int
    ) -> List[dict]:
        """Generate test cases for a single document."""
        prompt = f"""
Generate {num_questions} question-answer pairs based on the following document.
Include different types: factual, conceptual, and analytical questions.

Document:
Title: {document.get('title', 'Untitled')}
Content: {document.get('content', '')[:2000]}

For each question-answer pair, provide:
1. The question
2. The expected answer (reference answer)
3. The key context points needed to answer

Format as JSON:
[
  {{
    "question": "...",
    "answer": "...",
    "contexts": ["...", "..."]
  }}
]
"""
        
        response = await self.llm.complete(prompt)
        
        # Parse JSON from response
        import json
        import re
        
        json_match = re.search(r'\[[\s\S]*\]', response)
        
        if json_match:
            test_cases = json.loads(json_match.group())
            
            for case in test_cases:
                case["source_doc_id"] = document.get("id")
            
            return test_cases
        
        return []
    
    async def create_human_curated(
        self,
        seed_questions: List[str],
        documents: List[dict]
    ) -> List[dict]:
        """
        Create test set from human-curated questions.
        """
        test_cases = []
        
        for question in seed_questions:
            # Find most relevant document
            relevant_doc = await self._find_relevant_doc(question, documents)
            
            if relevant_doc:
                test_cases.append({
                    "question": question,
                    "answer": "",  # To be filled by human
                    "contexts": [relevant_doc.get("content", "")],
                    "source_doc_id": relevant_doc.get("id"),
                    "requires_human_review": True
                })
        
        return test_cases
```

### Example 2: Dashboard và Reporting

```python
class EvaluationDashboard:
    """
    Generate evaluation reports and dashboards.
    """
    
    def __init__(self, evaluator: RAGEvaluationPipeline):
        self.evaluator = evaluator
    
    def generate_report(
        self,
        results: Dict,
        format: str = "html"
    ) -> str:
        """
        Generate evaluation report.
        """
        if format == "html":
            return self._generate_html_report(results)
        elif format == "markdown":
            return self._generate_markdown_report(results)
        else:
            return str(results)
    
    def _generate_markdown_report(self, results: Dict) -> str:
        """Generate markdown report."""
        lines = [
            "# RAG Evaluation Report",
            "",
            f"**Total Test Cases:** {results['total_cases']}",
            "",
            "## Metrics Summary",
            ""
        ]
        
        for metric_name, metrics in results["metrics"].items():
            lines.append(f"### {metric_name.upper()}")
            lines.append("")
            lines.append("| Sub-metric | Mean | Std | Min | Max |")
            lines.append("|------------|------|-----|-----|-----|")
            
            for sub_metric, stats in metrics.items():
                lines.append(
                    f"| {sub_metric} | "
                    f"{stats['mean']:.4f} | "
                    f"{stats['std']:.4f} | "
                    f"{stats['min']:.4f} | "
                    f"{stats['max']:.4f} |"
                )
            
            lines.append("")
        
        return "\n".join(lines)
    
    def _generate_html_report(self, results: Dict) -> str:
        """Generate HTML report with visualizations."""
        html = """
<!DOCTYPE html>
<html>
<head>
    <title>RAG Evaluation Report</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; }
        .metric-card { 
            border: 1px solid #ddd; 
            padding: 20px; 
            margin: 10px 0;
            border-radius: 8px;
        }
        .score { font-size: 32px; font-weight: bold; }
        .chart-container { max-width: 600px; margin: 20px 0; }
    </style>
</head>
<body>
    <h1>RAG Evaluation Report</h1>
    <p>Total Test Cases: {total_cases}</p>
""".format(total_cases=results['total_cases'])
        
        for metric_name, metrics in results["metrics"].items():
            html += f"""
    <div class="metric-card">
        <h2>{metric_name.upper()}</h2>
        <canvas id="chart-{metric_name}"></canvas>
        <script>
            new Chart(document.getElementById('chart-{metric_name}'), {{
                type: 'bar',
                data: {{
                    labels: {list(metrics.keys())},
                    datasets: [{{
                        label: 'Mean Score',
                        data: {[m['mean'] for m in metrics.values()]},
                        backgroundColor: 'rgba(54, 162, 235, 0.5)'
                    }}]
                }}
            }});
        </script>
    </div>
"""
        
        html += "</body></html>"
        
        return html
```

### Example 3: Automated Quality Gates

```python
class QualityGate:
    """
    Automated quality gates for RAG deployment.
    """
    
    def __init__(
        self,
        evaluator: RAGEvaluationPipeline,
        thresholds: Dict[str, float]
    ):
        self.evaluator = evaluator
        self.thresholds = thresholds
    
    async def check_quality(
        self,
        test_cases: List[dict]
    ) -> Dict:
        """
        Check if RAG system passes quality gates.
        """
        # Run evaluation
        results = await self.evaluator.evaluate(test_cases)
        
        # Check against thresholds
        passed = {}
        failed = {}
        
        for metric_name, metrics in results["metrics"].items():
            for sub_metric, stats in metrics.items():
                full_metric = f"{metric_name}.{sub_metric}"
                threshold = self.thresholds.get(full_metric, 0.0)
                
                if stats["mean"] >= threshold:
                    passed[full_metric] = {
                        "score": stats["mean"],
                        "threshold": threshold
                    }
                else:
                    failed[full_metric] = {
                        "score": stats["mean"],
                        "threshold": threshold,
                        "gap": threshold - stats["mean"]
                    }
        
        return {
            "passed": len(passed) > 0,
            "all_gates_passed": len(failed) == 0,
            "passed_metrics": passed,
            "failed_metrics": failed,
            "summary": {
                "total_checks": len(passed) + len(failed),
                "passed_count": len(passed),
                "failed_count": len(failed)
            },
            "recommendation": self._get_recommendation(passed, failed)
        }
    
    def _get_recommendation(
        self,
        passed: Dict,
        failed: Dict
    ) -> str:
        """Get deployment recommendation based on results."""
        if not failed:
            return "APPROVED: All quality gates passed. Safe to deploy."
        
        critical_failures = [
            metric for metric in failed.keys()
            if "faithfulness" in metric or "correctness" in metric
        ]
        
        if critical_failures:
            return (
                "BLOCKED: Critical quality issues detected. "
                f"Failed metrics: {', '.join(critical_failures)}. "
                "Review and improve before deployment."
            )
        
        return (
            f"REVIEW NEEDED: {len(failed)} non-critical gates failed. "
            "Review results before deployment."
        )


# Default thresholds
DEFAULT_THRESHOLDS = {
    "ragas.faithfulness": 0.8,
    "ragas.answer_relevance": 0.75,
    "ragas.context_precision": 0.7,
    "ragas.context_recall": 0.7,
    "traditional.bleu": 0.3,
    "traditional.rouge_l": 0.4
}
```

## References

1. **RAGAS Paper**: https://arxiv.org/abs/2309.15217
2. **BLEU Score**: https://www.aclweb.org/anthology/P02-1040.pdf
3. **ROUGE Score**: https://aclanthology.org/W04-1013.pdf
4. **RAG Evaluation Survey**: https://arxiv.org/abs/2312.10937
5. **Cursor Enterprise Framework - RAG Rules**: `.cursor/rules/rag.mdc`
