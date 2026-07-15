# Benchmarks and Datasets

## Selection matrix

| Resource | Best for | Important limitation |
|---|---|---|
| AgentDojo | stateful tool-agent utility and security | default attacks are not a complete adaptive evaluation |
| InjecAgent | tool-pair and indirect-injection taxonomy | simulated construction differs from live workflows |
| BIPIA | external-content tasks and defenses | source-data licensing varies by task |
| Agent Security Bench | broad attack and defense research | preprint versions and experimental setup require review |
| Your own authorized traces | production relevance | privacy, label delay, and sampling bias |

## Integration rule

Do not merge benchmark rows blindly. Normalize:

- unit of analysis
- label meaning
- attack goal
- success check
- tool and environment identifiers
- provenance and license
- generation template
- model-visible versus evaluator-only fields

## Recommended benchmark layers

1. deterministic unit cases for code correctness
2. curated hard cases for regression
3. grouped held-out benchmark for model selection
4. out-of-distribution attack families
5. dynamic stateful agent tests
6. shadow production data with delayed labels

## License discipline

Record the license and upstream source for code and every data component. BIPIA explicitly notes that some task contexts must be downloaded separately because of source licenses. Linking to a dataset does not grant redistribution rights.
