## Evidence B — Real API Documentation

### API Reviewed
GitHub REST API

### Documentation
https://docs.github.com/en/rest/using-the-rest-api/getting-started-with-the-rest-api

### What I Found

I reviewed GitHub's official REST API documentation to understand how a real API request is structured.

The documentation identifies the major components of an API request, including the HTTP method, path, headers, authentication and parameters.

For HTTP methods, the documentation explains that GET is generally used to retrieve resources, POST to create resources, PATCH to update properties, PUT to replace resources, and DELETE to delete resources.

The documentation also explains authentication and shows that many API endpoints require an authentication token with the appropriate permissions.

This connects directly to what I learned in Session 13 about HTTP request anatomy and API security. When analysing an API request, I should not only look at whether a request contains a token. I also need to consider what the authenticated user is authorised to access and what information supplied by the client should be independently verified by the server.

### Screenshot Evidence

<img width="1919" height="1079" alt="Screenshot 2026-08-20 125221" src="https://github.com/user-attachments/assets/acc8c6f7-d688-4d82-8c74-1438a79ba42c" />


### Security Observation

The documentation shows that an API request contains several components that a security analyst needs to understand. From a security perspective, authentication alone does not determine what a user is allowed to access. The server must still enforce appropriate authorization and validate client-supplied values.
