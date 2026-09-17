# Week 10 — Data Pipelines & RAG Security

Domain 4 uses the PayGuard FinTech scenario and covers Sessions 17–20.

## Sessions 17–18 — RAG Matrix + STRIDE Threat Modeling

### Deliverable 1 — RAG Pipeline Diagram
- File: `week-10-rag-pipeline-diagram.png` (or Markdown with embedded diagram)
- Show the ingestion flow: Documents → Chunking → Embedding Model → Vector Database.
- Show the retrieval flow: User Question → Embedding Model → Vector Database → AI Model → Response.
- Annotate the three required attack surfaces:
  - Cross-Tenant Data Leakage — Vector Database
  - Knowledge Base Poisoning — document injection point
  - Embedding Model Supply Chain Attack — Embedding Model

### Deliverable 2 — STRIDE Matrix
- File: `week-10-stride-matrix.md`
- Cover at least four RAG components.
- For each component, apply at least three STRIDE categories.
- Each entry needs a plain-English threat description and High/Medium/Low severity.
- The Vector Database entry was completed in class and serves as the reference.

### Deliverable 3 — Wednesday LinkedIn Post
- Write in my own words, voice, and experience.
- Explain what it felt like to think through possible attacks before they happen.
- Reflect on what the RAG diagram revealed and which STRIDE category surprised me most.
- Visual proof: screenshot of the RAG pipeline diagram or STRIDE matrix.

## Sessions 19–20 — RAG Poisoning + Metadata Filter Enforcement

### Deliverable 4 — RAG Security Assessment
- File: `week-10-rag-security-assessment.md`
- Section 1: Poisoning Vectors — retrieval-time and training-time; attacker action, user experience, and Blue Team IoC for each.
- Section 2: Embedding Model Audit — five behavioural trust checks and whether the model should be approved, with reasons.
- Section 3: Filter Enforcement Gap — explain the application-layer failure and what an attacker needs to exploit it.
- Section 4: Recommendations — three specific, actionable recommendations for a non-technical FinTech founder; no jargon or generic advice.

### Deliverable 5 — Filter Enforcement Writeup
- File: `week-10-filter-enforcement-writeup.md`
- Explain the application-layer filter and why it looks correct.
- Explain the failure scenario and bypass.
- Explain the database-layer fix and why the bypass no longer works.
- Include one original analogy, not the class analogy.
- Reference what I saw in the live demo. Use my own words; no copy-paste from the Fellow Notes.

### Deliverable 6 — Wednesday LinkedIn Post
- Write in my own words, voice, and experience.
- Explain watching a security fix fail live: correct-looking code bypassed in three lines.
- Explain what that teaches about where a defence must be enforced.
- Address what I would tell a developer who says application-level security means database-level controls are unnecessary.
- Visual proof: screenshot of the bypass demo or database-layer fix code.

## Submission

- Due: Monday, 12 Noon WAT.
- Submit to `#project-submissions` on Slack.
- Provide direct GitHub URLs for the required Markdown deliverables.
