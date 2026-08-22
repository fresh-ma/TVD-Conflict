# Research Contract

## Concept

Stress-test LLM-as-Judge safety evaluations by searching for responses that induce disagreement among judge models operating under identical evaluation criteria.

## Target Venue

- TAE (Trust-AI-Eval): Can We Trust AI Evaluation?, NeurIPS 2026 Workshop
- Double-blind full paper, up to 8 pages excluding references and appendices
- Submission deadline: August 29, 2026 (AoE)

## Threat Model

TVD-Conflict treats multiple safety judges as competing validators and searches for adversarially discovered responses that receive conflicting judgments. The evaluation targets reliability failures caused by evaluator choice, including implicit harmful intent, code-mediated behavior, and multi-step contextual reasoning.

## Key Differentiator

The work evaluates the evaluators themselves: judge disagreement is treated as a searchable failure mode rather than incidental annotation noise.

## Current Scope

This initialization milestone contains only the supplied title and abstract. Method details, claims, experiments, citations, and code remain intentionally unspecified until the design and evidence phases are complete.
