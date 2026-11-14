---
name: redis
description: Redis development guidance for application code, configuration and reviews. Use whenever a task touches Redis: data modeling and key naming, client setup and connection handling, security, monitoring and triage, Redis Cluster, or Redis Search and vector search.
---

# Redis

Entry point to the Redis knowledge base. Do not read every topic. Pick the topics relevant to the task from the index, read each topic's `SKILL.md`, then open only the `references/` files the guide points to for the case at hand.

## Index

| Topic | Read when | Path |
|---|---|---|
| Core | choosing a data structure (String, Hash, List, Set, Sorted Set, JSON, Stream, Vector Set), Hash vs JSON, counters, leaderboards, sessions, key naming | `upstream/redis-core/SKILL.md` |
| Connections | client setup (redis-py, Jedis, Lettuce, NRedisStack, others), pooling, pipelining, timeouts, client-side caching, slow commands such as `KEYS`, `SMEMBERS`, `HGETALL`, iterating with `SCAN` | `upstream/redis-connections/SKILL.md` |
| Security | auth, ACL users, TLS, `bind` and protected-mode, firewalling, dangerous commands, production hardening | `upstream/redis-security/SKILL.md` |
| Observability | metrics and alerts, incident triage with `SLOWLOG`, `INFO`, `MEMORY DOCTOR`, `CLIENT LIST`, Prometheus or Datadog wiring | `upstream/redis-observability/SKILL.md` |
| Clustering | Redis Cluster key design, hash tags, `CROSSSLOT` errors, multi-key operations, reads from replicas | `upstream/redis-clustering/SKILL.md` |
| Search | `FT.CREATE` schemas, field types, query syntax, `FT.SEARCH`, `FT.AGGREGATE`, `FT.HYBRID`, vector KNN, HNSW tuning, RAG retrieval, index aliases, `FT.PROFILE` | `upstream/redis-search/SKILL.md` |

## Rules

- A task that only uses Redis in passing, such as reading an env var with the Redis URL, needs no topic.
- When a task spans topics, for example a new cache layer, read Core first and then Connections.
- The local project's conventions and its client library version take priority over this guidance. Say so when they conflict.

Source: [redis/agent-skills](https://github.com/redis/agent-skills), MIT. `upstream/` holds the official skill folders unmodified; update them by re-copying from upstream (pinned commit in `upstream/SOURCE`).
