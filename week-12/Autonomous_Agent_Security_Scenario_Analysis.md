# Autonomous Agent Security Scenario Analysis

## Purpose

This analysis examines the two scenarios discussed in Session 23: an AI customer-support agent with excessive permissions and an AI system that can pass generated commands to an unrestricted execution function. The aim is to identify the security risks, the permissions and trust boundaries involved, and controls that would reduce the risk.

The session was conceptual and scenario-based. The recommendations below describe defensive controls for the scenarios.

## Scenario 1: Customer-Support Agent with Excessive Permissions

### Scenario

A customer-support agent is intended to answer customer questions and create support tickets. If it is also given permission to delete customer accounts, it has authority beyond what it needs for its normal role.

### Security risks

- **Excessive agency:** The agent can perform a destructive action that is unnecessary for its support role.
- **Tool misuse:** An incorrect decision, manipulated request, or unsafe tool call could trigger account deletion.
- **Data loss and service disruption:** Customers could lose access or important account information could be removed.
- **Large blast radius:** If the agent or one of its tools is misused, the impact could extend beyond answering questions or creating tickets.

### Permissions and trust boundaries

The main permission boundary is between the AI model's decision and the application function that changes customer records. A tool call from the model must not be treated as proof that the action is authorised. The application must independently check whether the requested action is allowed for that user, purpose and context.

### Recommended defensive controls

1. **Apply least privilege.** Give the agent only the permissions required to answer questions and create tickets. Do not grant account-deletion access if the role does not need it. This reduces the actions available if the agent behaves incorrectly.
2. **Separate sensitive tools.** Keep destructive account-management functions outside the agent's normal tool set. If account deletion is a legitimate business process, use a separate authorised workflow.
3. **Enforce authorisation in the application.** Check permissions at the tool or API boundary instead of trusting the model's decision. This prevents an AI-generated request from bypassing normal access controls.
4. **Require human approval for high-impact actions.** Where a sensitive action is genuinely necessary, require an authorised person to review it before execution.
5. **Validate tool arguments and outputs.** Check that inputs have the expected structure and values, and that the proposed action follows application rules before it reaches a sensitive function.
6. **Log important actions.** Record tool calls, outcomes and approval decisions so activity can be reviewed and investigated.

## Scenario 2: Unrestricted Code or Command Execution

### Scenario

An application exposes a function such as execute_command(command) and passes an AI-generated command to the operating system without strong restrictions. The model's output could therefore become a path to system execution.

### Security risks

- **Arbitrary command execution:** The agent may cause commands to run that were not intended by the application owner.
- **System or data damage:** Depending on the execution environment's permissions, a command could modify or delete files, disrupt services, or access sensitive information.
- **Privilege abuse:** If the execution function runs with broad permissions, the impact could be more serious than the original task requires.
- **Increased blast radius:** An unrestricted command interface gives the agent access to many possible operations instead of a small, defined set.
- **Repeated or excessive actions:** Tool-calling loops can repeat operations or continue taking actions unless the application imposes limits.

### Permissions and trust boundaries

The critical trust boundary is between AI-generated text and the operating system or other powerful execution environment. AI output must be treated as untrusted data, not automatically accepted as a trusted system instruction. The execution function and its surrounding application need their own restrictions.

### Recommended defensive controls

1. **Avoid unrestricted shell access.** Where possible, replace a general-purpose command function with a small set of specific, purpose-built tools. Each tool should perform only an approved operation.
2. **Use strict input and schema validation.** Check the structure, type, permitted values and purpose of each request before it reaches a sensitive function. Reject unexpected arguments.
3. **Use least privilege and isolation.** If execution is necessary, run it in a restricted environment with only the resources and permissions required for the task. This limits potential damage.
4. **Set execution and resource limits.** Restrict the number of records, operations, runtime or resources an agent can use. These limits reduce the impact of a mistake or loop.
5. **Validate the proposed action before execution.** The application should verify that the requested operation matches an explicit policy, rather than relying only on the model's output.
6. **Use forbidden-string checks only as a supporting control.** Blocking known dangerous strings may catch some unsafe commands, but it is not sufficient on its own because a command can be represented in other ways. Strong permission boundaries and restricted tools are more reliable.
7. **Require approval for high-impact operations and log execution.** Human review should be used where an operation could cause significant harm, and execution attempts and outcomes should be recorded.

## Shared Security Lessons

Both scenarios show that the risk is not simply that an AI system has tools. The risk increases when it has more authority than it needs or when the application trusts its output without independent checks.

The main lessons from Session 23 are:

- Give an agent only the authority needed for its assigned task.
- Treat AI-generated input as untrusted until the application validates it.
- Validate inputs and proposed actions before they reach sensitive functions.
- Limit the scale and resources of each operation.
- Enforce permissions at the application or tool boundary, not only through prompts.
- Keep records of sensitive actions and require human review where the consequences justify it.

## Conclusion

The customer-support scenario demonstrates how unnecessary permissions can turn a routine support agent into a risk to customer accounts. The command-execution scenario demonstrates how unrestricted functions can turn AI-generated text into system actions. In both cases, least privilege, strong validation, restricted tools, execution limits, logging and appropriate human approval help reduce the potential blast radius.
