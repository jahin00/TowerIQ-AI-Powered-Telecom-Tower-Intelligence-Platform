# TowerIQ Architecture

```text
Messy Source Data -> Data Quality -> SQL Analytical Layer
                                      |              |
                                      v              v
                               EDA / Risk       Forecasting
                                      \              /
                                       v            v
                                    Power BI Semantic Layer
                                               |
                                               v
                                   Investigation Engine
                                               |
                                   Natural-language question
                                               |
                                   Evidence retrieval/routing
                                               |
                                   Read-only evidence packet
                                               |
                                               v
                                   Optional LLM explanation
                                               |
                                               v
                                   Evidence-backed reporting
```

The LLM is downstream of deterministic analytics. It explains retrieved evidence rather than acting as the source of truth.
