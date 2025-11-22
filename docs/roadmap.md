# Roadmap

## Current Status
**Version**: 1.0 (Enterprise MVP)
**Readiness**: Ready for internal deployment.

## Future Plans (Commercial SaaS Transition)

### Phase 1: Infrastructure Hardening
-   [ ] **Database Migration**: Move from file-based storage to PostgreSQL.
-   [ ] **Task Queue**: Implement Celery/Redis for handling concurrent review requests.
-   [ ] **API Layer**: Build a REST API to serve report data to a web dashboard.

### Phase 2: SaaS Features
-   [ ] **Authentication**: Implement OAuth2 (GitLab/GitHub) for user login.
-   [ ] **Multi-Tenancy**: Isolate data between different organizations.
-   [ ] **Billing Integration**: Stripe integration for subscription plans.

### Phase 3: Advanced Intelligence
-   [ ] **Fine-tuned Models**: Train custom LLMs on specific codebases.
-   [ ] **Auto-Fix**: Automatically commit suggested fixes to the branch.
-   [ ] **Performance Profiling**: Integrate with APM tools for runtime performance analysis.
