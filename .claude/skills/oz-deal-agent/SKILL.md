---
name: oz-deal-agent
description: Find personalised Australian OzBargain deals, verify offer terms and use locally saved feedback.
---

Read and follow the shared skill at `../../../.agents/skills/oz-deal-agent/SKILL.md` relative to this file. Resolve the shared Python scripts relative to that shared skill, not this wrapper. Preserve all local-state, sourcing and verification rules.

Use the shared host-discovery scheduling instructions after the user chooses a frequency. Claude Desktop has local scheduled-task capabilities, but discover what is actually available to the current session. `/loop` and session cron are temporary, so do not present them as durable delivery. Cloud tasks cannot assume access to a local SQLite database. If no persistent scheduling interface can be used, clearly tell the user to return to the conversation and ask for a check.
