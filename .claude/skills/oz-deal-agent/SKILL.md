---
name: oz-deal-agent
description: Find personalised Australian OzBargain deals, verify offer terms and use locally saved feedback.
---

Read and follow the shared skill at `../../../.agents/skills/oz-deal-agent/SKILL.md` relative to this file. Resolve the shared Python scripts relative to that shared skill, not this wrapper. Preserve all local-state, sourcing and verification rules.

For persistent scheduled digests, prefer Claude Desktop's local scheduled tasks if available; `/loop` and session cron are temporary and are not a durable daily delivery mechanism. If a durable scheduling interface is unavailable to this session, prepare the prompt and guide the user to create the task in Claude Desktop, but do not claim a task exists until verified. Do not use a cloud task that cannot access the user's local SQLite database. On macOS the shared scheduler can install the independent local RSS collector; use the shared skill's scheduling instructions.
