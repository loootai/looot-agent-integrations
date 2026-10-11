---
name: looot-quickstart
description: Use when a task needs live or external data (work emails, company and people enrichment, SERP, keyword volume, backlinks, web pages, news). Search looot's 2,500+ endpoints by the job, read the price, run one call.
version: 1.0.0
metadata:
  openclaw:
    requires:
      env: [LOOOT_TOKEN]
    primaryEnv: LOOOT_TOKEN
    homepage: https://looot.ai
---

# looot quickstart

looot is one key and one prepaid balance for 2,500+ data API endpoints from 90+ providers. Searching the catalog and reading prices is free. A failed call costs nothing.

## With the MCP server

If the `looot` MCP server is configured (https://api.looot.ai/mcp), use its tools: `search_catalog`, `inspect`, `run`, `runs_get`, `balance`.

## Without MCP (REST)

Token: `$LOOOT_TOKEN`, created at https://looot.ai (Settings, Agent tokens). Never print it or write it to a file.

1. Search, free, no token:

```bash
curl -s "https://api.looot.ai/v1/public-catalog?q=find+a+work+email"
```

2. Read the endpoint id, input names and price from the result.
3. Run one call:

```bash
curl -s -X POST "https://api.looot.ai/v1/runs?wait=30" \
  -H "Authorization: Bearer $LOOOT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"endpointId":"serper-search","input":{"q":"best crm for agencies","num":5},"idempotencyKey":"run-001"}'
```

`idempotencyKey` is required and must be unique per call. `status` is one of queued, running, completed, failed, blocked, stopped, reconciliation_pending, pending_provider. Poll `GET /v1/runs/{runId}` until it is terminal (completed, failed, blocked, stopped). `result` is the provider's raw body.

## Rules

- Tell the user the price before a run that costs more than a cent.
- Do not retry a failed run without a new `idempotencyKey`.
- The full skill set is at https://github.com/loootai/looot-skills.
