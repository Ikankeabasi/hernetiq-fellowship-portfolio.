# Week 5 — Incident Report: Prompt Injection in CorpConnect Messenger

## Incident Summary

During testing of CorpConnect Messenger, an AI-powered communication agent, prompt injection was used to influence how the agent understood the identity of the user. The testing successfully affected the agent's behaviour in Levels 1 and 2. Level 3 was attempted but has not yet been successfully completed.

## What Happened

In Level 1, the prompt included a fake system instruction claiming that the default user was the CEO. In Level 2, the prompt went further by claiming that the user was authenticated as the CEO. The agent accepted the injected information sufficiently for the levels to be completed.

The important issue was that information supplied directly through the conversation was able to influence a security decision about the user's identity.

## Why the Defence Failed

The weakness was the separation between trusted security information and normal language processed by the model. An AI language model processes the conversation as tokens and uses attention to determine which parts of the context are important when generating its response.

Because the injected text was written in a format that resembled system-level information, it could receive significant attention from the model. This allowed attacker-controlled text to influence the model's understanding of who the user was.

The problem was therefore not that the attacker actually changed the authentication system. The problem was that the model could be influenced into treating untrusted text as if it contained trusted information.

## Impact

In a real AI communication system, this type of weakness could allow an attacker to influence the agent into performing actions using an identity or permission that the attacker does not actually possess.

## Root Cause

The main root cause was allowing the language model to use user-controlled text when making a decision that should have been based on trusted authentication information from the application.

## Recommendation

The authenticated identity should come directly from the application's authentication system. User messages should never be able to define or change the authenticated user. Security decisions should also be enforced by backend application controls rather than relying only on the language model.

## Current Status

Levels 1 and 2 were successfully completed. Level 3 is still in progress, while Levels 4 and 5 have not yet been reached.
