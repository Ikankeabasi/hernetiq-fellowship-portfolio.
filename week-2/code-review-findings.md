# Week 2 — Code Review Findings: MedVitals AI

## 1. What This Script Does

This Python script is used by MedVitals AI to generate summaries of patient medical records using an AI model. It also connects to the hospital database and cloud services needed for the application to work. Hospital staff rely on this system to quickly access patient information, so it must be properly secured.

---

## 2. Security Findings

### Finding 1 — Hardcoded Credentials

    DATABASE_URL = "postgres://..."
    AI_MODEL_KEY = "sk-..."

- **Line(s):** Section 1
- **What it is:** Sensitive information such as the AI API key, database credentials, and internal token are written directly inside the source code.
- **Why it matters:** If someone gains access to the code, they can steal these credentials, access confidential patient data, misuse paid AI services, and create unexpected financial costs for the organisation.
- **Business Impact:** This could lead to data breaches, service abuse, financial loss, and damage to the hospital's reputation.
- **Fix:** Store all secrets in environment variables using `os.environ.get()` instead of writing them directly in the code.

---

### Finding 2 — Overly Permissive IAM Policy

    "Action": "*",
     "Resource": "*"

- **Line(s):** Section 2
- **What it is:** The IAM policy uses `"Action": "*"` and `"Resource": "*"`, allowing unrestricted access to all resources.
- **Why it matters:** If an attacker compromises the account, they could perform any action, including deleting systems, accessing sensitive data, or changing cloud resources.
- **Business Impact:** Excessive permissions increase the risk of major security incidents, operational disruption, and significant financial losses.
- **Fix:** Apply the principle of least privilege by granting only the permissions required for each specific task.

---

### Finding 3 — Missing Secret Management

    print(f"Connected to: {DATABASE_URL}")
    print(f"AI Key: {AI_MODEL_KEY}")

- **Line(s):** Section 4
- **What it is:** The script prints the database URL and AI API key directly to the terminal logs, exposing sensitive information.
- **Why it matters:** Anyone with access to the application logs could view and misuse these secrets to gain unauthorised access.
- **Business Impact:** Exposed secrets in logs can result in compromised systems, customer data exposure, and increased incident response costs.
- **Fix:** Never print secrets to logs. Store them securely using environment variables and ensure sensitive values are masked or omitted from log output.

---

## 3. Overall Risk Rating

**Critical**

The script contains multiple high-risk security issues, including exposed credentials, excessive cloud permissions, and poor secret management. If exploited together, these weaknesses could allow attackers to compromise sensitive patient information, misuse cloud resources, and seriously impact the organisation.

---

## 4. Reviewed By

**Ikanke Asuquo** — HerNetIQ AI Security Fellowship, Cohort 1, 2026
