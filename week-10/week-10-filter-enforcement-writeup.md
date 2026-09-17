# Week 10 Filter Enforcement Writeup

## What the application-layer filter does and why it looks like the right fix

From the live demo, I understood the application-layer filter as a check that starts with the user's `tenant_id`. The application checks that the tenant ID exists, sends the search to the vector database, and then removes any result whose `tenant_id` does not match the user's tenant.

At first, this looks correct to me because the user should only see documents belonging to their own company. The application is checking the tenant before the results are returned to the user, so it is easy to think the data is already protected.

The problem I noticed is that the database has already returned the data before the application removes it.

## The specific scenario in which it fails

The failure happens when someone can reach the vector database without going through the application.

In the normal flow I observed, it is:

**User → Application → Vector Database**

The application filter runs in that path.

But in the bypass scenario, it becomes:

**Attacker → Vector Database**

There is no application involved, so there is no application-layer filter to run. The database can return records belonging to different tenants.

This also means the application-layer filter does not solve the fact that unauthorised records were already retrieved. The records may not be shown to the user, but the retrieval has still happened.

## How the bypass works

In the live demo, I saw that the bypass was simple: instead of sending the search through the application, the attacker called the vector database directly with a search such as an outstanding invoice balance query.

Because the database itself had no tenant restriction, the response contained results from different companies. The application never got the chance to remove the unwanted records.

The main thing I took from the demo is that the filter was not completely useless. It worked when the request followed the normal application path. The weakness was that the database itself did not enforce the same rule.

## What the database-layer fix does differently

The database-layer fix puts the tenant condition inside the database search itself. The search includes the tenant ID, so the database returns only records where the stored tenant ID matches it.

The database therefore filters the records before they leave the database.

When I think about the same direct database request after this fix, the attacker cannot simply skip the application and remove the protection. The tenant condition is already part of the database query.

For me, this is the main difference: the application-layer control depends on the request passing through the application, while the database-layer control is applied where the records are retrieved.

## My analogy

I see it like a warehouse with different companies' goods stored inside. An application-layer filter is like a receptionist checking the goods after the warehouse worker has already brought several companies' items to the front desk. The receptionist can remove the wrong items before the customer leaves, but the wrong items have already left their storage area.

A database-layer filter is different. It is like giving the warehouse worker the customer's company ID before picking anything. The worker brings out only goods belonging to that company in the first place.

That is why, from what I saw in the demo, the database-layer control provides a stronger boundary for this case. The restriction is applied where the records are stored and retrieved, not only after the application receives them.
