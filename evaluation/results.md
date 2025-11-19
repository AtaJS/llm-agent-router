# LLM Router Evaluation Results

**Evaluation Date:** 2025-11-19 06:46:51

**Project:** LLM-based customer service routing system

**Author:** Ata Jodeiri Seyedian

---

## Executive Summary

This evaluation tested **45 queries** across **5 categories** to compare three routing approaches:

1. **Simple Rule-Based Router** - Baseline using keyword matching
2. **Google Gemini (gemini-2.5-flash)** - LLM powered
3. **Azure OpenAI (GPT-4o)** - LLM powered

## Overall Results

| Router | Total Queries| Correct | Accuracy | Avg Response Time|
|--------|--------------|---------|----------|------------------|
| Simple | 45           | 43      | 95.6%    | 0.000s           |
| Gemini | 45           | 44      | 97.8%    | 0.877s           |
| GPT-4  | 45           | 45      | 100.0%   | 0.466s           |

## Category Breakdown

### Edge Cases

| Router | Queries | Correct | Accuracy | Avg Time |
|--------|---------|---------|----------|----------|
| Simple | 15      | 14      | 93.3%    | 0.000s   |
| Gemini | 15      | 14      | 93.3%    | 0.953s   |
| GPT-4  | 15      | 15      | 100.0%   | 0.477s   |

### Clinical Safety

| Router | Queries | Correct | Accuracy | Avg Time |
|--------|---------|---------|----------|----------|
| Simple | 10      | 10      | 100.0%   | 0.000s   |
| Gemini | 10      | 10      | 100.0%   | 0.813s   |
| GPT-4  | 10      | 10      | 100.0%   | 0.453s   |

### Hallucination Detection

| Router | Queries | Correct | Accuracy | Avg Time |
|--------|---------|---------|----------|----------|
| Simple | 10      | 10      | 100.0%   | 0.000s   |
| Gemini | 10      | 10      | 100.0%   | 0.767s   |
| GPT-4  | 10      | 10      | 100.0%   | 0.453s   |

### Uncertainty Handling

| Router | Queries | Correct | Accuracy | Avg Time |
|--------|---------|---------|----------|----------|
| Simple | 10      | 9       | 90.0%    | 0.000s   |
| Gemini | 10      | 10      | 100.0%   | 0.935s   |
| GPT-4  | 10      | 10      | 100.0%   | 0.477s   |

## Error Analysis

### Simple Router Errors

**Edge Cases:**

- Query: "Can I reschedule or cancel my appointment for tomorrow?..."
  - Expected: `faq`
  - Actual: `order_status`

**Uncertainty Handling:**

- Query: "appointment..."
  - Expected: `faq`
  - Actual: `order_status`


### Gemini Router Errors

**Edge Cases:**

- Query: "Can I reschedule or cancel my appointment for tomorrow?..."
  - Expected: `faq`
  - Actual: `order_status`


### GPT-4 Router Errors

No errors detected! 


