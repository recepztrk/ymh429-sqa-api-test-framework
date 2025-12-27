# Project Roadmap Checklist (v1)

## Phase 0 — Repo + working baseline
- [ ] Create Git repo (GitHub/GitLab)
- [ ] Add Python venv + requirements.txt
- [ ] Add folders: api/, tests/, docs/evidence/, docs/diagrams/
- [ ] Add OpenAPI contract: openapi_v1.yaml
- [ ] Add report template: YMH429_Final_Rapor_Sablonu.docx

## Phase 1 — API contract freeze (v1)
- [ ] Confirm business rules (qty, cart total, stock, order states, payment idempotency)
- [ ] Confirm roles/authorization policy (admin vs customer)
- [ ] Confirm error response model + status code mapping
- [ ] Update openapi_v1.yaml to match decisions

## Phase 2 — Minimal API implementation
- [ ] Implement /health
- [ ] Implement /auth/register + /auth/login (JWT)
- [ ] Implement /products endpoints (list, get, admin create)
- [ ] Implement /orders endpoints (create, get, cancel)
- [ ] Implement /payments endpoints (create, get)
- [ ] Provide seed data or setup endpoint/fixture approach

## Phase 3 — Test framework skeleton
- [ ] BaseClient (base_url, headers, auth token)
- [ ] Domain clients (AuthClient, ProductClient, OrderClient, PaymentClient)
- [ ] Central assertions (status/schema/business)
- [ ] Failure logging to docs/evidence/

## Phase 4 — Test suite implementation
- [ ] Implement SMK-01 smoke flow
- [ ] Implement AUTH-* tests
- [ ] Implement PROD-* tests
- [ ] Implement ORD-* tests
- [ ] Implement PAY-* tests
- [ ] Add data-driven payloads (tests/data/*.json)

## Phase 5 — CI + reporting
- [ ] Add CI workflow: start API + run pytest
- [ ] Produce junit.xml (and optional html)
- [ ] Upload artifacts

## Phase 6 — Final report
- [ ] Fill Sections 1–2 (literature + problem + existing methods)
- [ ] Fill Section 3 (architecture + tech choices + step-by-step + evidence)
- [ ] Fill Section 4 (evaluation, limitations, future work)
- [ ] IEEE references
- [ ] Verify format requirements (margins/font/spacing)
