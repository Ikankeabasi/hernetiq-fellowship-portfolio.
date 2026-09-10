# Week 9 — RAG Pipeline & STRIDE Threat Modeling

## Overview

This week introduced Domain 4: Data Pipelines & RAG Security through the PayGuard FinTech scenario. The sessions focused on understanding how a Retrieval Augmented Generation (RAG) system retrieves information from a vector database and how security threats can affect that retrieval process.

The work covered the RAG pipeline, vector databases, chunking, embeddings, retrieval security, and STRIDE threat modeling applied to the vector database.

## RAG — Retrieval Augmented Generation

RAG is an AI system approach in which the system retrieves relevant information from a knowledge base before generating a response. Instead of relying only on the AI model's training data, the system retrieves specific documents or chunks and uses them to build the answer.

PayGuard uses RAG so its AI can answer questions about customer invoices, payment histories, and account balances.

## RAG Pipeline

### Document and Vector Data Flow

```text
Documents → Chunking → Embedding Model → Vector Database
```

- **Documents** — source information that enters the knowledge base.
- **Chunking** — large documents are split into smaller pieces before embedding. Each chunk receives its own vector.
- **Embedding Model** — converts text into vectors, which represent the meaning of the text as numbers.
- **Vector Database** — stores the vectors and allows searches based on meaning.

### Retrieval Flow

```text
User Question → Embedding Model → Vector Database → AI Model → Response
```

The retrieval process works as follows:

1. The user sends a question.
2. The question is converted into an embedding.
3. The vector database searches for the closest relevant vectors.
4. Relevant chunks are returned to the AI model.
5. The AI model uses the retrieved information to generate the response.

## Retrieval Security Risks

The sessions identified three important attack surfaces in the RAG pipeline.

### 1. Cross-Tenant Data Leakage

**Location:** Vector Database

PayGuard serves multiple companies. If the vector database does not enforce tenant isolation, a query from one company could retrieve another company's invoice or financial data.

The retrieval system must explicitly enforce tenant isolation rather than assuming that semantic search will understand which data belongs to which customer.

### 2. Knowledge Base Poisoning

**Location:** Documents / knowledge-base flow

An attacker can inject malicious content into the knowledge base. When a user's question retrieves the poisoned content, the AI may use that content when generating its response.

The injection happens once, but the effect can extend to every query that retrieves the poisoned chunk.

### 3. Supply Chain Attack

**Location:** Embedding Model

The embedding model used to translate documents into vectors can itself be a downloaded model. If it comes from an unverified source, the model may introduce a supply-chain risk.

## STRIDE Threat Modeling

STRIDE is a threat modeling framework used to work through six categories of security threats systematically:

| Letter | Threat | RAG Example |
|---|---|---|
| S | Spoofing | A query pretending to come from an authorised tenant |
| T | Tampering | Injecting malicious content into the knowledge base |
| R | Repudiation | No audit log of what was retrieved and when |
| I | Information Disclosure | Cross-tenant leakage from the vector database |
| D | Denial of Service | Flooding the embedding model with oversized documents |
| E | Elevation of Privilege | A query retrieving admin-level financial data |

### STRIDE Applied to the Vector Database

The vector database was examined against each STRIDE category:

- **Spoofing:** Possible when retrieval requests are not authenticated and the caller can claim another tenant's ID.
- **Tampering:** Possible when write access to the vector database is not restricted.
- **Repudiation:** A risk when retrieval activity is not logged, making it difficult to determine what was retrieved, when, or by whom.
- **Information Disclosure:** Possible when metadata filters do not enforce tenant isolation.
- **Denial of Service:** Possible when retrieval requests are not rate-limited.
- **Elevation of Privilege:** Possible when document access is not role-scoped and lower-privilege users can retrieve higher-level documents.

## Blue Team Controls Covered

The STRIDE deep dive described defensive controls for the PayGuard vector database, including:

- Authenticate every retrieval request.
- Derive the tenant ID from the authenticated identity rather than trusting a caller-supplied tenant ID.
- Restrict vector-database write access to the ingestion pipeline.
- Use role-based access control at the database level.
- Log every retrieval query with timestamp, authenticated identity, tenant ID, query text, retrieved chunks, and document IDs.
- Keep audit logs immutable and separate from the system being logged.
- Attach `tenant_id` metadata to every chunk during ingestion.
- Enforce tenant filtering server-side on every retrieval query.
- Apply document access levels such as customer, support, executive, and admin.
- Enforce both tenant and access-level filters server-side.
- Apply rate limits and query-size limits to protect retrieval resources.
- Monitor query volume and alert on unusual activity.

## Week 9 Deliverables

### Deliverable 1 — Vector Data Pipeline Flow Diagram

The diagram must show the RAG components in sequence:

```text
Documents → Chunking → Embedding Model → Vector Database
```

and the retrieval flow:

```text
User Question → Embedding Model → Vector Database → AI Model → Response
```

It must also show the three attack surfaces:

- **Cross-Tenant Leakage** — at the Vector Database
- **Knowledge Base Poisoning** — at the Documents / knowledge-base flow
- **Supply Chain Attack** — at the Embedding Model

### Deliverable 2 — LinkedIn Content

The content post should be written in the fellow's own words and voice about the work completed in the sessions.

The source brief asks the post to reflect on:

- What it feels like to look at a system and think about possible attacks before they happen.
- What the RAG pipeline diagram revealed that was unexpected.
- Which STRIDE category was most surprising.

The visual proof is a screenshot of the RAG pipeline diagram or STRIDE matrix.

### STRIDE Matrix Foundation

The source Evidence Brief also describes a STRIDE Matrix Foundation deliverable covering at least four RAG components, with at least three STRIDE categories per component, plain-English threat descriptions, and severity ratings.

This README does not present that matrix as completed work.
