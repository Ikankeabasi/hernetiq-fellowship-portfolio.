# Week 10 RAG Security Assessment

## 1. Poisoning Vectors

### Retrieval-Time Poisoning

**What the attacker does:**

I identified a case where an attacker could submit a fake invoice or modified payment document into PayGuard's knowledge base and get it ingested. The document contains false information that can affect answers about an invoice or payment dispute.

**What the user experiences:**

A customer asks PayGuard's AI about an invoice or payment dispute. The AI retrieves the poisoned document and gives the customer wrong information or wrong advice about the payment or dispute.

**Blue Team indicator of compromise:**

The indicator I would look for is an invoice or document that came from an unapproved or unexpected source. The document may also contain information that does not match PayGuard's original financial records. I would check the document's source and ingestion record.

### Training-Time Fine-Tuning Poisoning

**What the attacker does:**

I identified another case where an attacker gets false or deliberately misleading financial examples into the dataset used to fine-tune PayGuard's model. The poisoned examples teach the model an incorrect way of reasoning about invoices or payment disputes.

**What the user experiences:**

The model keeps giving wrong advice about payment disputes even when the correct information is already in the knowledge base. In this case, the problem is in what the model has learned, not just in the documents being retrieved.

**Blue Team indicator of compromise:**

The indicator I would look for is a repeated pattern of wrong answers during model testing. I would then review the fine-tuning dataset for suspicious or incorrect training examples and compare them with the change in the model's behaviour.

## 2. Embedding Model Audit

For this assessment, I would use **BAAI/bge-small-en-v1.5** as the embedding model for PayGuard's RAG system.

### 1. Publisher Verification

**Check:** Is the publisher identifiable and accountable?

**Finding:** BAAI is an identifiable organisation, not an anonymous community account. The model is published under the BAAI account with a public model page and project information.

**Decision:** Pass.

### 2. Training Data Provenance

**Check:** Can I understand where the model's training data came from?

**Finding:** The model documentation explains that BGE models are trained using large-scale text-pair data with contrastive learning and provides information about the training approach. This gives me information to assess rather than accepting an embedding model with no training information at all.

**Decision:** Pass, but I would still review the available training-data information before using the model for sensitive financial data.

### 3. Evaluation Results

**Check:** Does the model have published evaluation results?

**Finding:** The model card provides MTEB evaluation results, including retrieval results. This gives me a way to check its retrieval performance instead of accepting it without evidence.

**Decision:** Pass.

### 4. Intended Use Documentation

**Check:** Is it clear what the model is designed to do?

**Finding:** The model is documented for sentence similarity, semantic search and information retrieval, which matches the role I need from an embedding model in PayGuard's RAG system.

**Decision:** Pass.

### 5. Active Maintenance

**Check:** Is the model publicly maintained and does it have an update history?

**Finding:** The model has a public repository history, documented releases and visible project activity. I can also review its model files and documentation rather than depending on an unknown private copy.

**Decision:** Pass, with continued review before accepting future model updates.

### Approval Decision

**I would approve BAAI/bge-small-en-v1.5 for PayGuard's initial use.** My reason is that it has an identifiable publisher, documented training approach, published evaluation results, clear retrieval-related use, and public project history. Before accepting a new version, I would review the model again and test the new version with PayGuard's own data and retrieval questions.

## 3. Filter Enforcement Gap

I found that the application-layer filter first gets the user's `tenant_id`, checks that it exists, and then searches the vector database. The problem is that the database search happens before the tenant filter is applied. The application receives results from all tenants and only removes the results belonging to other tenants afterwards.

This looks like the right fix because the final results shown to the user are supposed to contain only that user's company's data. However, the unauthorised data has already been retrieved from the database before the filtering happens. In a regulated FinTech system, that retrieval can itself be a security or compliance problem.

I also found that the protection only exists in the application. If an attacker can reach the vector database without going through the application, the application filter is never executed.

**What an attacker needs to exploit it:**

The attacker needs a way to bypass or directly reach the vector database instead of going through the normal application path. Once direct access is possible, the attacker can send a search request to the database and receive results from different tenants because the application-layer filter is no longer involved.

## 4. Recommendations

1. **Control who can add documents to the knowledge base.** I would allow only approved sources to submit documents for ingestion. I would also check every new document before the AI is allowed to use it, especially invoices and payment records.

2. **Move the customer-company check into the database query itself.** I would make the database return only records belonging to the company making the request. This keeps the protection in place even if someone reaches the database without using the application.

3. **Keep one approved embedding model and review it before updates.** I would record the exact model version being used, review its publisher, training information, evaluation results and intended use before accepting a new version, and test retrieval with PayGuard's own invoice and dispute examples before putting an update into use.
