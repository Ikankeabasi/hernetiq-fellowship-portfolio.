# Week 10 — RAG Security Assessment

In Week 10, I assessed security risks in a Retrieval-Augmented Generation (RAG) system, focusing on document poisoning, embedding-model trust, and tenant-filter enforcement.

## My Deliverables

### 1. RAG Security Assessment
I documented the poisoning vectors I identified, audited the `BAAI/bge-small-en-v1.5` embedding model using five trust checks, examined the application-layer filter gap, and recorded three actionable security recommendations.

[View RAG Security Assessment](./week-10-rag-security-assessment.md)

### 2. Filter Enforcement Writeup
I explained how the application-layer filter works, the specific bypass scenario I observed, how the bypass can expose data across tenants, and why enforcing the tenant restriction at the database layer provides a stronger control. I also included my own warehouse analogy to explain the difference.

[View Filter Enforcement Writeup](./week-10-filter-enforcement-writeup.md)

### 3. LinkedIn Post
I shared my Week 10 work on LinkedIn, including the key lessons from the RAG security assessment.

[View my LinkedIn post](https://lnkd.in/p/e7D_3YAX)

## Evidence

The two documents above contain my written assessment and findings from the Week 10 lab, while the LinkedIn post provides the public record of the work I shared.
