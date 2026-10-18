# Agent Security Quick Assessment
**HerNetIQ AI Security Fellowship · Domain 5 · Week 12 · Session 24**

## 1. What does ASI01 mean?
ASI01 means **Agent Goal Hijack**. My understanding is that an attacker tries to redirect an AI agent from its original goal to another goal it was not meant to achieve. For example, a customer-support agent that should solve a complaint could be tricked into looking for private company information.

## 2. What is the difference between ASI02 and ASI03?
**ASI02 — Tool Misuse & Exploitation** is when an agent uses a legitimate tool in an unsafe or unintended way. **ASI03 — Identity & Privilege Abuse** is when the agent’s identity or permissions are abused, especially when it has more access than its task requires. In simple terms, ASI02 is about how a tool is used; ASI03 is about who or what has permission to use it.

## 3. What are an agent’s action surfaces, and why do they matter?
Action surfaces are the places where an agent can do something, such as calling tools or APIs, reading customer records, sending emails, creating tickets or issuing refunds. Each action creates a possible security risk. I would limit the agent to the tools and permissions it needs and require human approval for sensitive actions.

## 4. What does schema enforcement provide?
Schema enforcement checks whether the agent’s output follows the structure the application expects, including the required fields and data types. For example, if a field requires a phone number, the system should not accept random text in its place. This helps stop badly structured output from being passed to the next step or used in a tool call. It checks structure; it does not by itself prove that the content is safe.

## 5. What is the role of Llama Guard?
Llama Guard acts as a safety classifier. It checks content against defined safety categories and helps identify content that may be unsafe. It can be placed at important points in an AI workflow, but it is not perfect, so it should be used alongside other security controls.

## 6. How does NeMo Guardrails differ from Llama Guard?
Llama Guard mainly checks whether content appears unsafe. NeMo Guardrails helps control how the AI application behaves and how its workflow proceeds. It can set rules for input, output, dialogue and tool actions—for example, requiring human approval before a sensitive action. They address different needs and can work together.

## 7. What are the seven MAESTRO layers?
1. **Foundation Models** — the models that reason, generate content or make decisions.
2. **Data Operations** — the data the agent receives, stores, retrieves or processes.
3. **Agent Frameworks** — the software that manages planning, memory, tools and workflows.
4. **Deployment & Infrastructure** — servers, APIs, containers, credentials and runtime environments.
5. **Evaluation & Observability** — testing, logging and monitoring agent behaviour.
6. **Security & Compliance** — access controls, security policies and compliance requirements.
7. **Agent Ecosystem** — external tools, APIs, other agents, vendors and connected services.

## 8. What are the four NIST AI RMF functions?
- **Govern:** Set policies, responsibilities and accountability for AI risks.
- **Map:** Understand the system’s purpose, context, affected people, risks and possible impacts.
- **Measure:** Assess risks and check whether controls are working.
- **Manage:** Prioritise risks and decide what to control, monitor or fix.

## 9. Why should the Risk Matrix include both MAESTRO and NIST AI RMF mappings?
I use **MAESTRO** to identify the technical part of the agent system where a risk exists. I use **NIST AI RMF** to show how the organisation should understand, assess and manage that risk. Including both gives a clearer picture: where the problem may occur and how the organisation should respond to it.

---

**My key takeaway:** Agent security is not only about whether the model gives a safe answer. I also need to consider what tools it can use, what data it can access, what actions it can take and how those actions are controlled and monitored.
