# Cohort 1 — Week 13 Carousel Copy (Draft)

This file records the Week 13 wording prepared for the Canva carousel, following the existing Week 12 six-page design. Pages 4–6 are intentionally not edited in this pass.

## Page 1 — Cover
**Cohort 1 · Week 13**

## Page 2 — This Week's Sessions

1. **Investigated Goal Hijacking**  
   Inspected LegalBot's standing dismissal permission and traced a citizen-input goal hijack.

2. **Analysed Privilege Abuse**  
   Used Semgrep, then mapped the risks to MAESTRO and NIST AI RMF.

3. **Applied Remediation Controls**  
   Removed standing authority, marked citizen input as untrusted, added human approval and enabled the action-logging setting.

## Page 3 — Fellow Spotlight

**Fellow:** Ikanke Asuquo

**INSIGHT**  
I realised that securing an AI agent requires more than blocking malicious instructions; its permissions, actions and accountability must also be properly controlled.

**WIN**  
I successfully identified the governance weaknesses and strengthened the system with restricted authority, human approval and audit logging.

**CHALLENGE**  
My main challenge was understanding how goal hijacking could lead to privilege misuse and determining the right architectural controls to prevent unauthorised actions.

The Insight, Win and Challenge above are reproduced exactly from the recap supplied in the conversation. Keep the existing fellow photo and name treatment in Canva.

## Artifact of the Week — Reference Link
[LegalBot hardened configuration — agent_config.py](https://github.com/Ikankeabasi/ai-security-defense-lab/blob/main/fixtures/level5_legalbot/agent_config.py)

Use this actual configuration file as the source for the artifact visual. The code and settings are evidence of the configuration changes; they do not, by themselves, prove a complete end-to-end blocked-action test or a persistent audit record.

## Editorial note
The three Page 2 cards combine the Session 25 investigation and Session 26 remediation. The Session 26 notebook requires before-and-after behavioural evidence: the sensitive action must not execute directly, the request must enter human review, and an audit record must be created. Do not present those runtime checks as verified unless the corresponding evidence is available.
