# Recommended Actions — NovaPay AI (Week 15)

These actions are linked to the same four findings in the Week 14 governance gap assessment and the Week 15 board report. Each action has an accountable role, timeframe and measurable completion evidence.

1. **Protect client records**
   - **Owner:** CTO / customer-access engineering lead
   - **Timeframe:** Within 7 days
   - **Action:** Require an independent review of customer-data separation and correct the authorisation gap in the reviewed access paths.
   - **Measurable outcome:** Review signed off; automated tests demonstrate that one client cannot view another client's records; release is blocked until evidence is accepted.

2. **Stop unreviewed data use**
   - **Owner:** data-governance lead
   - **Timeframe:** Disable the unreviewed source immediately; complete controls within 14 days
   - **Action:** Keep the external source disabled until documented approval, integrity checks, data-quality checks and fairness review are complete. Failed checks must stop processing.
   - **Measurable outcome:** Manifest records approval and validation status; tests demonstrate that unapproved or invalid data cannot proceed.

3. **Gate model releases**
   - **Owner:** CTO and AI release owner
   - **Timeframe:** Before the next production release and no later than 7 days
   - **Action:** Require acceptable evaluation results and a named person's approval before a retrained model is promoted to production. Retain rollback readiness.
   - **Measurable outcome:** Every release has recorded evaluation results, named approver, model version, deployment trigger and a tested rollback path; missing approval prevents release.

4. **Resolve fairness and monitoring gaps**
   - **Owner:** risk and compliance lead with credit and fraud model owners
   - **Timeframe:** Assign owners and triage both incidents within 48 hours; complete testing and alerting within 14 days
   - **Action:** Document triage and containment decisions, run postcode fairness checks, define thresholds for significant changes and configure alerts for significant changes in model performance or outcomes. Do not state a root cause unless evidence supports it.
   - **Measurable outcome:** Both incidents have named owners and recorded decisions; fairness results, agreed thresholds and evidence of a successful alert test are retained.
