# Week 6 — DataForge ML: AI Model Supply Chain Security

This folder contains my deliverables for Week 6 of the HerNetIQ AI Security Fellowship (Cohort 1).

## Overview

This week focused on AI model supply-chain security using the DataForge ML Level 2 lab.

The practical challenge involved auditing an AI model deployment pipeline, investigating the source repository of a downloaded model, running Picklescan against the model fixture, identifying the embedded threat, and hardening the model-loading process.

## Deliverables

### 1. Model Security Assessment

- File: `week-6-model-security-assessment.md`
- Documents the DataForge ML model investigation, Picklescan findings, supply-chain risks, business impact, remediation plan, MITRE ATLAS classification, and OWASP LLM mappings.

### 2. Level 2 AI Defense Lab

- Lab: DataForge ML — AI Model Supply Chain Security
- Level: Level 2
- Focus: AI model supply-chain security
- Tool: Picklescan
- Secure model format: safetensors
- Framework: MITRE ATLAS
- Level 2 classification: AML.T0010 — ML Supply Chain Compromise

### 3. GitHub Evidence

- Level 2 hardening commit:
  `https://github.com/Ikankeabasi/ai-security-defense-lab/commit/b85b96cb428457f5d5f2c45deade0e97076084de`

## Key Findings

The DataForge ML deployment downloaded `genomics_analyzer_v2.pkl` from the `logix-community/genomics-analyzer-v2` Hugging Face repository.

The model was stored in the legacy Pickle format and was loaded without a security scan or integrity verification.

Picklescan detected:

- 1 infected file
- 1 dangerous global
- `subprocess check_output`

The investigation identified the following supply-chain risk factors:

- Unverified account
- No checksum provided
- Licence is unknown
- No model card is provided
- The model uses the legacy .pkl format

## Security Hardening

The Level 2 fix replaced unsafe Pickle loading with safetensors, added a mandatory Picklescan pre-load security gate, changed the model source to the verified repository specified by the walkthrough, and introduced model integrity verification into the remediation plan.

## Skills Demonstrated

- AI model supply-chain security
- Static malware analysis
- Picklescan
- Secure model loading
- safetensors
- MITRE ATLAS
- OWASP LLM security mapping
- MLOps security
- Supply-chain risk assessment
- Security documentation
- Git and GitHub workflow

## Status

- ✅ Picklescan investigation completed
- ✅ Model Threat Assessment completed
- ✅ MITRE ATLAS AML.T0010 classification completed
- ✅ Level 2 hardening completed
- ✅ Level 2 commit completed
- ✅ Week 6 evidence submission
