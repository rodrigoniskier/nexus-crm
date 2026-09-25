# Security Policy

Nexus CRM stores contact and deal information in a local SQLite database. Treat that database as runtime data, not source code.

## Rules

- Never commit `*.db`, exports containing real client data, credentials or environment secrets.
- Use synthetic records in demonstrations and screenshots.
- If deployed for multiple users, add authentication, authorization and a server-side database before using real customer data.
- A public Streamlit deployment of this demo must not be treated as a secure multi-tenant CRM.

Report vulnerabilities through GitHub Private Vulnerability Reporting / Security Advisories when available.
