# Week 10 RAG Security Assessment

## 1. Poisoning Vectors

### Retrieval-Time Poisoning

**What the attacker does:**

The attacker submits a fake invoice or modified payment document into PayGuard's knowledge base and gets it ingested. The document contains false information that can affect answers about an invoice or payment dispute.

**What the user experiences:**

A customer asks PayGuard's AI about an invoice or payment dispute. The AI retrieves the poisoned document and gives the customer wrong information or wrong advice about the payment or dispute.

**Blue Team indicator of compromise:**

The Blue Team finds an invoice or document that came from an unapproved or unexpected source. The document may also contain information that does not match PayGuard's original financial records. The ingestion record and source of the document should be checked.

### Training-Time Fine-Tuning Poisoning

**What the attacker does:**

The attacker gets false or deliberately misleading financial examples into the dataset used to fine-tune PayGuard's model. The poisoned examples teach the model an incorrect way of reasoning about invoices or payment disputes.

**What the user experiences:**

The model keeps giving wrong advice about payment disputes even when the correct information is already in the knowledge base. The problem is now in what the model has learned, not just in the documents being retrieved.

**Blue Team indicator of compromise:**

The Blue Team notices a repeated pattern of wrong answers during model testing. When the fine-tuning dataset is reviewed, suspicious or incorrect training examples are found, together with a change in the model's behaviour that cannot be explained by the knowledge base.

## 2. Embedding Model Audit

For this assessment, I would use **BAAI/bge-small-en-v1.5**, the embedding model identified in the session as the trustworthy comparison model.

### 1. Publisher Verification

**Check:** Is the publisher identifiable and accountable?

**Finding:** BAAI is an identifiable organisation, not an anonymous community account. The model is published under the BAAI account with a public model page and project information.

**Decision:** Pass.

### 2. Training Data Provenance

**Check:** Can we understand where the model's training data came from?

**Finding:** The model documentation explains that BGE models are trained using large-scale text-pair data with contrastive learning and provides information about the training approach. This gives PayGuard more information to assess than an embedding model with no training information at all.

**Decision:** Pass, but PayGuard should still review the training-data documentation before using the model for sensitive financial data.

### 3. Evaluation Results

**Check:** Does the model have published evaluation results?

**Finding:** The model card provides MTEB evaluation results, including retrieval results. This gives PayGuard a way to judge the model's retrieval performance instead of accepting it without evidence.

**Decision:** Pass.

### 4. Intended Use Documentation

**Check:** Is it clear what the model is designed to do?

**Finding:** The model is documented for sentence similarity, semantic search and information retrieval, which matches the role of an embedding model in PayGuard's RAG system.

**Decision:** Pass.

### 5. Active Maintenance

**Check:** Is the model publicly maintained and does it have an update history?

**Finding:** The model has a public repository history, documented releases and visible project activity. It is also possible to review its model files and documentation rather than depending on an unknown private copy.

**Decision:** Pass, with continued review required before accepting future model updates.

### Approval Decision

**I would approve BAAI/bge-small-en-v1.5 for PayGuard's initial use.** The main reason is that it has an identifiable publisher, documented training approach, published evaluation results, clear retrieval-related use, and public project history. I would still review the model again whenever PayGuard changes the model version or makes a major update.

## 3. Filter Enforcement Gap

The application-layer filter first gets the user's `tenant_id`, checks that it exists, and then searches the vector database. The problem is that the database search happens before the tenant filter is applied. The application receives results from all tenants and only removes the results belonging to other tenants afterwards.

This looks like the right fix because the final results shown to the user are supposed to contain only that user's company's data. However, the unauthorised data has already been retrieved from the database before the filtering happens. In a regulated FinTech system, that retrieval can itself be a security or compliance problem.

The second problem is that the protection only exists in the application. If an attacker can reach the vector database without going through the application, the application filter is never executed.

**What an attacker needs to exploit it:**

The attacker needs a way to bypass or directly reach the vector database instead of going through the normal application path. Once direct access is possible, they can send a search request to the database and receive results from different tenants because the application-layer filter is no longer involved.

## 4. Recommendations

1. **Control who can add documents to PayGuard's knowledge base.** Only approved sources should be allowed to submit documents for ingestion. Every new document should be checked before the AI is allowed to use it, especially invoices and payment records.

2. **Move the customer-company check into the database query itself.** PayGuard should make the database return only records belonging to the company making the request. This prevents the protection from disappearing when someone reaches the database without using the application.

3. **Keep one approved embedding model and review it before updates.** PayGuard should record the exact model version being used, review its publisher, training information, evaluation results and intended use before accepting a new version, and test retrieval with PayGuard's own invoice and dispute examples before putting an update into use.
