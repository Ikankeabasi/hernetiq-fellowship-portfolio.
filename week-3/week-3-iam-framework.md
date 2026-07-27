# Hardened Cloud IAM Framework

## 1. Incident Summary

On July 10, 2026, the MedVitals AWS environment experienced a security incident involving the compromise of the `medvitals-backup-user` IAM account. An attacker used the compromised account to explore cloud resources, create a new IAM user, and grant that user full AdministratorAccess privileges. This resulted in persistent privileged access to the AWS account.

---

## 2. Attack Timeline

| Time (UTC) | Event | Description |
|------------|-------|-------------|
| 01:12:44 | GetCallerIdentity | The attacker verified that the stolen AWS credentials were valid and confirmed the identity of the compromised IAM user. |
| 01:14:09 | DescribeInstances | The attacker enumerated EC2 resources to understand the cloud environment before taking further action. |
| 01:19:31 | CreateUser | A new IAM user named **medvitals-support-svc** was created. This appears to be a backdoor account created for persistent access. |
| 01:26:58 | AttachUserPolicy | The attacker attached the **AdministratorAccess** managed policy to the newly created user, giving it unrestricted administrative privileges across the AWS account. |

---

## 3. Root Cause Analysis

The attack succeeded because the compromised IAM account had excessive permissions that violated the Principle of Least Privilege.

### Security weaknesses identified

- The compromised account was allowed to create new IAM users (`iam:CreateUser`).
- The compromised account was allowed to attach IAM policies (`iam:AttachUserPolicy`).
- The AdministratorAccess policy granted unrestricted control over the AWS account.
- No IAM conditions or additional restrictions were in place to limit where or when privileged actions could be performed.
- Suspicious activity from an unfamiliar IP address and automated Python client was not detected or blocked.

---

## 4. Hardened IAM Policy

The MedVitals backup application should only have the permissions required for its backup tasks.

Replace the excessive IAM permissions with a least-privilege policy similar to the hardened policy created in Session 5.

The application should:

- Read only the required S3 backup bucket.
- Access only approved backup resources.
- Never create IAM users.
- Never attach IAM policies.
- Never modify IAM roles.
- Never grant AdministratorAccess.
- Never perform privilege escalation.

---

## 5. Recommendations

To reduce the likelihood of future incidents, MedVitals should:

1. Disable and rotate the compromised AWS credentials immediately.
2. Delete the unauthorized IAM user (`medvitals-support-svc`).
3. Remove any AdministratorAccess permissions that were improperly assigned.
4. Apply Least Privilege to every IAM user and role.
5. Enable MFA for all privileged accounts.
6. Configure CloudTrail monitoring and SIEM alerts for IAM activities such as CreateUser and AttachUserPolicy.
7. Regularly audit IAM permissions and remove unnecessary access.
8. Review CloudTrail logs continuously for suspicious activity from unfamiliar IP addresses or automated scripts.
