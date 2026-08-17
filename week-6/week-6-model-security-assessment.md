## 1. Assessment Context

DataForge ML is an intentionally vulnerable BioTech AI pipeline. This Level 2 exercise focuses on AI model supply-chain security: verifying that a model obtained from an external repository is trustworthy before it is loaded into a production inference pipeline.

The vulnerable deployment downloads a model from a public Hugging Face repository and loads it with Python Pickle without a pre-load integrity or security check.

The investigation involved auditing the deployment code and model source repository, running Picklescan against the supplied model fixture, completing the Model Threat Assessment, and hardening the model-loading pipeline.

---

## 2. Picklescan Evidence

The required model fixture was scanned in the Codespace using: "picklescan -p models/genomics_analyzer_v2.pkl"

### Observed Scan Results

| Picklescan Result  | Finding |
| ------------------ | ------: |
| Scanned files      |       1 |
| Infected files     |       1 |
| Suspicious globals |       0 |
| Dangerous globals  |       1 |

The scan identified a dangerous `subprocess check_output` callable/import inside the pickle file.

The file was therefore treated as unsafe and should not be loaded into a production environment.

---

## 3. DataForge ML — Model Security Assessment

| Field                         | Your Finding                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| ----------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Model File**                | `genomics_analyzer_v2.pkl`                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| **Source Repository**         | `logix-community/genomics-analyzer-v2`                                                                                                                                                                                                                                                                                                                                                                                                                         |
| **Serialisation Format**      | Pickle (`.pkl`), a legacy Python serialisation format that can execute embedded code during loading/deserialisation.                                                                                                                                                                                                                                                                                                                                           |
| **Threats Detected**          | 1 infected file; 1 dangerous global; 0 suspicious globals.                                                                                                                                                                                                                                                                                                                                                                                                     |
| **Threat Type**               | Dangerous `subprocess check_output` callable/import identified by Picklescan, as described in the Level 2 walkthrough.                                                                                                                                                                                                                                                                                                                                         |
| **Supply Chain Risk Factors** | 1. Hugging Face account is not verified.<br>2. No checksum is provided for integrity verification.<br>3. Licence is unknown.<br>4. No model card is provided.<br>5. The model uses the legacy `.pkl`/Pickle format.                                                                                                                                                                                                                                            |
| **Business Impact**           | Loading the malicious pickle could execute the embedded payload in the DataForge ML production pipeline. Because the pipeline processes patient sample data, successful exploitation could allow an attacker to access, modify, or exfiltrate sensitive data and potentially execute additional commands using the privileges available to the pipeline. This could result in data exposure, service disruption, and compromise of the production environment. |
| **Remediation Plan**          | Replace unsafe Pickle loading with `safetensors`; add Picklescan as a mandatory pre-load security gate; use a verified model source; and introduce model integrity verification before allowing models into the production pipeline.                                                                                                                                                                                                                           |

---

## 4. MITRE ATLAS and OWASP LLM Classification

The incident involves AI model supply-chain compromise and a malicious model file.

| Finding                 | OWASP LLM Mapping                          | MITRE ATLAS Mapping                        |
| ----------------------- | ------------------------------------------ | ------------------------------------------ |
| Supply chain compromise | **OWASP LLM05 — Improper Output Handling** | **AML.T0010 — ML Supply Chain Compromise** |
| Poisoned model file     | **OWASP LLM03 — Supply Chain**             | **AML.T0020 — Poison Training Data**       |
| Model backdoor          | **OWASP LLM03 — Supply Chain**             | **AML.T0018 — Backdoor ML Model**          |

### Primary Classification

**MITRE ATLAS:** AML.T0010 — ML Supply Chain Compromise

**Technique:** Embedding a malicious payload in `.pkl` model weights distributed through a public repository.

The primary issue is that the model was obtained from an unverified external source and loaded into the production pipeline without sufficient security verification.

---

## 5. Why the Findings Matter

The main security problem is the combination of an unverified model source, lack of integrity verification, a legacy Pickle format, and direct use of `pickle.load()` before any security gate.

Picklescan performs static analysis of the pickle file. It examines the serialisation data for dangerous patterns without loading the malicious object.

This means the model can be inspected for known dangerous pickle content before it is trusted by the application.

---

## 6. Task 3 — Hardening Performed

The original vulnerable `model_loader.py` was preserved as evidence rather than deleted.

The deployment was hardened by:

1. Preserving the original vulnerable model loader as evidence.
2. Updating the requirements section to include `safetensors` and `picklescan`.
3. Replacing unsafe Pickle loading with `safetensors` loading.
4. Adding a mandatory Picklescan pre-load security gate.
5. Changing the model source to the verified repository specified by the walkthrough.
6. Committing the hardened implementation to the GitHub fork.

The hardened implementation prevents the original unsafe Pickle loading pattern from being used and introduces a security check before the model-loading process proceeds.

---

## 7. Evidence

### Level 2 GitHub Commit

**Commit URL:**
https://github.com/Ikankeabasi/ai-security-defense-lab/commit/b85b96cb428457f5d5f2c45deade0e97076084de

This commit contains the Level 2 hardening changes made to the DataForge ML lab.

### Picklescan Evidence

The Picklescan scan was executed against:

```text
models/genomics_analyzer_v2.pkl
```

The result showed:

```text
Scanned files: 1
Infected files: 1
Suspicious globals: 0
Dangerous globals: 1
```

---

## 8. Conclusion

The DataForge ML investigation demonstrated how an AI model can become a supply-chain security risk before it reaches a production system.

The vulnerable pipeline trusted a model from an unverified public repository, used the legacy Pickle format, and loaded the model without an appropriate security gate.

The investigation identified the malicious model content with Picklescan and classified the incident using MITRE ATLAS. The model-loading process was then hardened using `safetensors`, a mandatory pre-load security gate, and a verified model source.

The main lesson is that an AI model should be treated as a software supply-chain dependency and verified before it is trusted by a production system.
