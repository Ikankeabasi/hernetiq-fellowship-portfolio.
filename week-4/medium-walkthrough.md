# AI Security Defense Lab Level 1: My First Hands-on Cloud Security Investigation

*From reading about cloud attacks to investigating one myself.*

<img width="960" height="442" alt="Screenshot 2026-07-28 204706" src="https://github.com/user-attachments/assets/cf8121c6-a196-4967-973b-5580f778ce18" />



## Introduction

Until this lab, CloudTrail, IAM policies, hardcoded credentials, and incident response were concepts I had only studied. I understood the definitions, but I had never worked through a realistic cloud security incident from beginning to end.

Level 1 of the AI Security Defense Lab changed that.

Instead of acting as an attacker, I took the role of a Blue Team Security Analyst. The attack had already happened. My responsibility was to investigate how the attacker got into the environment, determine what they did, identify the security mistakes that made the breach possible, and apply the appropriate fixes.

The fictional company in this scenario was **MedVitals AI**, a healthcare startup that uses AI to help patients through an online medical triage platform. Since the application stores sensitive patient information, securing its cloud environment is critical.

---

# Setting Up the Lab

The first step was to fork the official AI Security Defense Lab repository into my own GitHub account.

Forking creates a personal copy of the project, allowing me to make changes without affecting the original repository. It also gives me a public record of every improvement I make, which can later serve as evidence of my practical experience.

After forking the repository, I deployed my own copy using Streamlit Community Cloud.

Once the deployment finished, I created my account and logged into the lab dashboard where Level 1 became available.

<img width="1919" height="914" alt="Screenshot 2026-08-01 140625" src="https://github.com/user-attachments/assets/ece85e31-760d-463e-8e98-de8fbc7bb917" />

---


# Understanding the Scenario

Before touching any code, I carefully read the scenario.

The developers at MedVitals AI had made two serious security mistakes while rushing to meet a business deadline.

The first mistake was storing sensitive AWS credentials directly inside the application source code instead of protecting them as environment variables.

The second mistake was attaching an IAM policy that allowed **any action on any resource** using wildcard (`*`) permissions.

Reading the scenario immediately helped me understand an important lesson:

**Security problems often begin with small configuration mistakes, not sophisticated hackers.**

---

# Investigating the Deployment Files

The lab provided two important files to inspect:

* `config.py`
* `deploy-role-policy.json`

## config.py

The configuration file contained production secrets written directly into the source code.

I found values such as:

* AWS Secret Access Key
* Database credentials
* Session secret
* Other production configuration values

Anyone who could view this repository would immediately have access to these credentials.

This is known as **hardcoded credentials**, and it is considered a serious security vulnerability because automated tools constantly scan public repositories looking for exposed secrets.

<img width="5998" height="3372" alt="Screenshot 2026-07-31 214729" src="https://github.com/user-attachments/assets/a22146de-d447-420d-92c4-3d5fa02403b8" />

---


## deploy-role-policy.json

The IAM policy was even more concerning.

Instead of allowing only the permissions required by the application, the policy granted access to:

* every action (`Action: "*"`)
* every resource (`Resource: "*"`)

This completely violated the Principle of Least Privilege.

If an attacker obtained the exposed credentials, there would be almost nothing preventing them from taking control of the AWS environment.

<img width="5968" height="2057" alt="Screenshot 2026-07-31 214729" src="https://github.com/user-attachments/assets/032337fc-cbbe-4723-bac8-ba040685cc6e" />

---


# Investigating the CloudTrail Logs

After identifying the two major security weaknesses, the next task was to investigate what actually happened inside the AWS environment.

The lab provided **17 CloudTrail events**, which represented everything that happened within a four-hour period.

Instead of immediately searching for suspicious activities, I first established what **normal behaviour** looked like. This made it much easier to identify where the attack began.

CloudTrail records every API request made inside an AWS account. Every event contains useful information such as:

* Who performed the action
* What action was performed
* When it happened
* Where the request came from
* How the request was made

Rather than reading every field randomly, I used the **5Ws investigation framework** introduced during the lab:

* **Who** performed the action?
* **What** happened?
* **When** did it happen?
* **Where** did the request come from?
* **How** was the action performed?

This simple framework helped me read the logs like an investigator instead of just looking at raw JSON data.

<img width="866" height="1021" alt="screencapture-cyberdammy-ai-security-defense-lab-hf-space-2026-07-31-22_31_32" src="https://github.com/user-attachments/assets/68098237-44e3-495a-be9e-e79d4bfd99ef" />

---


# Establishing Normal Behaviour

The first thirteen events all followed a consistent pattern.

The requests came from an internal private IP address.

The activities included normal operational tasks such as reading objects, updating Lambda functions, creating log groups, and describing EC2 resources.

The user agents were legitimate AWS tools like:

* aws-cli
* aws-sdk-java
* aws-sdk-python

Everything looked like normal application behaviour.

At this point, I had established my baseline.

From this moment onward, any significant deviation from this pattern became a potential Indicator of Compromise (IoC).

---

# Finding the First Suspicious Event

The investigation changed at **Event 14**.

Several things immediately stood out.

The request originated from an **external IP address** that had never appeared in the previous events.

Instead of using an AWS SDK, the request used **python-requests**, which is simply a generic Python HTTP library.

The action being performed was **AssumeRole**, meaning someone was attempting to obtain another role's permissions.

Even more concerning, the event happened around **03:02 UTC**, outside the company's normal operating pattern.

Seeing all these indicators together strongly suggested that this was not legitimate activity.

This became the first confirmed Indicator of Compromise.

---

# Reconstructing the Attack

Once the attacker successfully assumed the administrative role, the remaining events became much easier to understand.

The attacker followed a clear sequence.

First, they listed every S3 bucket in the AWS account to discover available storage locations.

Next, they uploaded an archive into the patient records bucket.

Finally, they downloaded that same archive from the cloud environment.

From the CloudTrail logs, I could reconstruct the entire attack timeline.

The attacker:

1. Gained access using exposed credentials.
2. Assumed a privileged IAM role.
3. Enumerated the available S3 buckets.
4. Staged patient data for export.
5. Downloaded the exported data.

The complete attack took only a little over two minutes from initial access to data exfiltration.

This demonstrated how quickly an exposed credential combined with excessive permissions can lead to a successful compromise.

<img width="1837" height="901" alt="Screenshot 2026-08-01 115605" src="https://github.com/user-attachments/assets/bd5fd7e9-e0e3-4a5b-8f5b-b8d936eff929" />

---


# Lessons From the Investigation

One of the biggest lessons I learned during this investigation was that security analysts do not rely on only one piece of evidence.

A single external IP address does not automatically indicate an attack.

A single API request is not enough either.

Instead, analysts combine multiple indicators.

In this case, the unusual source IP, the use of python-requests, the administrative role assumption, the unusual time of execution, and the subsequent access to sensitive storage together formed a clear attack pattern.

This helped me understand why behavioural analysis is often more valuable than simply checking whether an IP address has previously been reported as malicious.

---

# Fixing the Security Weaknesses

After completing the investigation, the next step was to remove the vulnerabilities that made the attack possible.

## Replacing Hardcoded Credentials

The first issue was the application's `config.py` file.

Sensitive values such as the AWS Secret Access Key, database password, and session secret were written directly into the source code. Anyone with access to the repository could immediately see these credentials.

To fix this, I replaced the hardcoded values with **environment variables** using Python's `os.environ.get()` function.

Instead of storing secrets inside the code, the application now reads them securely from the server environment at runtime.

I also created a `.env` file to hold the secret values during development.

To prevent accidental exposure, I added the following entries to `.gitignore`:

* `.env`
* `__pycache__/`
* `*.pyc`

This ensures Git will never upload sensitive files or Python cache files to the repository.

<img width="1919" height="1077" alt="Screenshot 2026-07-30 135857" src="https://github.com/user-attachments/assets/ce1ae33c-776b-4618-97ee-f751001dbbe3" />

---


# Hardening the IAM Policy

The second vulnerability was the overly permissive IAM policy.

Originally, the policy used wildcard permissions (`Action: "*"` and `Resource: "*"`) which effectively granted unlimited access to the AWS account.

I replaced it with a **least-privilege IAM policy**.

Instead of allowing every action, the new policy grants only the permissions the application actually needs, such as reading and writing specific S3 objects, creating CloudWatch logs, updating Lambda functions, and describing EC2 resources.

The policy is also restricted to only the required S3 buckets instead of the entire AWS account.

This significantly reduces the potential damage if the credentials are ever compromised again.

One important lesson I learned here is that **security is not just about preventing attacks—it is also about limiting the impact if an attack succeeds.**

<img width="1919" height="1074" alt="Screenshot 2026-07-30 142620" src="https://github.com/user-attachments/assets/603d098e-2916-47a0-b885-546fcc222765" />

---


# Committing the Changes

After completing the fixes, I committed my changes to my forked GitHub repository.

This step is more important than I originally thought.

The commit history provides permanent evidence of exactly what I changed and when I changed it.

Instead of simply saying that I understand cloud security, I now have publicly verifiable proof showing that I identified vulnerabilities and implemented the appropriate fixes.

That is far more valuable to recruiters and hiring managers than simply listing skills on a CV.

<img width="1918" height="1079" alt="Screenshot 2026-07-31 211133" src="https://github.com/user-attachments/assets/018cf3d8-7a0d-4bc5-84e2-3b86b35af80b" />

---


# What I Learned

Before this lab, CloudTrail, IAM policies, and incident response mostly existed as theory in my notes.

Working through this investigation changed that.

I learned how to establish a baseline of normal behaviour before looking for suspicious activity. I learned how attackers can abuse exposed credentials to gain privileged access in a matter of minutes. Most importantly, I learned that small configuration mistakes—like hardcoding secrets or using wildcard IAM permissions—can have serious consequences for an entire organization.

This lab also helped me appreciate the role of a Blue Team analyst. The job is not just to respond after an incident, but to understand what happened, explain it clearly, and implement controls that prevent similar incidents from happening again.

---

# Conclusion

Completing Level 1 gave me practical experience in several areas of cloud security and incident response.

During this lab, I:

* Investigated AWS CloudTrail logs.
* Applied the 5Ws framework to analyze security events.
* Identified Indicators of Compromise (IoCs).
* Reconstructed the attack timeline.
* Removed hardcoded credentials.
* Protected secrets using environment variables and `.gitignore`.
* Replaced an overly permissive IAM policy with a least-privilege policy.
* Documented my findings and submitted evidence through GitHub.

More importantly, I moved beyond simply reading about cloud security. I experienced what it feels like to investigate an incident, understand the attacker's actions, and apply real-world defensive practices.
 
This lab has strengthened my understanding of cloud infrastructure security and provided practical evidence that I can continue building on as I progress through the remaining AI Defense Lab levels.

---

# Medium Walkthrough

**Published Article:**
https://medium.com/@ikanke2021/ai-security-defense-lab-level-1-my-first-hands-on-cloud-security-investigation-21a05cfe567b?sharedUserId=ikanke2021
> This Markdown version is a backup copy of my published Medium article. The complete article, including all seven screenshots, is available at the Medium link above.
