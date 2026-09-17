# Week 10 Filter Enforcement Writeup

## What the application-layer filter does and why it looks like the right fix

The application-layer filter starts by taking the `tenant_id` from the user's session. It checks that the tenant ID exists and then sends the search to the vector database. After the database returns the results, the application removes any result whose `tenant_id` does not match the user's tenant.

At first, this looks correct because the user should only see documents belonging to their own company. The filter is checking the tenant before the results are returned to the user, so it is easy to assume the data is already protected.

The problem is that the database has already returned the data before the filter removes it.

## The specific scenario in which it fails

The problem appears when someone can reach the vector database without going through the application.

In the normal flow, it is:

**User → Application → Vector Database**

The application filter runs in that path.

But in the bypass scenario, the attacker goes directly to the database:

**Attacker → Vector Database**

There is no application involved, so there is no application-layer filter to run. The database can return records belonging to different tenants.

This also means the application-layer filter does not solve the fact that unauthorised records were already retrieved. The records may not be shown to the user, but the retrieval has still happened.

## How the bypass works

In the live demo, the bypass was simple: instead of sending the search through the application, the attacker called the vector database directly with a search such as an outstanding invoice balance query.

Because the database itself had no tenant restriction, the response contained results from different companies. The application never got the chance to remove the unwanted records.

The important point for me is that the filter was not completely useless; it worked only when the request followed the normal application path. The weakness was that the database itself did not enforce the same rule.

## What the database-layer fix does differently

The database-layer fix puts the tenant condition inside the database search itself. The search includes the tenant ID and the database is instructed to return only records where the stored tenant ID matches it.

So the database does the filtering before the results leave the database.

If an attacker tries the direct database request again, the tenant condition is still part of the query. They cannot simply skip the application and remove the protection because the protection is now attached to the data search itself.

This makes the database the final place enforcing the company boundary, rather than depending only on the application to remember to filter the results.

## My analogy

I see it like a warehouse with different companies' goods stored inside. An application-layer filter is like a receptionist checking the goods after the warehouse worker has already brought several companies' items to the front desk. The receptionist can remove the wrong items before the customer leaves, but the wrong items have already left their storage area.

A database-layer filter is different. It is like giving the warehouse worker the customer's company ID before picking anything. The worker brings out only goods belonging to that company in the first place.

That is why the database-layer control is stronger for this case. The restriction is applied where the records are stored and retrieved, not only after the application receives them.
