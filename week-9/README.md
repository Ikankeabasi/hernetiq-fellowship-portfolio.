# Week 9 — RAG Security & Threat Modeling

This week marked the beginning of Domain 4, focusing on Data Pipelines and RAG Security using the PayGuard FinTech scenario.

I worked on understanding how a RAG system moves documents through chunking, an embedding model and a vector database, and how user questions are retrieved and passed to the AI model.

### RAG Pipeline

**Knowledge flow:**

`Documents → Chunking → Embedding Model → Vector Database`

**Retrieval flow:**

`User Question → Embedding Model → Vector Database → AI Model → Response`

### Security Areas I Focused On

- **Cross-Tenant Data Leakage** — where one tenant could retrieve another tenant's data from the vector database if isolation is not enforced.
- **Knowledge Base Poisoning** — where malicious content can be introduced into the knowledge base and later retrieved by the AI.
- **Embedding Model Supply Chain Attack** — where an unverified embedding model could introduce a supply-chain risk.

I also applied **STRIDE** to the vector database, looking at Spoofing, Tampering, Repudiation, Information Disclosure, Denial of Service, and Elevation of Privilege.

The main security controls I looked at included authentication, tenant isolation, restricted write access, audit logging, role-based access control, rate limiting, query-size limits, and server-side retrieval filtering.

### Evidence

- [RAG Pipeline Flow Diagram](./week-9-rag-pipeline-diagram.png)
- LinkedIn: https://lnkd.in/p/eYsbFwet 
