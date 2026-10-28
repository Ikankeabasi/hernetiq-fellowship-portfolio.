# Regulatory Exposure Table — NovaPay AI (Week 15)

This companion table expands the regulatory section embedded in the two-page board report. It uses the same four findings as the Week 14 assessment. Article mappings are conditional on the system falling within the scope of Regulation (EU) 2024/1689 and, where relevant, being classified as high-risk.

| Finding | Named regulation and article | What it requires / why relevant | Evidence basis |
|---|---|---|---|
| Customer data separation | EU AI Act, Article 15 (Accuracy, robustness and cybersecurity); Article 9 (Risk management system) | Article 15 requires appropriate cybersecurity for applicable high-risk systems throughout their lifecycle. Article 9 requires risks to be identified, evaluated and addressed. | Week 14 Finding 1: the policy promises client data separation, but the reviewed access process does not visibly confirm that the business requesting records is the same client that signed in. |
| Unreviewed training data | EU AI Act, Article 10 (Data and data governance); Article 9 | Article 10 sets data-governance and quality criteria for training, validation and testing datasets for applicable high-risk systems. Article 9 requires appropriate risk-management measures. | Week 14 Finding 2: an external source is marked unreviewed, lacks integrity and fairness-review status, is enabled, and is shown in the 1 October 2024 pipeline-run record. This does not prove it caused an incident. |
| Model releases without evidenced approval | EU AI Act, Article 9; Article 43 (Conformity assessment) | Article 9 requires documented lifecycle risk management and testing against defined metrics. Article 43 sets the conformity-assessment procedure for applicable high-risk systems before placing on the market or putting into service. It does not mean every routine retraining automatically requires a new conformity assessment. | Week 14 Finding 3: audit records show automatic production model updates; the reviewed release path does not evidence a pre-release approval gate. The fraud incident's root cause remains unknown. |
| Fairness and monitoring gaps | EU AI Act, Article 10; Article 9 | Article 10 addresses data governance and quality; Article 9 requires continuous lifecycle risk management, including consideration of risks revealed by monitoring. | Week 14 Finding 4: fairness work is incomplete, alerts for significant changes in decision patterns are not configured and two incidents remain open without established root causes. |

## Legal scope limitation

Annex III, point 5(b), refers to AI systems used to evaluate the creditworthiness of natural persons or establish their credit score. The reviewed case describes SME loan applications, and the supplied materials do not conclusively establish the system's intended-use details, affected-person scope or EU territorial scope. A legal/compliance owner should confirm applicability before treating these articles as binding obligations or concluding that a breach occurred.

**Official legal text:** [Regulation (EU) 2024/1689 — EU AI Act, EUR-Lex](https://eur-lex.europa.eu/eli/reg/2024/1689).
