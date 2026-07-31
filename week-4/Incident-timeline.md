# Incident Timeline Report – MedVitals AI

## Incident Summary

During the Level 1 AI Defense Lab investigation, I analyzed AWS CloudTrail logs to determine how an attacker compromised the MedVitals AI cloud environment. The investigation showed that two security weaknesses allowed the breach, leading to unauthorized access and patient data exfiltration.

---

## Vulnerability 1 – Hardcoded Credentials

**Location:** `config.py`

Sensitive credentials such as the AWS Secret Access Key, database password, and session secret were stored directly inside the application source code.

### Why this is dangerous

Anyone who gains access to the repository can immediately use those credentials to access the company's AWS environment.

---

## Vulnerability 2 – Over-Permissive IAM Policy

**Location:** `deploy-role-policy.json`

The IAM policy used wildcard permissions (`Action: *` and `Resource: *`).

### Why this is dangerous

If an attacker obtains valid credentials, they automatically receive full administrative access to every AWS resource.

---

# Attack Timeline

| Time (UTC)   | Event       | Description                                                                                                             |
| ------------ | ----------- | ----------------------------------------------------------------------------------------------------------------------- |
| Before 03:02 | Events 1–13 | Normal system activity from internal IP address using official AWS tools. These events established the normal baseline. |
| 03:02:09     | AssumeRole  | The attacker used stolen credentials from an external IP address to assume an administrator role.                       |
| 03:02:31     | ListBuckets | The attacker listed all available S3 buckets to discover valuable data.                                                 |
| 03:03:02     | PutObject   | The attacker created an archive containing patient records for exfiltration.                                            |
| 03:04:18     | GetObject   | The attacker downloaded the archive, successfully completing the data theft.                                            |

---

# Events Considered Noise

Events **1–13** were excluded because they represented legitimate operational activities.

Reasons:

* Internal private IP address
* Official AWS CLI and SDK tools
* Normal deployment and maintenance operations
* Expected service account behaviour

These events helped establish the baseline for identifying abnormal activity.

---

# Security Fixes Implemented

## 1. Removed Hardcoded Credentials

Sensitive values were replaced with environment variables using:

* `os.environ.get()`
* `.env`
* `.gitignore`

This prevents secrets from being stored inside source code.

---

## 2. Hardened IAM Permissions

The wildcard IAM policy was replaced with a Least Privilege policy.

Permissions now allow only the specific actions required by the application on the approved resources.

---

# Business Impact

If this incident occurred in a real healthcare organization, attackers could steal confidential patient records, violate privacy regulations such as HIPAA, damage customer trust, and negatively affect investment or funding opportunities.

Implementing proper secrets management and Least Privilege significantly reduces the likelihood and impact of similar attacks.

---

# Key Lessons Learned

This investigation demonstrated how to:

* Analyze CloudTrail logs
* Identify Indicators of Compromise (IoCs)
* Establish a baseline of normal activity
* Detect abnormal behaviour
* Remove exposed credentials
* Apply Least Privilege IAM
* Produce an incident investigation report suitable for both technical and non-technical audiences
